from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from database import Item
from models import ItemCreate, ItemUpdate
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class ItemCRUD:
    @staticmethod
    def add(db: Session, item: ItemCreate) -> Item:
        """Add a new item to inventory"""
        try:
            db_item = Item(**item.dict())
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            logger.info(f"Added item: {db_item.name} with SKU: {db_item.sku}")
            return db_item
        except Exception as e:
            db.rollback()
            logger.error(f"Error adding item: {e}")
            raise
    
    @staticmethod
    def get_one(db: Session, item_id: int) -> Optional[Item]:
        """Get a single item by ID with optimized query"""
        return db.query(Item).filter(Item.id == item_id).first()
    
    @staticmethod
    def get_by_sku(db: Session, sku: str) -> Optional[Item]:
        """Get item by SKU using index"""
        return db.query(Item).filter(Item.sku == sku).first()
    
    @staticmethod
    def update(db: Session, item_id: int, item_update: ItemUpdate) -> Optional[Item]:
        """Update an existing item"""
        try:
            db_item = db.query(Item).filter(Item.id == item_id).first()
            if not db_item:
                return None
            
            update_data = item_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_item, field, value)
            
            db.commit()
            db.refresh(db_item)
            logger.info(f"Updated item: {db_item.name} (ID: {item_id})")
            return db_item
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating item {item_id}: {e}")
            raise
    
    @staticmethod
    def delete(db: Session, item_id: int) -> bool:
        """Delete an item by ID"""
        try:
            db_item = db.query(Item).filter(Item.id == item_id).first()
            if not db_item:
                return False
            
            db.delete(db_item)
            db.commit()
            logger.info(f"Deleted item: {db_item.name} (ID: {item_id})")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting item {item_id}: {e}")
            raise
    
    @staticmethod
    def get_category(db: Session, category: str, page: int = 1, per_page: int = 50) -> dict:
        """Get items by category with pagination and optimized query"""
        offset = (page - 1) * per_page
        
        # Use index on category for efficient filtering
        query = db.query(Item).filter(Item.category == category)
        total = query.count()
        
        items = query.offset(offset).limit(per_page).all()
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def get_categories(db: Session) -> List[dict]:
        """Get all categories with item count and total value - optimized with aggregation"""
        result = db.query(
            Item.category,
            func.count(Item.id).label('item_count'),
            func.sum(Item.quantity * Item.price).label('total_value')
        ).group_by(Item.category).all()
        
        return [
            {
                "category": row.category,
                "item_count": row.item_count,
                "total_value": float(row.total_value or 0)
            }
            for row in result
        ]
    
    @staticmethod
    def search_items(db: Session, search_term: str, page: int = 1, per_page: int = 50) -> dict:
        """Search items by name, SKU, or description with pagination"""
        offset = (page - 1) * per_page
        
        # Use OR condition for flexible search across indexed fields
        search_filter = or_(
            Item.name.ilike(f"%{search_term}%"),
            Item.sku.ilike(f"%{search_term}%"),
            Item.description.ilike(f"%{search_term}%")
        )
        
        query = db.query(Item).filter(search_filter)
        total = query.count()
        
        items = query.offset(offset).limit(per_page).all()
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def get_low_stock(db: Session, threshold: int = 10) -> List[Item]:
        """Get items with low stock using quantity index"""
        return db.query(Item).filter(Item.quantity <= threshold).all()
    
    @staticmethod
    def get_all_paginated(db: Session, page: int = 1, per_page: int = 50) -> dict:
        """Get all items with pagination"""
        offset = (page - 1) * per_page
        
        total = db.query(Item).count()
        items = db.query(Item).offset(offset).limit(per_page).all()
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        } 