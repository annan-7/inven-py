from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from database import get_db, create_tables
from models import ItemCreate, ItemUpdate, ItemResponse, CategoryResponse, ItemListResponse
from crud import ItemCRUD

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Tuari Inventory API",
    description="Fast and efficient inventory management system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize database tables
create_tables()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def add_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Add a new item to inventory"""
    try:
        # Check if SKU already exists
        existing_item = ItemCRUD.get_by_sku(db, item.sku)
        if existing_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Item with SKU '{item.sku}' already exists"
            )
        
        db_item = ItemCRUD.add(db, item)
        return db_item
    except Exception as e:
        logger.error(f"Error adding item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add item"
        )

@app.get("/api/items/{item_id}", response_model=ItemResponse)
async def get_one(item_id: int, db: Session = Depends(get_db)):
    """Get a single item by ID"""
    db_item = ItemCRUD.get_one(db, item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    return db_item

@app.put("/api/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    """Update an existing item"""
    try:
        db_item = ItemCRUD.update(db, item_id, item_update)
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
        return db_item
    except Exception as e:
        logger.error(f"Error updating item {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update item"
        )

@app.delete("/api/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item by ID"""
    try:
        success = ItemCRUD.delete(db, item_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
    except Exception as e:
        logger.error(f"Error deleting item {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item"
        )

@app.get("/api/items/category/{category}", response_model=ItemListResponse)
async def get_category(
    category: str,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get items by category with pagination"""
    try:
        result = ItemCRUD.get_category(db, category, page, per_page)
        return ItemListResponse(
            items=result["items"],
            total=result["total"],
            page=result["page"],
            per_page=result["per_page"],
            total_pages=result["total_pages"]
        )
    except Exception as e:
        logger.error(f"Error getting category {category}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get category items"
        )

@app.get("/api/categories", response_model=List[CategoryResponse])
async def get_categories(db: Session = Depends(get_db)):
    """Get all categories with item count and total value"""
    try:
        categories = ItemCRUD.get_categories(db)
        return categories
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get categories"
        )

@app.get("/api/items", response_model=ItemListResponse)
async def get_all_items(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    db: Session = Depends(get_db)
):
    """Get all items with pagination and optional search"""
    try:
        if search:
            result = ItemCRUD.search_items(db, search, page, per_page)
        else:
            result = ItemCRUD.get_all_paginated(db, page, per_page)
        
        return ItemListResponse(
            items=result["items"],
            total=result["total"],
            page=result["page"],
            per_page=result["per_page"],
            total_pages=result["total_pages"]
        )
    except Exception as e:
        logger.error(f"Error getting items: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get items"
        )

@app.get("/api/items/low-stock", response_model=List[ItemResponse])
async def get_low_stock(
    threshold: int = Query(10, ge=0, description="Low stock threshold"),
    db: Session = Depends(get_db)
):
    """Get items with low stock"""
    try:
        items = ItemCRUD.get_low_stock(db, threshold)
        return items
    except Exception as e:
        logger.error(f"Error getting low stock items: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get low stock items"
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Tuari Inventory API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 