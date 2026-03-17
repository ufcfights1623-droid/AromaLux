/**
 * AromaLux - Luxury Perfume Marketplace
 * JavaScript Main Functionality
 * Client-side logic for e-commerce operations
 */

// ============================================================================
// GLOBAL STATE MANAGEMENT
// ============================================================================

const AppState = {
    user: null,
    cart: [],
    favorites: [],
    filters: {
        search: '',
        category: 0,
        brand: '',
        fragrance_type: '',
        min_price: 0,
        max_price: 10000,
        sort: 'latest'
    },
    currentPage: 1,
    isLoggedIn: false
};

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    loadUserSession();
});

async function initializeApp() {
    console.log('🌟 AromaLux initialized');
    
    // Load cart from localStorage
    loadCartFromLocalStorage();
    
    // Setup navigation
    setupNavigation();
    
    // Load content based on current page
    const path = window.location.pathname;
    if (path.includes('/perfumes')) {
        loadPerfumes();
    } else if (path.includes('/cart')) {
        loadCart();
    } else if (path.includes('/blogs')) {
        loadBlogs();
    } else if (path.includes('/profile')) {
        loadUserProfile();
    }
}

function setupEventListeners() {
    // Hamburger menu
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }
    
    // Search functionality
    const searchForm = document.querySelector('.search-bar');
    if (searchForm) {
        searchForm.addEventListener('submit', handleSearch);
    }
    
    // Scroll animations
    window.addEventListener('scroll', handleScroll);
    
    // Close mobile menu on link click
    if (navLinks) {
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }
}

// ============================================================================
// NAVIGATION & UI
// ============================================================================

function setupNavigation() {
    const navbar = document.querySelector('nav');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar?.classList.add('scrolled');
        } else {
            navbar?.classList.remove('scrolled');
        }
    });
}

function handleScroll() {
    // Lazy load animations
    const elements = document.querySelectorAll('[data-animate]');
    
    elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
            el.classList.add('animated');
        }
    });
}

function handleSearch(e) {
    e.preventDefault();
    const searchInput = e.target.querySelector('input');
    AppState.filters.search = searchInput.value;
    AppState.currentPage = 1;
    loadPerfumes();
}

// ============================================================================
// PERFUME PRODUCTS
// ============================================================================

async function loadPerfumes(page = 1) {
    try {
        const params = new URLSearchParams({
            ...AppState.filters,
            page: page
        });
        
        const response = await fetch(`/api/perfumes?${params}`);
        const data = await response.json();
        
        if (data.perfumes) {
            renderPerfumes(data.perfumes);
            renderPagination(data.pagination);
            AppState.currentPage = page;
        }
    } catch (error) {
        console.error('Error loading perfumes:', error);
        showNotification('Error loading perfumes', 'error');
    }
}

function renderPerfumes(perfumes) {
    const grid = document.querySelector('.products-grid');
    if (!grid) return;
    
    grid.innerHTML = perfumes.map(perfume => `
        <div class="product-card" data-id="${perfume.perfume_id}">
            <div class="product-image" data-icon="💎">
                ${perfume.discount_percent > 0 ? `
                    <div class="product-badge">
                        <span class="discount-badge">-${perfume.discount_percent}%</span>
                    </div>
                ` : ''}
                ${perfume.stock_quantity === 0 ? '<div class="badge badge-primary" style="position: absolute;">Out of Stock</div>' : ''}
            </div>
            <h3 class="product-name" title="${perfume.perfume_name}">${perfume.perfume_name}</h3>
            <p class="product-brand">${perfume.brand_name}</p>
            <div class="product-rating">
                <span class="stars">⭐ ${perfume.rating}</span>
                <span>(${perfume.review_count} reviews)</span>
            </div>
            <div class="product-price">
                ${perfume.discount_percent > 0 ? `
                    <span class="original-price">$${perfume.price.toFixed(2)}</span>
                    <span class="price">$${perfume.discounted_price.toFixed(2)}</span>
                ` : `
                    <span class="price">$${perfume.price.toFixed(2)}</span>
                `}
            </div>
            <div class="product-actions">
                <button class="btn-add-cart" onclick="addToCart(${perfume.perfume_id})" 
                    ${perfume.stock_quantity === 0 ? 'disabled' : ''}>
                    🛒 Add to Cart
                </button>
                <button class="btn-favorite" onclick="toggleFavorite(${perfume.perfume_id})"
                    title="Add to favorites">♡</button>
            </div>
        </div>
    `).join('');
    
    // Add click handlers for product detail
    document.querySelectorAll('.product-card').forEach(card => {
        card.querySelector('.product-image').addEventListener('click', () => {
            window.location.href = `/perfume/${card.dataset.id}`;
        });
        card.querySelector('.product-name').addEventListener('click', () => {
            window.location.href = `/perfume/${card.dataset.id}`;
        });
    });
}

