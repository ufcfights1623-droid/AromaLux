import os

files_to_create = """
powdery|✨|Powdery Fragrances|Soft, delicate, and powdery fragrances with a gentle touch
sweet|🍬|Sweet Fragrances|Delicious and sugary sweet perfumes for those who love gourmand scents
fruity|🍓|Fruity Fragrances|Juicy and fruity fragrances bursting with tropical and berry notes
tropical|🌴|Tropical Fragrances|Exotic tropical fragrances evoking island paradise vibes
soft|☁️|Soft Fragrances|Gentle and airy soft fragrances with a whisper-like quality
citrus|🍊|Citrus Fragrances|Bright and zesty citrus fragrances perfect for energy and freshness
musky|🌙|Musky Fragrances|Sensual and alluring musky fragrances with depth and mystery
woody|🌲|Woody Fragrances|Rich, earthy, and woody fragrances for sophistication and strength
leather|🎒|Leather Fragrances|Bold leather fragrances with a rebellious and bold character
green|🌿|Green Fragrances|Fresh and herbal green fragrances with natural plant essence
aromatic|🌱|Aromatic Fragrances|Herbaceous and aromatic fragrances with Mediterranean charm
patchouli|🍂|Patchouli Fragrances|Earthy patchouli fragrances with vintage bohemian appeal
amber|🔥|Amber Fragrances|Warm amber fragrances with golden, luxurious depth
oud|👑|Oud Fragrances|Premium oud fragrances, the king of perfume ingredients
animalic|🦁|Animalic Fragrances|Wild and primal animalic fragrances for daring personalities
tobacco|🚬|Tobacco Fragrances|Smoky tobacco fragrances with leather and spice notes
aquatic|💧|Aquatic Fragrances|Clean and aquatic fragrances evoking water and sea breeze
oriental|🧞|Oriental Fragrances|Warm, sensual, and mysterious oriental fragrances
light|☀️|Light Fragrances|Subtle and delicate light fragrances for minimalists
boozy|🍷|Boozy Fragrances|Rich and intoxicating boozy fragrances with alcohol notes
coffee|☕|Coffee Fragrances|Aromatic coffee fragrances perfect for coffee lovers
chypre|🌾|Chypré Fragrances|Classic chypré fragrances with moss and citrus balance
"""

template = '''<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title} - AromaLux</title><link rel="stylesheet" href="{{{{ url_for('static', filename='style.css') }}}}"></head><body><nav><div class="navbar"><a href="/" class="logo">✨ AromaLux</a><ul class="nav-links"><li><a href="/">Home</a></li></ul><div class="nav-right"><a href="/cart" class="nav-icon">🛒<span class="cart-badge">0</span></a></div></div></nav><section class="hero"><div class="container"><h1>{emoji} {title}</h1><p>{description}</p></div></section><section class="section"><div class="container"><div style="display:flex;gap:1rem;margin-bottom:2rem;flex-wrap:wrap"><button class="btn btn-primary" onclick="filterByGender('all')" data-filter="all">All</button><button class="btn btn-outline" onclick="filterByGender('male')" data-filter="male">👨</button><button class="btn btn-outline" onclick="filterByGender('female')" data-filter="female">👩</button><button class="btn btn-outline" onclick="filterByGender('unisex')" data-filter="unisex">👥</button><select id="sortSelect" onchange="changeSortOrder()"><option>Latest</option><option value="price_low">Price: Low</option><option value="price_high">Price: High</option><option value="rating">Rated</option></select></div><div class="products-grid" id="products-grid"></div><div id="pagination" style="text-align:center;margin-top:2rem"></div></div></section><script src="{{{{ url_for('static', filename='script.js') }}}}"></script><script>const c='{slug}';let g='all',p=1,s='latest';function filterByGender(x){{g=x;p=1;load();document.querySelectorAll('[data-filter]').forEach(b=>{{b.classList.toggle('btn-primary',b.dataset.filter===x);b.classList.toggle('btn-outline',b.dataset.filter!==x);}});}function changeSortOrder(){{s=document.getElementById('sortSelect').value;p=1;load();}function load(){{fetch(`/api/classifications/${{c}}?page=${{p}}&gender=${{g}}&sort=${{s}}`).then(r=>r.json()).then(d=>{{render(d.perfumes);pag(d.pagination);}});}function render(products){{document.getElementById('products-grid').innerHTML=products.map(x=>`<div class="product-card"><div class="product-image" data-icon="💎">${{x.discount_percent>0?`<span class="discount-badge">-${{x.discount_percent}}%</span>`:''}}<span style="position:absolute;top:10px;right:10px;background:var(--magenta);color:white;padding:0.25rem;border-radius:20px;font-size:0.75rem">${{x.gender==='male'?'👨':x.gender==='female'?'👩':'👥'}}</span></div><h3>${{x.perfume_name}}</h3><p>${{x.brand_name}}</p><div>⭐${{x.rating}}</div><div>${{x.discount_percent>0?`<strike>$${{parseFloat(x.price).toFixed(2)}}</strike>$${{parseFloat(x.discounted_price).toFixed(2)}}`:`$${{parseFloat(x.price).toFixed(2)}}`}}</div><div style="display:flex;gap:0.5rem"><button onclick="addToCart(${{x.perfume_id}})">🛒</button><button onclick="toggleFavorite(${{x.perfume_id}})">♡</button></div></div>`).join('');}function pag(p){{let h='';if(p.page>1)h+=`<button onclick="goTo(${{p.page-1}})">Prev</button>`;for(let i=1;i<=5&&i<=p.pages;i++)h+=`<button style="font-weight:${{i===p.page?'bold':'normal'}}" onclick="goTo(${{i}})">${{i}}</button>`;if(p.page<p.pages)h+=`<button onclick="goTo(${{p.page+1}})">Next</button>`;document.getElementById('pagination').innerHTML=h;}function goTo(x){{p=x;load();window.scrollTo(0,0);}load();</script></body></html>
'''

os.chdir('e:/Desktop/AromaLux/templates')

for line in files_to_create.strip().split('\n'):
    if not line.strip():
        continue
    parts = line.split('|')
    slug, emoji, title, description = parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip()
    
    html = template.format(slug=slug, emoji=emoji, title=title, description=description)
    filename = f'{slug}.html'
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'✓ {filename}')
    except Exception as e:
        print(f'✗ {filename}: {e}')

print('\nDone!')
