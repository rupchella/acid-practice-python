from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


class CreateAccountRequest(BaseModel):
    owner_id: UUID
    currency: str = Field(default="RUB", min_length=3, max_length=3)


class AccountResponse(BaseModel):
    id: UUID
    owner_id: UUID
    balance: Decimal
    currency: str
    created_at: datetime
    updated_at: datetime