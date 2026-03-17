#!/usr/bin/env python3
"""Generate all 26 classification HTML pages"""

import os

classifications = [
    ('spicy', '🌶️', 'Spicy Fragrances', 'Warm, bold, and spicy perfumes with exotic spices and warmth'),
    ('vanilla', '🍦', 'Vanilla Fragrances', 'Sweet and creamy vanilla perfumes for comfort and elegance'),
    ('powdery', '✨', 'Powdery Fragrances', 'Soft, delicate, and powdery fragrances with a gentle touch'),
    ('sweet', '🍬', 'Sweet Fragrances', 'Delicious and sugary sweet perfumes for those who love gourmand scents'),
    ('fruity', '🍓', 'Fruity Fragrances', 'Juicy and fruity fragrances bursting with tropical and berry notes'),
    ('tropical', '🌴', 'Tropical Fragrances', 'Exotic tropical fragrances evoking island paradise vibes'),
    ('soft', '☁️', 'Soft Fragrances', 'Gentle and airy soft fragrances with a whisper-like quality'),
    ('citrus', '🍊', 'Citrus Fragrances', 'Bright and zesty citrus fragrances perfect for energy and freshness'),
    ('musky', '🌙', 'Musky Fragrances', 'Sensual and alluring musky fragrances with depth and mystery'),
    ('woody', '🌲', 'Woody Fragrances', 'Rich, earthy, and woody fragrances for sophistication and strength'),
    ('leather', '🎒', 'Leather Fragrances', 'Bold leather fragrances with a rebellious and bold character'),
    ('green', '🌿', 'Green Fragrances', 'Fresh and herbal green fragrances with natural plant essence'),
    ('aromatic', '🌱', 'Aromatic Fragrances', 'Herbaceous and aromatic fragrances with Mediterranean charm'),
    ('patchouli', '🍂', 'Patchouli Fragrances', 'Earthy patchouli fragrances with vintage bohemian appeal'),
    ('amber', '🔥', 'Amber Fragrances', 'Warm amber fragrances with golden, luxurious depth'),
    ('oud', '👑', 'Oud Fragrances', 'Premium oud fragrances, the king of perfume ingredients'),
    ('animalic', '🦁', 'Animalic Fragrances', 'Wild and primal animalic fragrances for daring personalities'),
    ('tobacco', '🚬', 'Tobacco Fragrances', 'Smoky tobacco fragrances with leather and spice notes'),
    ('aquatic', '💧', 'Aquatic Fragrances', 'Clean and aquatic fragrances evoking water and sea breeze'),
    ('oriental', '🧞', 'Oriental Fragrances', 'Warm, sensual, and mysterious oriental fragrances'),
    ('light', '☀️', 'Light Fragrances', 'Subtle and delicate light fragrances for minimalists'),
    ('boozy', '🍷', 'Boozy Fragrances', 'Rich and intoxicating boozy fragrances with alcohol notes'),
    ('coffee', '☕', 'Coffee Fragrances', 'Aromatic coffee fragrances perfect for coffee lovers'),
    ('chypre', '🌾', 'Chypré Fragrances', 'Classic chypré fragrances with moss and citrus balance'),
]

template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AromaLux</title>
    <link rel="stylesheet" href="{{{{ url_for('static', filename='style.css') }}}}">
