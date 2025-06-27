from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Item name")
    category: str = Field(..., min_length=1, max_length=100, description="Item category")
    description: Optional[str] = Field(None, max_length=1000, description="Item description")
    quantity: int = Field(0, ge=0, description="Item quantity")
    price: float = Field(0.0, ge=0.0, description="Item price")
    sku: str = Field(..., min_length=1, max_length=100, description="Stock Keeping Unit")
    location: Optional[str] = Field(None, max_length=100, description="Item location")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    quantity: Optional[int] = Field(None, ge=0)
    price: Optional[float] = Field(None, ge=0.0)
    sku: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=100)

class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CategoryResponse(BaseModel):
    category: str
    item_count: int
    total_value: float

class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    total: int
    page: int
    per_page: int
    total_pages: int 