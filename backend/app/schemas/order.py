from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.order import OrderStatus, PaymentStatus


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)
    size: str = ""


class OrderCreate(BaseModel):
    contact_name: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=1, max_length=64)
    delivery_address: str = Field(min_length=1, max_length=1024)
    comment: str = Field(default="", max_length=2000)
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int | None
    product_name: str
    price: float
    quantity: int
    size: str

    @field_validator("price", mode="before")
    @classmethod
    def _to_float(cls, v):
        return float(v) if v is not None else 0.0


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    contact_name: str
    phone: str
    delivery_address: str
    comment: str
    status: OrderStatus
    payment_status: PaymentStatus
    total: float
    created_at: datetime
    items: list[OrderItemOut]

    @field_validator("total", mode="before")
    @classmethod
    def _to_float(cls, v):
        return float(v) if v is not None else 0.0