</head>
<body>
    <nav>
        <div class="navbar">
            <a href="/" class="logo">✨ AromaLux</a>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/perfumes">Perfumes</a></li>
                <li><a href="/classifications">Classifications</a></li>
            </ul>
            <div class="nav-right">
                <a href="/cart" class="nav-icon">🛒<span class="cart-badge">0</span></a>
                <a href="/profile" class="nav-icon">👤</a>
            </div>
        </div>
    </nav>

    <section class="hero" style="background: linear-gradient(135deg, rgba(232, 75, 138, 0.2), rgba(139, 92, 246, 0.2));">
        <div class="container">
            <h1>{emoji} {title}</h1>
            <p>{description}</p>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <div style="display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap;">
                <button class="btn btn-primary" onclick="filterByGender('all')" data-filter="all">All Products</button>
                <button class="btn btn-outline" onclick="filterByGender('male')" data-filter="male">👨 Male</button>
                <button class="btn btn-outline" onclick="filterByGender('female')" data-filter="female">👩 Female</button>
                <button class="btn btn-outline" onclick="filterByGender('unisex')" data-filter="unisex">👥 Unisex</button>
                <select id="sortSelect" class="sort-select" onchange="changeSortOrder()" style="padding: 0.75rem 1rem; border: 2px solid var(--light-gray); border-radius: 8px;">
                    <option value="latest">Latest</option>
                    <option value="price_low">Price: Low to High</option>
                    <option value="price_high">Price: High to Low</option>
                    <option value="rating">Top Rated</option>
                </select>
            </div>
            <div class="products-grid" id="products-grid"></div>
            <div id="pagination" style="text-align: center; margin-top: 2rem;"></div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2024 AromaLux. All rights reserved.</p>
        </div>
    </footer>

    <script src="{{{{ url_for('static', filename='script.js') }}}}"></script>
    <script>
        const classification = '{slug}';
        let currentGenderFilter = 'all', currentPage = 1, currentSort = 'latest';

        function filterByGender(g) {{ currentGenderFilter = g; currentPage = 1; loadProducts(); document.querySelectorAll('[data-filter]').forEach(b => {{ b.classList.toggle('btn-primary', b.dataset.filter === g); b.classList.toggle('btn-outline', b.dataset.filter !== g); }}); }}
        function changeSortOrder() {{ currentSort = document.getElementById('sortSelect').value; currentPage = 1; loadProducts(); }}
        function loadProducts() {{ fetch(`/api/classifications/${{classification}}?page=${{currentPage}}&gender=${{currentGenderFilter}}&sort=${{currentSort}}`).then(r => r.json()).then(d => {{ renderProducts(d.perfumes); renderPagination(d.pagination); }}); }}
        function renderProducts(products) {{ document.getElementById('products-grid').innerHTML = products.map(p => `<div class="product-card"><div class="product-image" data-icon="💎">${{p.discount_percent > 0 ? `<span class="discount-badge">-${{p.discount_percent}}%</span>` : ''}}<span class="gender-badge" style="position: absolute; top: 10px; right: 10px; background: var(--magenta); color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem;">${{p.gender === 'male' ? '👨' : p.gender === 'female' ? '👩' : '👥'}} ${{p.gender.toUpperCase()}}</span></div><h3>${{p.perfume_name}}</h3><p>${{p.brand_name}}</p><div class="product-rating">⭐ ${{p.rating}}</div><div class="product-price">${{p.discount_percent > 0 ? `<span class="original-price">$${{parseFloat(p.price).toFixed(2)}}</span><span class="price">$${{parseFloat(p.discounted_price).toFixed(2)}}</span>` : `<span class="price">$${{parseFloat(p.price).toFixed(2)}}</span>`}}</div><div class="product-actions"><button class="btn-add-cart" onclick="addToCart(${{p.perfume_id}})">🛒 Add</button><button class="btn-favorite" onclick="toggleFavorite(${{p.perfume_id}})">♡</button></div></div>`).join(''); }}
        function renderPagination(p) {{ let h = ''; if(p.page > 1) h += `<button class="btn btn-outline" onclick="goToPage(${{p.page - 1}})">← Prev</button>`; for(let i=1; i<=p.pages && i<=5; i++) h += `<button class="btn ${{i === p.page ? 'btn-primary' : 'btn-outline'}}" onclick="goToPage(${{i}})">${{i}}</button>`; if(p.page < p.pages) h += `<button class="btn btn-outline" onclick="goToPage(${{p.page + 1}})">Next →</button>`; document.getElementById('pagination').innerHTML = h; }}
        function goToPage(p) {{ currentPage = p; loadProducts(); window.scrollTo(0, 0); }}
        loadProducts();
    </script>
</body>
</html>
'''

os.chdir('e:/Desktop/AromaLux/templates')

for slug, emoji, title, description in classifications:
    filename = f'{slug}.html'
    content = template.format(
        slug=slug,
        emoji=emoji,
        title=title,
        description=description
    )
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created {filename}")

print(f"\n✓ Successfully created {len(classifications)} classification pages!")
