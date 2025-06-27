// Global variables
let currentPage = 1;
let currentSearch = '';
let currentCategory = '';
let itemsPerPage = 50;
let itemsToDelete = null;

// API base URL
const API_BASE = '/api';

// Utility functions
function showLoading() {
    document.getElementById('loadingSpinner').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loadingSpinner').classList.add('hidden');
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 fade-in ${
        type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
    }`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// API functions
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showNotification(error.message, 'error');
        throw error;
    }
}

// Data loading functions
async function loadItems() {
    showLoading();
    try {
        let url = `/items?page=${currentPage}&per_page=${itemsPerPage}`;
        if (currentSearch) url += `&search=${encodeURIComponent(currentSearch)}`;
        
        const data = await apiCall(url);
        displayItems(data.items);
        updatePagination(data);
        updateStatistics();
    } catch (error) {
        console.error('Error loading items:', error);
    } finally {
        hideLoading();
    }
}

async function loadCategories() {
    try {
        const categories = await apiCall('/categories');
        updateCategoryFilter(categories);
        updateCategoryStats(categories);
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

async function loadLowStockCount() {
    try {
        const lowStockItems = await apiCall('/items/low-stock?threshold=10');
        document.getElementById('lowStockCount').textContent = lowStockItems.length;
    } catch (error) {
        console.error('Error loading low stock count:', error);
    }
}

// Display functions
function displayItems(items) {
    const tbody = document.getElementById('itemsTableBody');
    tbody.innerHTML = '';
    
    if (items.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="px-6 py-4 text-center text-gray-500">
                    No items found
                </td>
            </tr>
        `;
        return;
    }
    
    items.forEach(item => {
        const row = document.createElement('tr');
        row.className = 'hover:bg-gray-50 fade-in';
        
        const stockClass = item.quantity <= 10 ? 'text-red-600 font-semibold' : 'text-gray-900';
        const stockIcon = item.quantity <= 10 ? '<i class="fas fa-exclamation-triangle text-red-500 mr-1"></i>' : '';
        
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                    <div>
                        <div class="text-sm font-medium text-gray-900">${item.name}</div>
                        <div class="text-sm text-gray-500">${item.description || 'No description'}</div>
                    </div>
                </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    ${item.category}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-mono">
                ${item.sku}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="${stockClass}">${stockIcon}${item.quantity}</span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                $${parseFloat(item.price).toFixed(2)}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ${item.location || 'N/A'}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button onclick="editItem(${item.id})" class="text-blue-600 hover:text-blue-900 mr-3">
                    <i class="fas fa-edit"></i>
                </button>
                <button onclick="showDeleteModal(${item.id})" class="text-red-600 hover:text-red-900">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        
        tbody.appendChild(row);
    });
}

function updatePagination(data) {
    const startItem = (data.page - 1) * data.per_page + 1;
    const endItem = Math.min(startItem + data.items.length - 1, data.total);
    
    document.getElementById('startItem').textContent = startItem;
    document.getElementById('endItem').textContent = endItem;
    document.getElementById('totalItemsCount').textContent = data.total;
    document.getElementById('pageInfo').textContent = `Page ${data.page} of ${data.total_pages}`;
    
    // Update pagination buttons
    const prevBtn = document.querySelector('button[onclick="previousPage()"]');
    const nextBtn = document.querySelector('button[onclick="nextPage()"]');
    
    prevBtn.disabled = data.page <= 1;
    nextBtn.disabled = data.page >= data.total_pages;
    
    if (data.page <= 1) {
        prevBtn.classList.add('opacity-50', 'cursor-not-allowed');
    } else {
        prevBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
    
    if (data.page >= data.total_pages) {
        nextBtn.classList.add('opacity-50', 'cursor-not-allowed');
    } else {
        nextBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
}

function updateCategoryFilter(categories) {
    const select = document.getElementById('categoryFilter');
    const currentValue = select.value;
    
    // Keep "All Categories" option
    select.innerHTML = '<option value="">All Categories</option>';
    
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.category;
        option.textContent = `${category.category} (${category.item_count})`;
        select.appendChild(option);
    });
    
    // Restore selected value if it still exists
    if (currentValue) {
        select.value = currentValue;
    }
}

function updateStatistics() {
    // Update total items count
    const totalItemsElement = document.getElementById('totalItems');
    const totalItemsCountElement = document.getElementById('totalItemsCount');
    const count = parseInt(totalItemsCountElement.textContent) || 0;
    totalItemsElement.textContent = count;
}

function updateCategoryStats(categories) {
    document.getElementById('totalCategories').textContent = categories.length;
    
    // Calculate total value
    const totalValue = categories.reduce((sum, cat) => sum + cat.total_value, 0);
    document.getElementById('totalValue').textContent = `$${totalValue.toFixed(2)}`;
}