function renderPagination(pagination) {
    const container = document.querySelector('.pagination-container');
    if (!container) return;
    
    let html = `<div class="pagination">`;
    
    if (pagination.current_page > 1) {
        html += `<button class="btn btn-outline" onclick="loadPerfumes(${pagination.current_page - 1})">← Previous</button>`;
    }
    
    for (let i = 1; i <= pagination.total_pages; i++) {
        if (i === pagination.current_page) {
            html += `<button class="btn btn-primary" disabled>${i}</button>`;
        } else {
            html += `<button class="btn btn-outline" onclick="loadPerfumes(${i})">${i}</button>`;
        }
    }
    
    if (pagination.current_page < pagination.total_pages) {
        html += `<button class="btn btn-outline" onclick="loadPerfumes(${pagination.current_page + 1})">Next →</button>`;
    }
    
    html += `</div>`;
    container.innerHTML = html;
}

// ============================================================================
// CART MANAGEMENT
// ============================================================================

async function addToCart(perfumeId, quantity = 1, bottleSize = '50ml') {
    try {
        const response = await fetch('/api/cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                perfume_id: perfumeId,
                quantity: quantity,
                bottle_size: bottleSize
            })
        });
        
        if (response.ok) {
            showNotification('Added to cart!', 'success');
            updateCartBadge();
        } else {
            const error = await response.json();
            showNotification(error.error || 'Error adding to cart', 'error');
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        showNotification('Error adding to cart', 'error');
    }
}

async function loadCart() {
    try {
        const response = await fetch('/api/cart');
        if (!response.ok) {
            window.location.href = '/login';
            return;
        }
        
        const data = await response.json();
        renderCartItems(data.items, data.summary);
    } catch (error) {
        console.error('Error loading cart:', error);
    }
}

