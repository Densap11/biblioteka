#!/usr/bin/env sh
set -eu

BASE="http://127.0.0.1:8000"
mkdir -p api-test-report

# Wait for health endpoint
echo "Waiting for API to become healthy..."
max=60
i=0
while [ $i -lt $max ]; do
  if curl -sSf "$BASE/api/health" >/dev/null 2>&1; then
    echo "API is up"
    break
  fi
  i=$((i+1))
  sleep 1
done
if [ $i -ge $max ]; then
  echo "API did not start within $max seconds"
  exit 2
fi

# Check health response
echo "Checking /api/health"
health=$(curl -s "$BASE/api/health")
if [ "$(echo "$health" | jq -r .status)" != "healthy" ]; then
  echo "Health check failed: $health"
  exit 2
fi

# Create a book
echo "Creating a book"
book_resp=$(curl -sS -H "Content-Type: application/json" -d '{"title":"CI Book","author":"CI Bot","year":2025}' $BASE/api/books/)
book_id=$(echo "$book_resp" | jq -r .id)
if [ -z "$book_id" ] || [ "$book_id" = "null" ]; then
  echo "Failed to create book: $book_resp"
  exit 2
fi

# Create a copy
echo "Creating a copy"
inv="CI-COPY-$(date +%s)"
copy_resp=$(curl -sS -H "Content-Type: application/json" -d "{\"book_id\":${book_id},\"inventory_number\":\"${inv}\",\"status\":\"available\"}" $BASE/api/copies/)
copy_id=$(echo "$copy_resp" | jq -r .id)
if [ -z "$copy_id" ] || [ "$copy_id" = "null" ]; then
  echo "Failed to create copy: $copy_resp"
  exit 2
fi

# Create reader
echo "Creating a reader"
reader_resp=$(curl -sS -H "Content-Type: application/json" -d '{"full_name":"CI Reader","library_card":"CI-READER-001"}' $BASE/api/readers/)
reader_id=$(echo "$reader_resp" | jq -r .id)
if [ -z "$reader_id" ] || [ "$reader_id" = "null" ]; then
  echo "Failed to create reader: $reader_resp"
  exit 2
fi

# Create loan
echo "Creating a loan"
loan_resp=$(curl -sS -H "Content-Type: application/json" -d "{\"copy_id\":${copy_id},\"reader_id\":${reader_id},\"loan_days\":7}" $BASE/api/loans/)
loan_id=$(echo "$loan_resp" | jq -r .id)
if [ -z "$loan_id" ] || [ "$loan_id" = "null" ]; then
  echo "Failed to create loan: $loan_resp"
  exit 2
fi

# Verify loan status
loan_check=$(curl -s $BASE/api/loans/${loan_id})
loan_status=$(echo "$loan_check" | jq -r .status)
if [ "$loan_status" != "active" ]; then
  echo "Loan status unexpected: $loan_check"
  exit 2
fi

# Return loan
echo "Returning loan $loan_id"
return_resp=$(curl -sS -X POST $BASE/api/loans/return/${loan_id})
return_status=$(echo "$return_resp" | jq -r .status)
if [ "$return_status" != "returned" ]; then
  echo "Return failed: $return_resp"
  exit 2
fi

# Verify copy status is available again
copy_check=$(curl -s $BASE/api/copies/${copy_id})
copy_status=$(echo "$copy_check" | jq -r .status)
if [ "$copy_status" != "available" ]; then
  echo "Copy status not available after return: $copy_check"
  exit 2
fi

# Write report
cat > api-test-report/api-results.json <<EOF
{
  "health": true,
  "book_id": ${book_id},
  "copy_id": ${copy_id},
  "reader_id": ${reader_id},
  "loan_id": ${loan_id},
  "timestamp": "$(date -Iseconds)"
}
EOF

echo "E2E smoke tests passed"
exit 0
