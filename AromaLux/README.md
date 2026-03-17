# 🌟 AromaLux - Luxury Perfume Marketplace

A production-ready, full-stack e-commerce platform for luxury fragrance shopping. Built with Flask, MySQL, HTML5, CSS3, and JavaScript.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Features](#detailed-features)

## ✨ Features

### E-Commerce Core
- 🛍️ **Product Catalog**: 1000+ luxury perfumes with advanced filtering
- 🔍 **Smart Search**: Full-text search with category, brand, and price filtering
- 🛒 **Shopping Cart**: Add, remove, and update items in real-time
- 💳 **Multiple Payment Options**: Credit/Debit cards, PayPal, Stripe, Cash on Delivery
- 📦 **Order Management**: Track orders, view history, and manage shipments

### User Management
- 👤 **User Accounts**: Secure registration and authentication
- 📋 **Profile Management**: Edit personal information and preferences
- ❤️ **Favorites**: Save and manage favorite perfumes
- 📍 **Address Management**: Multiple shipping and billing addresses
- 📊 **Order History**: View past purchases and tracking

### Product Features
- 🎨 **Detailed Perfume Information**: Notes, descriptions, prices, ratings
- ⭐ **Reviews & Ratings**: Customer reviews with authentic ratings
- 💰 **Dynamic Discounts**: Real-time discount calculation
- 🏷️ **Multiple Bottle Sizes**: 30ml, 50ml, 100ml, 150ml options

### Advanced Features
- 🤖 **AI Fragrance Recommendations**: Quiz-based fragrance suggestions
- 🔗 **Similar Products**: Smart recommendation engine
- 📰 **Blog System**: Fragrance guides and expert articles
- 🌙 **Dark Mode**: Luxury dark theme support
- 📱 **Fully Responsive**: Mobile, tablet, and desktop optimization

### UI/UX Design
- ✨ **Glassmorphism Cards**: Modern frosted glass effect
- 🎯 **Smooth Animations**: Delightful page transitions
- 🌈 **Luxury Color Scheme**: Magenta, Black, Purple, Soft Pink
- ♿ **Accessibility**: WCAG 2.1 AA compliant

## 🛠 Tech Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Advanced styling with animations, flexbox, grid
- **JavaScript (ES6+)**: AJAX, DOM manipulation, client-side logic

### Backend
- **Python 3.8+**: Server-side logic
- **Flask 2.3+**: Lightweight web framework
- **Flask-MySQLdb**: Database integration
- **Werkzeug**: Security utilities

### Database
- **MySQL 8.0+**: Relational database
- **SQLAlchemy** (optional): ORM support

### Development Tools
- **Faker**: Realistic data generation
- **python-dotenv**: Environment configuration
- **Flask-CORS**: Cross-origin resource sharing

## 📁 Project Structure

```
AromaLux/
├── static/
│   ├── style.css              # Main stylesheet (luxury theme)
│   ├── script.js              # Client-side functionality
│   └── images/                # Product images
├── templates/
│   ├── home.html              # Homepage
│   ├── perfumes.html          # Product listing
│   ├── perfume-details.html   # Product detail page
│   ├── cart.html              # Shopping cart
│   ├── checkout.html          # Checkout page
│   ├── login.html             # Login page
│   ├── signup.html            # Registration page
│   ├── profile.html           # User profile
│   ├── orders.html            # Order history
│   ├── blogs.html             # Blog listing
│   ├── blog-detail.html       # Blog post
│   ├── collections.html       # Product collections
│   ├── offers.html            # Special offers
│   ├── about.html             # About page
│   ├── contact.html           # Contact page
│   ├── 404.html               # Error page
│   └── 500.html               # Server error page
├── app.py                     # Main Flask application
├── database.sql               # Database schema
├── seed_perfumes.py           # Data generation script
├── requirements.txt           # Python dependencies
├── .env.example               # Environment configuration
└── README.md                  # Documentation
```

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/aromalux.git
cd AromaLux
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🗄️ Database Setup

### Step 1: Create Database
```bash
# Connect to MySQL
mysql -u root -p

# Run the SQL script
mysql -u root -p < database.sql
```

### Step 2: Seed Sample Data
```bash
python seed_perfumes.py
```

This generates 1000 realistic perfume products using Faker library.

## 🚀 Running the Application

### Development Mode
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

### Production Mode
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔌 API Endpoints

### Authentication
- `POST /signup` - Register new user
- `POST /login` - User login
- `GET /logout` - User logout

### Products
- `GET /api/perfumes` - Get paginated perfumes with filters
- `GET /api/perfumes/<id>` - Get perfume details
- `GET /api/categories` - Get all categories
- `GET /api/brands` - Get all brands
- `GET /api/fragrance-types` - Get fragrance types

### Cart Management
- `GET /api/cart` - Get cart items (requires login)
- `POST /api/cart` - Add item to cart
- `PUT /api/cart/update` - Update quantity
- `DELETE /api/cart` - Remove from cart

### Favorites
- `GET /api/favorites` - Get favorite perfumes
- `POST /api/favorites/<id>` - Add to favorites
- `DELETE /api/favorites/<id>` - Remove from favorites

### Orders
- `POST /api/orders` - Create new order
- `GET /api/orders` - Get user's orders
- `GET /api/orders/<id>` - Get order details

### User Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile
- `GET /api/addresses` - Get user addresses
- `POST /api/addresses` - Add new address

### Recommendations
- `POST /api/recommendation/quiz` - Get recommendations from quiz
- `GET /api/recommendation/similar/<id>` - Get similar perfumes

### Blog
- `GET /api/blogs` - Get all blog posts
- `GET /api/blogs/<slug>` - Get blog post details

## 🎯 Detailed Features

### Smart Search & Filtering
- Full-text search on product names, brands, descriptions
- Filter by category, brand, fragrance type
- Price range filtering with dynamic sliders
- Multiple sort options: latest, price, rating
- Real-time pagination

### Fragrance Recommendation System
- Quiz-based recommendations
- User preference matching
- Similar product suggestions
- Smart filtering by fragrance family

### Security Features
- Password hashing with Werkzeug
- SQL injection prevention
- CSRF protection
- Session management
- Input validation

### Performance Optimization
- Database indexing
- Full-text search indexes
- Lazy loading
- CSS/JS minification
- Image optimization

## 🎨 Customization

### Changing Colors
Edit CSS variables in `static/style.css`:
```css
--primary-color: #E84B8A;      /* Magenta */
--secondary-color: #000000;    /* Black */
--accent-color: #8B5CF6;       /* Purple */
--highlight-color: #FFB6E1;    /* Soft Pink */
```

### Adding New Categories
Insert into database:
```sql
INSERT INTO categories (category_name, description) 
VALUES ('New Category', 'Description');
```

### Customizing Fragrance Data
Modify `seed_perfumes.py` to adjust:
- Brand names
- Fragrance types
- Notes
- Price ranges
- Stock quantities

## 📊 Database Schema

### Key Tables
- **users**: User accounts and profiles
- **perfumes**: Product catalog (1000+ items)
- **cart**: Shopping cart items
- **orders**: Customer orders
- **order_items**: Order line items
- **reviews**: Product reviews
- **favorites**: Saved perfumes
- **blog_posts**: Blog articles
- **categories**: Product categories
- **addresses**: Shipping/billing addresses

## 🔐 Security Best Practices

✅ Password hashing with salt
✅ SQL injection protection
✅ XSS prevention
✅ CSRF tokens
✅ Secure session cookies
✅ Input validation
✅ Rate limiting ready
✅ HTTPS ready

## 📱 Responsive Design

- **Mobile (320px+)**: Optimized touch targets, single column layout
- **Tablet (768px+)**: Two-column layout, optimized spacing
- **Desktop (1200px+)**: Full multi-column layout, enhanced features

## 🚀 Deployment

### Heroku
```bash
heroku create aromalux
git push heroku main
heroku config:set MYSQL_HOST=your_db_host
```

### Docker
```bash
docker build -t aromalux .
docker run -p 5000:5000 aromalux
```

### AWS/Azure
Use RDS for MySQL, App Service/Elastic Beanstalk for Flask

## 📝 API Documentation

Full API documentation with examples available in `/api/docs` (when deployed)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Support

For support, email support@aromalux.com or open an issue in the repository.

## 🌐 Live Demo

Visit [AromaLux Demo](https://aromalux-demo.herokuapp.com) (when deployed)

---

**Built with ❤️ for luxury fragrance enthusiasts worldwide.**

Last Updated: March 2024
Version: 1.0.0 Production Ready
