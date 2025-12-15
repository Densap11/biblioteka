from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.config import settings
from app.database import engine, Base

# Импортируем роутеры
from app.api.books import router as books_router
from app.api.readers import router as readers_router
from app.api.copies import router as copies_router
from app.api.loans import router as loans_router

# Создаем таблицы в БД
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы базы данных созданы успешно")
except Exception as e:
    print(f"❌ Ошибка при создании таблиц: {e}")

# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Подключаем роутеры
app.include_router(books_router, prefix="/api/books", tags=["Книги"])
app.include_router(readers_router, prefix="/api/readers", tags=["Читатели"])
app.include_router(copies_router, prefix="/api/copies", tags=["Экземпляры"])
app.include_router(loans_router, prefix="/api/loans", tags=["Выдачи"])

# HTML страница
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "app_name": settings.APP_NAME}
    )

# Простой health check
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "endpoints": [
            "/api/books",
            "/api/readers", 
            "/api/copies",
            "/api/loans",
            "/api/docs"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)