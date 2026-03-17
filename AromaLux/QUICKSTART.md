# 🌟 AromaLux - Quick Start Guide (2 Minutes)

## ⚡ Express Setup

### Prerequisites Check
```bash
python --version    # Should be 3.8+
mysql --version     # Should be 8.0+
```

### 1. Setup Environment (30 seconds)
```bash
# Navigate to project
cd AromaLux

# Create virtual environment
python -m venv venv

# Activate it
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Database (30 seconds)
```bash
# Create database and tables
mysql -u root -p < database.sql

# Generate sample data (1000 perfumes)
python seed_perfumes.py
```

### 3. Configure App (30 seconds)
```bash
# Copy configuration
cp .env.example .env

# Edit .env with your MySQL password
# nano .env  (or use your editor)
```

### 4. Run Application (30 seconds)
```bash
python app.py
```

### 5. Access Website ✅
```
Open browser: http://localhost:5000
```

---

## 🛍️ Quick Feature Demo

### Create Test Account
- Email: `demo@aromalux.com`
- Password: `Demo12345!`

### Try Features
1. **Browse**: Visit /perfumes - see 1000+ perfumes
2. **Search**: Filter by price, brand, category
3. **Shop**: Add items to cart
4. **Checkout**: Complete order (test mode)
5. **Profile**: View account and orders

---

## 📁 Project Structure Overview

```
AromaLux/
├── app.py                 # Main Flask app
├── database.sql           # Database schema
├── seed_perfumes.py       # Data generator
├── requirements.txt       # Dependencies
├── config.py             # Configuration
├── static/
│   ├── style.css         # Luxury styling
│   ├── script.js         # Frontend logic
│   └── images/           # Product images
└── templates/            # 15+ HTML pages
```

---

## 🔑 Key Endpoints

| URL | Purpose |
|-----|---------|
| `/` | Homepage |
| `/perfumes` | Product listing |
| `/perfume/<id>` | Product details |
| `/cart` | Shopping cart |
| `/checkout` | Order checkout |
| `/login` | User login |
| `/signup` | Register account |
| `/profile` | User profile |
| `/blogs` | Blog articles |
| `/api/perfumes` | Product API |
| `/api/cart` | Cart API |

---

## 🎨 Customization (2 minutes)

### Change Color Scheme
Edit `static/style.css`:
```css
--primary-color: #E84B8A;    /* Change to your color */
--accent-color: #8B5CF6;
--secondary-color: #000000;
```

### Add New Perfume Brand
```sql
-- Add to database
INSERT INTO perfumes (perfume_name, brand_name, price, ...) 
VALUES ('New Perfume', 'New Brand', 89.99, ...);
```

### Customize Site Name
Edit `app.py`:
```python
app.config['APP_NAME'] = 'Your Perfume Shop'
```

---

## 🐛 Common Issues & Quick Fixes

| Issue | Fix |
|-------|-----|
| Port already in use | `python app.py --port 5001` |
| MySQL not running | `sudo systemctl start mysql` |
| Module not found | `pip install -r requirements.txt` |
| Database error | `mysql -u root -p < database.sql` |
| CSS not loading | Clear browser cache (Ctrl+Shift+Del) |

---

## 📊 Database Reset

```bash
# Backup current database
mysqldump -u root -p aromalux > backup.sql

# Reset database
mysql -u root -p < database.sql

# Regenerate data
python seed_perfumes.py
```

---

## 🚀 Next Steps

1. ✅ Run the app locally (you're here!)
2. 📝 Customize branding and settings
3. 💾 Add your own perfume products
4. 📤 Deploy to production (Heroku, AWS, etc.)
5. 🔒 Set up SSL certificate

---

## 📚 Full Documentation

See **README.md** and **INSTALLATION.md** for comprehensive guides

---

## 💡 Pro Tips

✨ **For Development**: Run with `FLASK_ENV=development`
🎯 **Testing**: Use SQLite for quick testing instead of MySQL
🚀 **Production**: Always use Gunicorn instead of Flask's dev server
🔐 **Security**: Change SECRET_KEY in .env before deploying
📦 **Deployment**: Use Docker for easy deployment

---

## 🎉 You're All Set!

Your luxury perfume marketplace is ready to go!

**Need help?**
- 📖 Check README.md
- 🔗 Visit documentation
- 📧 support@aromalux.com

---

**Happy selling! 🌟**
