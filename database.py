from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Index, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from datetime import datetime
import os

# Create database directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Database URL
DATABASE_URL = "sqlite:///./data/inventory.db"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False  # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    quantity = Column(Integer, default=0, index=True)
    price = Column(Float, default=0.0, index=True)
    sku = Column(String(100), unique=True, index=True)
    location = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    
    # Create composite indexes for common query patterns
    __table_args__ = (
        Index('idx_category_name', 'category', 'name'),
        Index('idx_sku_category', 'sku', 'category'),
        Index('idx_quantity_price', 'quantity', 'price'),
        Index('idx_created_updated', 'created_at', 'updated_at'),
    )

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!") 