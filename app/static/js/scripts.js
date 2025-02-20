async function searchProducts() {
    const searchInput = document.getElementById('searchInput').value;
    try {
        const response = await fetch(`/products?search=${searchInput}`);
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

function displayProducts(products) {
    const productList = document.getElementById('productList');
    productList.innerHTML = products.map(product => `
        <div class="product-card">
            <h3>${product.name}</h3>
            <p>Price: ${product.price}</p>
            <p>Source: ${product.source}</p>
        </div>
    `).join('');
}
