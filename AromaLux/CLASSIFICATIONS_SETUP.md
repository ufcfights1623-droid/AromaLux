# 🚀 AromaLux Classifications Setup Guide

## Quick Setup Instructions

### Step 1: Initialize Database Schema
```bash
mysql -u root -p < database.sql
```

**What this does:**
- Creates the `aromalux` database
- Creates 15 tables including perfumes with NEW fields:
  - `gender` (male, female, unisex)
  - `classification` (26 fragrance types)

### Step 2: Generate 1000+ Perfume Products
```bash
python seed_perfumes.py
```

**What this does:**
- Generates 1000 perfumes across 26 classifications
- Each classification gets ~38-39 perfumes (26 types × 38 = 1000)
- Each perfume is assigned:
  - Random gender (male, female, or unisex)
  - Random classification from 26 types
  - Realistic pricing, discounts, ratings, and fragrance notes

**Progress Output:**
```
✓ Progress: 100/1000 perfumes inserted (10%)
✓ Progress: 200/1000 perfumes inserted (20%)
... (continues to 100%)
```

### Step 3: Verify Data
```bash
mysql -u root -p -e "USE aromalux; SELECT COUNT(*) as total_perfumes FROM perfumes; SELECT DISTINCT classification, COUNT(*) as count FROM perfumes GROUP BY classification;"
```

### Step 4: Start Flask Application
```bash
python app.py
```

Then open: `http://localhost:5000/classifications`

---

## How Classifications Work

### 26 Fragrance Types Available:
1. **Floral** - Rose, Jasmine, Peony
2. **Fresh** - Bright citrus and aquatic
3. **Spicy** - Warm exotic spices
4. **Vanilla** - Sweet and creamy
5. **Powdery** - Soft and delicate
6. **Sweet** - Gourmand and dessert-like
7. **Fruity** - Juicy and tropical
8. **Tropical** - Exotic island vibes
9. **Soft** - Gentle and airy
10. **Citrus** - Zesty and bright
11. **Musky** - Sensual and alluring
12. **Woody** - Rich and earthy
13. **Leather** - Bold and rebellious
14. **Green** - Fresh herbal
15. **Aromatic** - Mediterranean charm
16. **Patchouli** - Bohemian earthy
17. **Amber** - Warm and luxurious
18. **Oud** - Premium and rare
19. **Animalic** - Wild and primal
20. **Tobacco** - Smoky and sophisticated
21. **Aquatic** - Clean water-like
22. **Oriental** - Warm and sensual
23. **Light** - Subtle and delicate
24. **Boozy** - Rich with alcohol notes
25. **Coffee** - Aromatic coffee vibes
26. **Chypré** - Classic moss and citrus

### Gender Filtering:
Each page includes buttons to filter by:
- 👨 Male perfumes
- 👩 Female perfumes
- 👥 Unisex perfumes
- All Products (mixed)

---

## URL Structure

### Browse Classifications:
- `/classifications` - View all 26 fragrance types
- `/classification/floral` - View Floral fragrances
- `/classification/fresh` - View Fresh fragrances
- `/classification/spicy` - View Spicy fragrances
- ... (any of the 26 types)

### API Endpoints:
```
GET /api/classifications
GET /api/classifications/{classification}?page=1&gender=all&sort=latest
GET /api/classifications/{classification}?page=1&gender=male&sort=price_low
GET /api/classifications/{classification}?page=1&gender=female&sort=rating
```

**Sort Options:**
- `latest` - Newest products first
- `price_low` - Price: Low to High
- `price_high` - Price: High to Low
- `rating` - Top Rated
- `featured` - Featured products

---

## Expected Results After Setup

After running `seed_perfumes.py`:

```
Total Perfumes in Database: 1000+
Total Classifications: 26
Products per Classification: ~38-39 (distributed)

Example Query Results:
floral     | 38 perfumes (15 male, 15 female, 8 unisex)
fresh      | 39 perfumes (14 male, 16 female, 9 unisex)
spicy      | 38 perfumes (16 male, 14 female, 8 unisex)
... (26 classifications)
```

---

## Features Included

✅ **Dynamic Product Loading** - Fetches from API on page load
✅ **Gender Filtering** - Filter by male/female/unisex
✅ **Sort Options** - Price, rating, latest, featured
✅ **Pagination** - 20 products per page
✅ **Responsive Design** - Works on mobile/tablet/desktop
✅ **Shopping Integration** - Add to cart with one click
✅ **Favorites** - Save favorite perfumes
✅ **Real-time Badge** - Shows gender (👨/👩/👥)

---

## Troubleshooting

### "No products showing"
**Solution:** Run `python seed_perfumes.py` to populate the database

### "Cannot connect to MySQL"
**Solution:** 
```bash
mysql -u root -p
# Enter password: root
```

### "Database 'aromalux' not found"
**Solution:** Run `mysql -u root -p < database.sql`

### "ModuleNotFoundError: No module named 'mysql'"
**Solution:**
```bash
pip install mysql-connector-python
```

---

## File Structure

```
AromaLux/
├── database.sql              ← Schema with gender & classification fields
├── seed_perfumes.py          ← Generates 1000+ products
├── app.py                    ← API endpoints for classifications
├── static/
│   ├── script.js             ← Filter & load functions
│   └── style.css             ← Gender badge styling
└── templates/
    ├── classifications.html  ← Main classifications page
    ├── floral.html          ← Floral classification page (loads products dynamically)
    ├── fresh.html           ← Fresh classification page
    ├── spicy.html           ← Spicy classification page
    ... (23 more classification pages)
    └── chypre.html          ← Last classification page
```

---

## Ready to Launch!

1. Run database setup ✅
2. Generate products ✅
3. Start Flask app ✅
4. Visit `/classifications` ✅

Your luxury perfume marketplace with 26 fragrance classifications is ready! 🌟
