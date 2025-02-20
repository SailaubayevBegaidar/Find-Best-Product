let products = [];
let editingProductId = null;

async function loadProducts() {
    try {
        const response = await fetch('/products', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        products = await response.json();
        displayProducts();
        updateCategoryFilter();
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

function displayProducts() {
    const productList = document.getElementById('productList');
    productList.innerHTML = products.map(product => `
        <div class="product-card">
            <h3>${product.name}</h3>
            <p class="price">$${product.price}</p>
            <p class="source">${product.source}</p>
            <p class="category">${product.category || 'No category'}</p>
            <div class="product-actions">
                <button onclick="editProduct('${product._id}')" class="btn edit">Edit</button>
                <button onclick="deleteProduct('${product._id}')" class="btn delete">Delete</button>
            </div>
        </div>
    `).join('');
}

async function saveProduct(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const productData = Object.fromEntries(formData);
    
    try {
        const url = editingProductId ? 
            `/products/${editingProductId}` : 
            '/products';
            
        const method = editingProductId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(productData)
        });
        
        if (response.ok) {
            closeModal();
            loadProducts();
        }
    } catch (error) {
        console.error('Error saving product:', error);
    }
}

// Add event listeners and initialize
document.addEventListener('DOMContentLoaded', () => {
    loadProducts();
    document.getElementById('productForm').addEventListener('submit', saveProduct);
}); 