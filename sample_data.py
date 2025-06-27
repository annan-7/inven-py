#!/usr/bin/env python3
"""
Sample Data Generator for Tuari Inventory System
"""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from database import SessionLocal, Item
from models import ItemCreate
from datetime import datetime

def create_sample_data():
    """Create sample inventory data"""
    
    sample_items = [
        {
            "name": "MacBook Pro 16-inch",
            "category": "Electronics",
            "sku": "MBP16-001",
            "description": "Apple MacBook Pro with M2 Pro chip, 16GB RAM, 512GB SSD",
            "quantity": 15,
            "price": 2499.99,
            "location": "Warehouse A - Shelf 1"
        },
        {
            "name": "Dell XPS 13",
            "category": "Electronics",
            "sku": "DXP13-001",
            "description": "Dell XPS 13 laptop with Intel i7, 16GB RAM, 512GB SSD",
            "quantity": 8,
            "price": 1299.99,
            "location": "Warehouse A - Shelf 2"
        },
        {
            "name": "iPhone 15 Pro",
            "category": "Electronics",
            "sku": "IP15P-001",
            "description": "Apple iPhone 15 Pro 128GB, Titanium",
            "quantity": 25,
            "price": 999.99,
            "location": "Warehouse B - Shelf 1"
        },
        {
            "name": "Samsung Galaxy S24",
            "category": "Electronics",
            "sku": "SGS24-001",
            "description": "Samsung Galaxy S24 Ultra 256GB, Titanium Gray",
            "quantity": 12,
            "price": 1199.99,
            "location": "Warehouse B - Shelf 2"
        },
        {
            "name": "Wireless Mouse",
            "category": "Accessories",
            "sku": "WM001",
            "description": "Logitech MX Master 3S Wireless Mouse",
            "quantity": 50,
            "price": 99.99,
            "location": "Warehouse C - Shelf 1"
        },
        {
            "name": "Mechanical Keyboard",
            "category": "Accessories",
            "sku": "MK001",
            "description": "Corsair K100 RGB Mechanical Gaming Keyboard",
            "quantity": 20,
            "price": 229.99,
            "location": "Warehouse C - Shelf 2"
        },
        {
            "name": "4K Monitor",
            "category": "Electronics",
            "sku": "4KM001",
            "description": "LG 27-inch 4K Ultra HD Monitor with HDR",
            "quantity": 10,
            "price": 399.99,
            "location": "Warehouse A - Shelf 3"
        },
        {
            "name": "USB-C Cable",
            "category": "Accessories",
            "sku": "USBC001",
            "description": "Anker USB-C to USB-C Cable, 100W, 6ft",
            "quantity": 100,
            "price": 19.99,
            "location": "Warehouse C - Shelf 3"
        },
        {
            "name": "Laptop Stand",
            "category": "Accessories",
            "sku": "LS001",
            "description": "Rain Design mStand Laptop Stand for MacBook",
            "quantity": 30,
            "price": 59.99,
            "location": "Warehouse C - Shelf 4"
        },
        {
            "name": "External SSD",
            "category": "Storage",
            "sku": "ESSD001",
            "description": "Samsung T7 Portable SSD 1TB, USB 3.2 Gen 2",
            "quantity": 40,
            "price": 89.99,
            "location": "Warehouse B - Shelf 3"
        },
        {
            "name": "Webcam",
            "category": "Electronics",
            "sku": "WC001",
            "description": "Logitech StreamCam 1080p Webcam with USB-C",
            "quantity": 35,
            "price": 169.99,
            "location": "Warehouse B - Shelf 4"
        },
        {
            "name": "Gaming Headset",
            "category": "Accessories",
            "sku": "GH001",
            "description": "SteelSeries Arctis Pro Wireless Gaming Headset",
            "quantity": 15,
            "price": 329.99,
            "location": "Warehouse C - Shelf 5"
        },
        {
            "name": "Tablet",
            "category": "Electronics",
            "sku": "TAB001",
            "description": "iPad Air 5th Gen 64GB, Space Gray",
            "quantity": 18,
            "price": 599.99,
            "location": "Warehouse B - Shelf 5"
        },
        {
            "name": "Power Bank",
            "category": "Accessories",
            "sku": "PB001",
            "description": "Anker PowerCore 26800mAh Portable Charger",
            "quantity": 25,
            "price": 49.99,
            "location": "Warehouse C - Shelf 6"
        },
        {
            "name": "Bluetooth Speaker",
            "category": "Electronics",
            "sku": "BS001",
            "description": "JBL Flip 6 Portable Bluetooth Speaker",
            "quantity": 22,
            "price": 129.99,
            "location": "Warehouse A - Shelf 4"
        }
    ]
    
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_count = db.query(Item).count()
        if existing_count > 0:
            print(f"⚠️  Database already contains {existing_count} items")
            response = input("Do you want to add sample data anyway? (y/N): ")
            if response.lower() != 'y':
                print("❌ Sample data creation cancelled")
                return
        
        print("📦 Adding sample inventory data...")
        
        for item_data in sample_items:
            # Check if SKU already exists
            existing_item = db.query(Item).filter(Item.sku == item_data["sku"]).first()
            if existing_item:
                print(f"⚠️  SKU {item_data['sku']} already exists, skipping...")
                continue
            
            # Create item
            item = Item(**item_data)
            db.add(item)
            print(f"✅ Added: {item_data['name']} ({item_data['sku']})")
        
        db.commit()
        print(f"🎉 Successfully added {len(sample_items)} sample items to inventory!")
        
        # Show summary
        total_items = db.query(Item).count()
        total_value = db.query(Item).with_entities(
            db.func.sum(Item.quantity * Item.price)
        ).scalar() or 0
        
        print("\n📊 Inventory Summary:")
        print(f"   Total Items: {total_items}")
        print(f"   Total Value: ${total_value:,.2f}")
        
        # Show categories
        from sqlalchemy import func
        categories = db.query(
            Item.category,
            func.count(Item.id).label('count'),
            func.sum(Item.quantity * Item.price).label('value')
        ).group_by(Item.category).all()
        
        print("\n🏷️  Categories:")
        for category, count, value in categories:
            print(f"   {category}: {count} items (${value:,.2f})")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error adding sample data: {e}")
        raise
    finally:
        db.close()

def main():
    """Main function"""
    print("=" * 50)
    print("🎯 Tuari Inventory - Sample Data Generator")
    print("=" * 50)
    
    try:
        create_sample_data()
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 