from typing import Any

from sqladmin import Admin
from starlette.datastructures import FormData
from starlette.requests import Request


class MediaAdmin(Admin):
    """Admin с безопасной обработкой файловых полей формы.

    Базовый ``Admin._handle_form_data`` для пустого file-поля делает
    ``getattr(obj, key)`` по колонке модели. У нас поле ``image_upload`` —
    это поле формы, а не колонка ``Product``, поэтому базовый код падает с
    ``AttributeError: 'Product' object has no attribute 'image_upload'``.
    Передаём ``obj=None`` — тогда ветка с подстановкой прежнего файла
    пропускается (файловых колонок в моделях нет), а новый загруженный файл
    по-прежнему доходит до ``on_model_change``.
    """

    async def _handle_form_data(
        self, request: Request, obj: Any = None
    ) -> FormData:
        return await super()._handle_form_data(request, None)
