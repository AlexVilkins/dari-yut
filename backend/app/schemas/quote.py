from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.quote import QuoteStatus


class QuoteCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    phone: str = Field(min_length=1, max_length=64)
    company: str = Field(default="", max_length=255)
    product: str = Field(default="", max_length=255)
    quantity: str = Field(default="", max_length=64)
    comment: str = Field(default="", max_length=2000)


class QuoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    company: str
    product: str
    quantity: str
    comment: str
    status: QuoteStatus
    created_at: datetime
