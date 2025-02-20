async function searchProducts() {
    const searchTerm = document.getElementById('productSearch').value;
    const category = document.getElementById('categoryFilter')?.value;
    
    try {
        const response = await fetch(
            `/api/products/compare?name=${encodeURIComponent(searchTerm)}${category ? `&category=${encodeURIComponent(category)}` : ''}`,
            {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            }
        );
        
        if (!response.ok) {
            throw new Error('Search failed');
        }
        
        const data = await response.json();
        displayCompareResults(data);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('compareResults').innerHTML = 
            '<p class="error">Error fetching comparison data</p>';
    }
}

function displayCompareResults(data) {
    const container = document.getElementById('compareResults');
    
    const bestDeal = data.best_deal;
    const html = `
        <div class="best-deal">
            <h3>Best Deal Found</h3>
            <div class="product-card highlight">
                <h4>${bestDeal.name}</h4>
                <p class="price">$${bestDeal.price}</p>
                <p class="source">From: ${bestDeal.source}</p>
                <p class="category">${bestDeal.category || 'No category'}</p>
                <a href="${bestDeal.url}" target="_blank" class="btn">View Deal</a>
            </div>
        </div>
        
        <div class="price-comparison">
            <h3>Price Differences</h3>
            ${data.price_differences.map(diff => `
                <div class="price-difference">
                    <span class="source">${diff.source}</span>
                    <span class="difference">+$${diff.price_difference.toFixed(2)}</span>
                    <span class="percentage">(+${diff.percentage_difference.toFixed(1)}%)</span>
                </div>
            `).join('')}
        </div>
        
        <div class="summary">
            <p>Total products compared: ${data.total_compared}</p>
            <p>Price range: $${data.price_range.lowest} - $${data.price_range.highest}</p>
        </div>
    `;
    
    container.innerHTML = html;
} 