function renderCartItems(items, summary) {
    const container = document.querySelector('.cart-items');
    const summaryContainer = document.querySelector('.cart-summary');
    
    if (!container) return;
    
    if (items.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 3rem;">
                <p style="font-size: 3rem; margin-bottom: 1rem;">🛒</p>
                <h3>Your cart is empty</h3>
                <p>Continue shopping and add some luxury fragrances!</p>
                <a href="/perfumes" class="btn btn-primary" style="margin-top: 1rem;">Browse Perfumes</a>
            </div>
        `;
        return;
    }
    
    container.innerHTML = items.map((item, index) => `
        <div class="cart-item" data-id="${item.cart_id}">
            <div class="cart-item-image">💎</div>
            <div class="cart-item-info">
                <div class="cart-item-name">${item.perfume_name}</div>
                <div class="cart-item-brand">${item.brand_name}</div>
                <div class="cart-item-brand">Size: ${item.bottle_size}</div>
                <div class="cart-item-price">$${item.discounted_price.toFixed(2)} each</div>
            </div>
            <div class="cart-item-controls">
                <div class="quantity-control">
                    <button onclick="updateCartQuantity(${item.cart_id}, ${item.quantity - 1})">−</button>
                    <input type="number" value="${item.quantity}" min="1" max="999" 
                        onchange="updateCartQuantity(${item.cart_id}, this.value)">
                    <button onclick="updateCartQuantity(${item.cart_id}, ${item.quantity + 1})">+</button>
                </div>
                <div class="cart-item-price">$${item.item_total.toFixed(2)}</div>
                <button class="cart-item-remove" onclick="removeFromCart(${item.cart_id})">🗑️</button>
            </div>
        </div>
    `).join('');
    
    if (summaryContainer) {
        summaryContainer.innerHTML = `
            <h3>Order Summary</h3>
            <div class="summary-row">
                <span>Subtotal:</span>
                <span>$${summary.subtotal.toFixed(2)}</span>
            </div>
            <div class="summary-row">
                <span>Tax (5%):</span>
                <span>$${summary.tax.toFixed(2)}</span>
            </div>
            <div class="summary-row">
                <span>Shipping:</span>
                <span>$10.00</span>
            </div>
            <div class="summary-row total">
                <span>Total:</span>
                <span>$${(summary.total + 10).toFixed(2)}</span>
            </div>
            <button class="btn btn-primary" style="width: 100%; margin-top: 1.5rem; padding: 1rem;"
                onclick="proceedToCheckout()">Proceed to Checkout</button>
            <a href="/perfumes" class="btn btn-outline" style="width: 100%; margin-top: 0.75rem; padding: 1rem; text-align: center;">
                Continue Shopping
            </a>
        `;
    }
}

async function updateCartQuantity(cartId, quantity) {
    quantity = parseInt(quantity);
    if (quantity < 1) return;
    
    try {
        const response = await fetch('/api/cart/update', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cart_id: cartId,
                quantity: quantity
            })
        });
        
        if (response.ok) {
            loadCart();
        }
    } catch (error) {
        console.error('Error updating cart:', error);
    }
}

async function removeFromCart(cartId) {
    if (!confirm('Remove this item from cart?')) return;
    
    try {
        const response = await fetch('/api/cart', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cart_id: cartId
            })
        });
        
        if (response.ok) {
            loadCart();
            updateCartBadge();
        }
    } catch (error) {
        console.error('Error removing from cart:', error);
    }
}

function loadCartFromLocalStorage() {
    const saved = localStorage.getItem('aromalux_cart');
    if (saved) {
        AppState.cart = JSON.parse(saved);
        updateCartBadge();
    }
}

function updateCartBadge() {
    const badge = document.querySelector('.cart-badge');
    if (badge) {
        fetch('/api/cart')
            .then(r => r.json())
            .then(data => {
                badge.textContent = data.summary.item_count || 0;
            })
            .catch(() => {
                badge.textContent = AppState.cart.length;
            });
    }
}

// ============================================================================
// FAVORITES
// ============================================================================

async function toggleFavorite(perfumeId) {
    try {
        const isFavorited = AppState.favorites.includes(perfumeId);
        const method = isFavorited ? 'DELETE' : 'POST';
        
        const response = await fetch(`/api/favorites/${perfumeId}`, { method });
        
        if (response.ok) {
            if (isFavorited) {
                AppState.favorites = AppState.favorites.filter(id => id !== perfumeId);
                showNotification('Removed from favorites', 'info');
            } else {
                AppState.favorites.push(perfumeId);
                showNotification('Added to favorites!', 'success');
            }
            updateFavoriteButtons();
        }
    } catch (error) {
        console.error('Error toggling favorite:', error);
    }
}

function updateFavoriteButtons() {
    document.querySelectorAll('.btn-favorite').forEach(btn => {
        const card = btn.closest('.product-card');
        const perfumeId = parseInt(card?.dataset.id);
        
        if (AppState.favorites.includes(perfumeId)) {
            btn.classList.add('active');
            btn.textContent = '♥';
        } else {
            btn.classList.remove('active');
            btn.textContent = '♡';
        }
    });
}

// ============================================================================
// CHECKOUT & ORDERS
// ============================================================================

async function proceedToCheckout() {
    if (!AppState.isLoggedIn) {
        window.location.href = '/login';
        return;
    }
    
    // Show checkout modal
    showCheckoutModal();
}

function showCheckoutModal() {
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>Checkout</h2>
                <button class="modal-close" onclick="this.closest('.modal').remove()">✕</button>
            </div>
            <form id="checkout-form" onsubmit="submitCheckout(event)">
                <div class="form-group">
                    <label>Payment Method</label>
                    <select name="payment_method" required>
                        <option value="">Select a payment method</option>
                        <option value="credit_card">Credit Card</option>
                        <option value="debit_card">Debit Card</option>
                        <option value="paypal">PayPal</option>
                        <option value="stripe">Stripe</option>
                        <option value="cash_on_delivery">Cash on Delivery</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Shipping Address</label>
                    <select name="shipping_address_id" required>
                        <option value="">Select or add address</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%; padding: 1rem;">
                    Complete Order
                </button>
            </form>
        </div>
    `;
    
    document.body.appendChild(modal);
    loadAddressOptions();
}

async function loadAddressOptions() {
    try {
        const response = await fetch('/api/addresses');
        const addresses = await response.json();
        
        const select = document.querySelector('select[name="shipping_address_id"]');
        addresses.forEach(addr => {
            const option = document.createElement('option');
            option.value = addr.address_id;
            option.textContent = `${addr.street_address}, ${addr.city}`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading addresses:', error);
    }
}

async function submitCheckout(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    try {
        const response = await fetch('/api/orders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                payment_method: formData.get('payment_method'),
                shipping_address_id: formData.get('shipping_address_id')
            })
        });
        
        if (response.ok) {
            const order = await response.json();
            showNotification('Order placed successfully!', 'success');
            setTimeout(() => {
                window.location.href = `/orders`;
            }, 1500);
        }
    } catch (error) {
        console.error('Error placing order:', error);
        showNotification('Error placing order', 'error');
    }
}

