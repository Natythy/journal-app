from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional

# ==============================================
# ENTRY SCHEMAS
# ==============================================

class EntryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

class EntryCreate(EntryBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ==============================================
# USER SCHEMAS
# ==============================================

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    id: int
    is_active: bool
    entries: List["Entry"] = []

    model_config = ConfigDict(from_attributes=True)