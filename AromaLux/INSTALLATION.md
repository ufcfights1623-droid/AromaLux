# 🚀 AromaLux Installation & Setup Guide

## System Requirements

- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **MySQL**: 8.0 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 500MB minimum

## Complete Setup Instructions

### Step 1️⃣: Install Python

**Windows:**
```bash
# Download from python.org
# Run installer, check "Add Python to PATH"
# Verify installation
python --version
```

**macOS:**
```bash
brew install python3
python3 --version
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
python3 --version
```

### Step 2️⃣: Install MySQL

**Windows:**
- Download MySQL Community Server from mysql.com
- Run installer, set root password
- Configure MySQL as Windows Service

**macOS:**
```bash
brew install mysql
brew services start mysql
mysql -u root -p
```

**Linux:**
```bash
sudo apt-get install mysql-server
sudo mysql_secure_installation
```

### Step 3️⃣: Create Project Directory

```bash
cd Desktop
mkdir AromaLux
cd AromaLux
```

### Step 4️⃣: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 5️⃣: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Expected output: Successfully installed all packages

### Step 6️⃣: Create Database

**Method 1: Using SQL File**
```bash
mysql -u root -p < database.sql
# Enter your MySQL root password
```

**Method 2: Manual Setup**
```bash
mysql -u root -p
```

Then paste:
```sql
CREATE DATABASE aromalux;
USE aromalux;
-- (Copy entire database.sql content)
```

Verify:
```bash
mysql -u root -p -e "USE aromalux; SHOW TABLES;"
```

### Step 7️⃣: Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit .env file with your settings
# Windows: notepad .env
# macOS/Linux: nano .env
```

**Key settings in .env:**
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=aromalux
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

### Step 8️⃣: Generate Sample Data

```bash
python seed_perfumes.py
```

Wait for completion. You should see:
```
✅ Progress: 1000/1000 perfumes inserted (100%)
🎉 Database seeding completed successfully!
```

### Step 9️⃣: Run Application

```bash
python app.py
```

Expected output:
```
* Running on http://0.0.0.0:5000
* Debug mode: on
```

### Step 🔟: Access in Browser

Open your browser and navigate to:
- **Home**: http://localhost:5000
- **Shop**: http://localhost:5000/perfumes
- **Admin**: http://localhost:5000/admin (if configured)

---

## Testing the Application

### Test User Registration
1. Go to http://localhost:5000/signup
2. Create an account:
   - Email: test@example.com
   - Password: Test12345!
   - Name: Test User

### Test Shopping
1. Browse perfumes
2. Add items to cart
3. Proceed to checkout
4. Complete order

### Test Orders
1. View order history
2. Track order status
3. Download invoice

### Test Admin Functions
1. Add products
2. Manage inventory
3. View orders
4. Generate reports

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Access denied for user 'root'@'localhost'"
**Solution:**
```bash
# Reset MySQL password
mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

### Issue: "Database 'aromalux' doesn't exist"
**Solution:**
```bash
mysql -u root -p < database.sql
```

### Issue: Port 5000 already in use
**Solution:**
```bash
# Use different port
python app.py --port 5001
```

### Issue: CSS not loading properly
**Solution:**
- Clear browser cache (Ctrl+Shift+Delete)
- Restart Flask application
- Check static folder permissions

### Issue: Images not displaying
**Solution:**
```bash
# Create images folder if missing
mkdir -p static/images
```

---

## Performance Optimization

### Database
```sql
-- Add indexes
CREATE INDEX idx_perfume_search ON perfumes (perfume_name, brand_name);
CREATE INDEX idx_user_email ON users (email);
CREATE FULLTEXT INDEX ft_search ON perfumes (perfume_name, description);
```

### Flask
```python
# Enable caching in app.py
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

### JavaScript
- Minify script.js
- Lazy load images
- Defer non-critical scripts

---

## Deployment Preparation

### Before Going Live

1. **Security Checklist**
   ```bash
   # Generate secure secret key
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Environment Setup**
   ```bash
   # Create production .env
   FLASK_ENV=production
   DEBUG=False
   SECRET_KEY=your_very_secure_key_here
   ```

3. **Database Backup**
   ```bash
   mysqldump -u root -p aromalux > backup.sql
   ```

4. **SSL Certificate**
   - Get from Let's Encrypt
   - Configure with Nginx/Apache

5. **Domain Setup**
   - Point domain to server
   - Update ALLOWED_HOSTS in config

---

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Nginx (Linux)
```bash
sudo apt-get install nginx
# Configure /etc/nginx/sites-available/aromalux
sudo systemctl start nginx
```

### Using Docker
```bash
docker build -t aromalux .
docker run -p 5000:5000 aromalux
```

### Cloud Platforms

**Heroku:**
```bash
heroku login
heroku create aromalux
git push heroku main
```

**AWS:**
- Use Elastic Beanstalk
- RDS for MySQL
- CloudFront for CDN

**Azure:**
- Azure App Service
- Azure Database for MySQL

---

## Maintenance

### Regular Tasks

**Daily:**
- Monitor error logs
- Check database backups
- Verify uptime

**Weekly:**
- Review user feedback
- Check security updates
- Analyze traffic

**Monthly:**
- Database optimization
- Clean old logs
- Update dependencies
- Review performance metrics

### Database Maintenance

```bash
# Backup database
mysqldump -u root -p aromalux > backup_$(date +%Y%m%d).sql

# Optimize tables
mysql -u root -p -e "OPTIMIZE TABLE aromalux.perfumes;"

# Check integrity
mysqlcheck -u root -p aromalux
```

---

## Support & Resources

📚 **Documentation**: README.md
🔗 **GitHub Issues**: github.com/yourusername/aromalux/issues
📧 **Email Support**: support@aromalux.com
💬 **Community Forum**: forum.aromalux.com

---

## Version Information

- **AromaLux**: v1.0.0
- **Python**: 3.8+
- **Flask**: 2.3+
- **MySQL**: 8.0+
- **Last Updated**: March 2024

---

**For detailed documentation, see README.md**

Happy perfume selling! 🌟