// Modal functions
function showAddModal() {
    document.getElementById('modalTitle').textContent = 'Add New Item';
    document.getElementById('itemForm').reset();
    document.getElementById('itemId').value = '';
    document.getElementById('itemModal').classList.remove('hidden');
}

function showEditModal(item) {
    document.getElementById('modalTitle').textContent = 'Edit Item';
    document.getElementById('itemId').value = item.id;
    document.getElementById('itemName').value = item.name;
    document.getElementById('itemCategory').value = item.category;
    document.getElementById('itemSku').value = item.sku;
    document.getElementById('itemDescription').value = item.description || '';
    document.getElementById('itemQuantity').value = item.quantity;
    document.getElementById('itemPrice').value = item.price;
    document.getElementById('itemLocation').value = item.location || '';
    document.getElementById('itemModal').classList.remove('hidden');
}

function closeModal() {
    document.getElementById('itemModal').classList.add('hidden');
}

function showDeleteModal(itemId) {
    itemsToDelete = itemId;
    document.getElementById('deleteModal').classList.remove('hidden');
}

function closeDeleteModal() {
    document.getElementById('deleteModal').classList.add('hidden');
    itemsToDelete = null;
}

// Event handlers
async function editItem(itemId) {
    try {
        const item = await apiCall(`/items/${itemId}`);
        showEditModal(item);
    } catch (error) {
        console.error('Error loading item for edit:', error);
    }
}

async function confirmDelete() {
    if (!itemsToDelete) return;
    
    try {
        await apiCall(`/items/${itemsToDelete}`, { method: 'DELETE' });
        showNotification('Item deleted successfully');
        closeDeleteModal();
        loadItems();
        loadCategories();
    } catch (error) {
        console.error('Error deleting item:', error);
    }
}

// Form submission
document.getElementById('itemForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const itemId = document.getElementById('itemId').value;
    const formData = {
        name: document.getElementById('itemName').value,
        category: document.getElementById('itemCategory').value,
        sku: document.getElementById('itemSku').value,
        description: document.getElementById('itemDescription').value,
        quantity: parseInt(document.getElementById('itemQuantity').value),
        price: parseFloat(document.getElementById('itemPrice').value),
        location: document.getElementById('itemLocation').value
    };
    
    try {
        if (itemId) {
            // Update existing item
            await apiCall(`/items/${itemId}`, {
                method: 'PUT',
                body: JSON.stringify(formData)
            });
            showNotification('Item updated successfully');
        } else {
            // Add new item
            await apiCall('/items', {
                method: 'POST',
                body: JSON.stringify(formData)
            });
            showNotification('Item added successfully');
        }
        
        closeModal();
        loadItems();
        loadCategories();
    } catch (error) {
        console.error('Error saving item:', error);
    }
});

// Search and filter functions
let searchTimeout;
document.getElementById('searchInput').addEventListener('input', function(e) {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        currentSearch = e.target.value;
        currentPage = 1;
        loadItems();
    }, 300);
});

document.getElementById('categoryFilter').addEventListener('change', function(e) {
    currentCategory = e.target.value;
    currentPage = 1;
    if (currentCategory) {
        loadCategoryItems();
    } else {
        loadItems();
    }
});

async function loadCategoryItems() {
    showLoading();
    try {
        const data = await apiCall(`/items/category/${encodeURIComponent(currentCategory)}?page=${currentPage}&per_page=${itemsPerPage}`);
        displayItems(data.items);
        updatePagination(data);
    } catch (error) {
        console.error('Error loading category items:', error);
    } finally {
        hideLoading();
    }
}

// Pagination functions
function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        if (currentCategory) {
            loadCategoryItems();
        } else {
            loadItems();
        }
    }
}

function nextPage() {
    currentPage++;
    if (currentCategory) {
        loadCategoryItems();
    } else {
        loadItems();
    }
}

// Refresh function
async function refreshData() {
    currentPage = 1;
    currentSearch = '';
    currentCategory = '';
    document.getElementById('searchInput').value = '';
    document.getElementById('categoryFilter').value = '';
    
    await Promise.all([
        loadItems(),
        loadCategories(),
        loadLowStockCount()
    ]);
    
    showNotification('Data refreshed successfully');
}

// Initialize app
async function initApp() {
    showLoading();
    try {
        await Promise.all([
            loadItems(),
            loadCategories(),
            loadLowStockCount()
        ]);
    } catch (error) {
        console.error('Error initializing app:', error);
        showNotification('Failed to load data. Please refresh the page.', 'error');
    } finally {
        hideLoading();
    }
}

// Start the app when DOM is loaded
document.addEventListener('DOMContentLoaded', initApp); 