# Tuari Inventory Management System

A fast and efficient desktop inventory management application built with FastAPI, SQLite, and a modern React-like frontend.

## Features

- 🚀 **Fast Performance**: Optimized SQLite database with proper indexing
- 📱 **Modern UI**: Beautiful, responsive interface with Tailwind CSS
- 🔍 **Smart Search**: Real-time search across items, SKU, and descriptions
- 📊 **Analytics**: Dashboard with statistics and low stock alerts
- 🏷️ **Category Management**: Organize items by categories
- 📄 **Pagination**: Efficient data loading with pagination
- ✨ **Real-time Updates**: Instant feedback and notifications

## API Endpoints

### Core CRUD Operations
- `POST /api/items` - Add new item
- `GET /api/items/{item_id}` - Get single item
- `PUT /api/items/{item_id}` - Update item
- `DELETE /api/items/{item_id}` - Delete item

### Advanced Queries
- `GET /api/items` - Get all items with pagination and search
- `GET /api/items/category/{category}` - Get items by category
- `GET /api/categories` - Get all categories with statistics
- `GET /api/items/low-stock` - Get items with low stock

### Utility
- `GET /api/health` - Health check endpoint

## Database Schema

The application uses SQLite with the following optimized schema:

```sql
CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    quantity INTEGER DEFAULT 0,
    price FLOAT DEFAULT 0.0,
    sku VARCHAR(100) UNIQUE NOT NULL,
    location VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Optimized indexes for performance
CREATE INDEX idx_category_name ON items(category, name);
CREATE INDEX idx_sku_category ON items(sku, category);
CREATE INDEX idx_quantity_price ON items(quantity, price);
CREATE INDEX idx_created_updated ON items(created_at, updated_at);
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Quick Start

1. **Clone and navigate to the project:**
   ```bash
   cd inventory-tuari
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database:**
   ```bash
   python database.py
   ```

4. **Start the application:**
   ```bash
   python main.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:8000`

### Alternative: Using uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Project Structure

```
inventory-tuari/
├── main.py              # FastAPI application
├── database.py          # Database configuration and models
├── models.py            # Pydantic models for validation
├── crud.py              # Database operations
├── requirements.txt     # Python dependencies
├── static/              # Frontend files
│   ├── index.html       # Main HTML page
│   └── app.js          # JavaScript application
├── data/                # SQLite database (created automatically)
│   └── inventory.db
└── README.md           # This file
```

## Performance Optimizations

### Database Indexing
- **Primary Key**: `id` for fast lookups
- **Composite Indexes**: Optimized for common query patterns
- **Unique Index**: `sku` for duplicate prevention
- **Search Indexes**: `name`, `category`, `quantity`, `price`

### API Efficiency
- **Pagination**: Prevents large data transfers
- **Selective Updates**: Only update changed fields
- **Error Handling**: Graceful error responses
- **Connection Pooling**: Efficient database connections

### Frontend Performance
- **Debounced Search**: Reduces API calls
- **Lazy Loading**: Load data on demand
- **Caching**: Browser-level caching
- **Optimized DOM**: Minimal re-renders

## Usage Examples

### Adding an Item
```bash
curl -X POST "http://localhost:8000/api/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "category": "Electronics",
    "sku": "LAP001",
    "description": "High-performance laptop",
    "quantity": 10,
    "price": 999.99,
    "location": "Warehouse A"
  }'
```

### Getting Items by Category
```bash
curl "http://localhost:8000/api/items/category/Electronics?page=1&per_page=20"
```

### Searching Items
```bash
curl "http://localhost:8000/api/items?search=laptop&page=1&per_page=10"
```

## Development

### Adding New Features
1. Update database models in `database.py`
2. Add CRUD operations in `crud.py`
3. Create API endpoints in `main.py`
4. Update frontend in `static/app.js`

### Database Migrations
The application automatically creates tables on startup. For schema changes:
1. Update the `Item` model in `database.py`
2. Delete the existing `data/inventory.db` file
3. Restart the application

## Troubleshooting

### Common Issues

**Database locked error:**
- Ensure no other process is using the database
- Check file permissions on the `data/` directory

**Port already in use:**
- Change the port in `main.py` or use a different port with uvicorn
- Kill existing processes using the port

**Import errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility

### Logs
The application logs to console. For production, consider:
- File-based logging
- Log rotation
- Error monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on GitHub

---

**Built with ❤️ for efficient inventory management** 