// ============================================================================
// BLOGS
// ============================================================================

async function loadBlogs() {
    try {
        const response = await fetch('/api/blogs');
        const blogs = await response.json();
        renderBlogs(blogs);
    } catch (error) {
        console.error('Error loading blogs:', error);
    }
}

function renderBlogs(blogs) {
    const container = document.querySelector('.blogs-grid');
    if (!container) return;
    
    container.innerHTML = blogs.map(blog => `
        <article class="blog-card">
            <div class="blog-image" style="background: linear-gradient(135deg, #E84B8A, #8B5CF6);">
                📰
            </div>
            <div class="blog-content">
                <h3>${blog.title}</h3>
                <p>${blog.short_description}</p>
                <div class="blog-meta">
                    <span>By ${blog.author}</span>
                    <span>${new Date(blog.created_at).toLocaleDateString()}</span>
                </div>
                <a href="/blog/${blog.slug}" class="btn btn-primary">Read More →</a>
            </div>
        </article>
    `).join('');
}

// ============================================================================
// USER PROFILE
// ============================================================================

async function loadUserProfile() {
    try {
        const response = await fetch('/api/profile');
        if (!response.ok) {
            window.location.href = '/login';
            return;
        }
        
        const user = await response.json();
        AppState.user = user;
        AppState.isLoggedIn = true;
        renderUserProfile(user);
    } catch (error) {
        console.error('Error loading profile:', error);
        window.location.href = '/login';
    }
}

function renderUserProfile(user) {
    const container = document.querySelector('.profile-container');
    if (!container) return;
    
    container.innerHTML = `
        <div class="profile-header">
            <div class="profile-avatar">👤</div>
            <div class="profile-info">
                <h2>${user.first_name} ${user.last_name}</h2>
                <p>${user.email}</p>
            </div>
        </div>
        <div class="profile-content">
            <div class="profile-section">
                <h3>Personal Information</h3>
                <form id="profile-form" onsubmit="updateProfile(event)">
                    <div class="form-group">
                        <label>First Name</label>
                        <input type="text" name="first_name" value="${user.first_name}">
                    </div>
                    <div class="form-group">
                        <label>Last Name</label>
                        <input type="text" name="last_name" value="${user.last_name}">
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" value="${user.email}" disabled>
                    </div>
                    <div class="form-group">
                        <label>Phone</label>
                        <input type="tel" name="phone" value="${user.phone || ''}">
                    </div>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                </form>
            </div>
        </div>
    `;
}

async function updateProfile(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    
    try {
        const response = await fetch('/api/profile', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                first_name: formData.get('first_name'),
                last_name: formData.get('last_name'),
                phone: formData.get('phone')
            })
        });
        
        if (response.ok) {
            showNotification('Profile updated successfully!', 'success');
        }
    } catch (error) {
        console.error('Error updating profile:', error);
        showNotification('Error updating profile', 'error');
    }
}

// ============================================================================
// AUTHENTICATION
// ============================================================================

async function loadUserSession() {
    try {
        const response = await fetch('/api/profile');
        if (response.ok) {
            AppState.isLoggedIn = true;
            updateAuthUI();
        }
    } catch (error) {
        AppState.isLoggedIn = false;
    }
}

function updateAuthUI() {
    const authButtons = document.querySelector('.auth-buttons');
    if (!authButtons) return;
    
    if (AppState.isLoggedIn) {
        authButtons.innerHTML = `
            <a href="/profile" class="btn btn-outline">👤 Profile</a>
            <a href="/logout" class="btn btn-primary">Logout</a>
        `;
    } else {
        authButtons.innerHTML = `
            <a href="/login" class="btn btn-outline">Login</a>
            <a href="/signup" class="btn btn-primary">Sign Up</a>
        `;
    }
}

// ============================================================================
// UTILITIES
// ============================================================================

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideDown 0.3s ease;
        z-index: 3000;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// ============================================================================
// FILTERS
// ============================================================================

function applyFilters() {
    AppState.currentPage = 1;
    loadPerfumes();
}

