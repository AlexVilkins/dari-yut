from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.admin.app import MediaAdmin
from app.admin.auth import AdminAuth
from app.admin.views import ADMIN_VIEWS
from app.api.routers import auth, orders, products
from app.core.config import settings
from app.core.storage import MEDIA_ROOT, ensure_media_dirs
from app.db.session import engine

app = FastAPI(title=settings.PROJECT_NAME)

# Загруженные файлы (изображения товаров) раздаются как статика.
ensure_media_dirs()
app.mount(settings.MEDIA_URL, StaticFiles(directory=MEDIA_ROOT), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API-роутеры (фронт ходит сюда через runtimeConfig.public.apiBase).
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}


# Админка SQLAdmin на /admin (вход по роли admin).
admin = MediaAdmin(
    app,
    engine,
    title="Дари Уют — админка",
    authentication_backend=AdminAuth(secret_key=settings.SECRET_KEY),
)
for view in ADMIN_VIEWS:
    admin.add_view(view)


def run() -> None:
    """Запуск сервера напрямую: `python -m app.main` (или `python app/main.py`)."""
    import uvicorn

    # reload требует строку импорта, а не объект app.
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )


if __name__ == "__main__":
    run()