function filterByCategory(categoryId) {
    AppState.filters.category = categoryId;
    applyFilters();
}

function filterByBrand(brand) {
    AppState.filters.brand = brand;
    applyFilters();
}

function filterByPriceRange(min, max) {
    AppState.filters.min_price = min;
    AppState.filters.max_price = max;
    applyFilters();
}

function sortBy(sortOption) {
    AppState.filters.sort = sortOption;
    applyFilters();
}

// ============================================================================
// FRAGRANCE RECOMMENDATION QUIZ
// ============================================================================

async function submitFragranceQuiz(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    const preferences = {
        preference_type: formData.get('preference_type'),
        fragrance_families: Array.from(form.querySelectorAll('input[name="fragrance_families"]:checked'))
            .map(el => el.value),
        occasions: Array.from(form.querySelectorAll('input[name="occasions"]:checked'))
            .map(el => el.value),
        price_range: formData.get('price_range'),
        skin_type: formData.get('skin_type')
    };
    
    try {
        const response = await fetch('/api/recommendation/quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(preferences)
        });
        
        const recommendations = await response.json();
        displayRecommendations(recommendations.recommendations);
    } catch (error) {
        console.error('Error getting recommendations:', error);
        showNotification('Error getting recommendations', 'error');
    }
}

function displayRecommendations(recommendations) {
    const container = document.querySelector('.recommendations-container');
    if (!container) return;
    
    container.innerHTML = `
        <h3>Recommended Perfumes for You</h3>
        <div class="products-grid">
            ${recommendations.map(perfume => `
                <div class="product-card">
                    <div class="product-image">💎</div>
                    <h3 class="product-name">${perfume.perfume_name}</h3>
                    <p class="product-brand">${perfume.brand_name}</p>
                    <div class="product-rating">⭐ ${perfume.rating}</div>
                    <div class="product-price">
                        <span class="price">$${perfume.discounted_price.toFixed(2)}</span>
                    </div>
                    <button class="btn-add-cart" onclick="addToCart(${perfume.perfume_id})">
                        Add to Cart
                    </button>
                </div>
            `).join('')}
        </div>
    `;
    
    container.scrollIntoView({ behavior: 'smooth' });
}

// ============================================================================
// GENDER AND CLASSIFICATION FILTERS
// ============================================================================

function filterByGender(gender) {
    const buttons = document.querySelectorAll('[data-filter]');
    buttons.forEach(btn => {
        btn.classList.toggle('btn-primary', btn.dataset.filter === gender);
        btn.classList.toggle('btn-outline', btn.dataset.filter !== gender);
    });
    
    // Trigger product reload - each classification page handles this
    if (window.loadProducts) {
        window.currentGenderFilter = gender;
        window.currentPage = 1;
        window.loadProducts();
    }
}

function changeSortOrder() {
    const selectElement = document.getElementById('sortSelect');
    if (selectElement && window.loadProducts) {
        window.currentSort = selectElement.value;
        window.currentPage = 1;
        window.loadProducts();
    }
}

function loadClassifications() {
    fetch('/api/classifications')
        .then(r => r.json())
        .then(classifications => {
            const grid = document.getElementById('classifications-grid');
            if (grid) {
                grid.innerHTML = classifications.map(c => `
                    <a href="/classification/${c.slug}" class="classification-card" style="background: linear-gradient(135deg, #E84B8A, #8B5CF6); text-decoration: none; padding: 1.5rem; border-radius: 12px; text-align: center; color: white; transition: all 0.3s ease;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📦</div>
                        <h3 style="margin: 0; font-size: 1rem;">${c.name}</h3>
                        <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem;">${c.count} perfumes</p>
                    </a>
                `).join('');
            }
        })
        .catch(err => console.error('Error loading classifications:', err));
}

// ============================================================================
// EXPORT
// ============================================================================

window.AppState = AppState;
window.addToCart = addToCart;
window.removeFromCart = removeFromCart;
window.updateCartQuantity = updateCartQuantity;
window.toggleFavorite = toggleFavorite;
window.loadCart = loadCart;
window.loadPerfumes = loadPerfumes;
window.loadBlogs = loadBlogs;
window.showNotification = showNotification;
window.applyFilters = applyFilters;
window.proceedToCheckout = proceedToCheckout;
window.submitCheckout = submitCheckout;
window.submitFragranceQuiz = submitFragranceQuiz;
window.filterByGender = filterByGender;
window.changeSortOrder = changeSortOrder;
window.loadClassifications = loadClassifications;
