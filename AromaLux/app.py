"""
AromaLux - Luxury Perfume Marketplace Backend
Flask-based REST API for enterprise e-commerce platform
Production-grade implementation with security, scalability, and performance optimization
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import re
import json
import secrets
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'aromalux_secret_key_2024')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# MySQL Configuration
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'root'),
    'database': os.getenv('MYSQL_DB', 'aromalux')
}

def get_db():
    """Get database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# Create a mock mysql object for compatibility
class MockMySQL:
    def get_db(self):
        return get_db()

mysql = MockMySQL()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def api_login_required(f):
    """Decorator for API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_user_data(user_id):
    """Fetch user data from database"""
    conn = mysql.get_db()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT user_id, email, first_name, last_name, phone, gender, birth_date, profile_image
        FROM users WHERE user_id = %s
    """, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def calculate_discount_price(price, discount_percent):
    """Calculate discounted price"""
    return round(price * (1 - discount_percent / 100), 2)

def generate_order_number():
    """Generate unique order number"""
    return f"ORD-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}"

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration endpoint"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        phone = data.get('phone', '').strip()
        
        # Validation
        if not email or not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        
        if not first_name or not last_name:
            return jsonify({'error': 'First and last name required'}), 400
        
        cursor = mysql.get_db().cursor()
        
        # Check if email already exists
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        hashed_password = generate_password_hash(password)
        
        try:
            cursor.execute("""
                INSERT INTO users (email, password, first_name, last_name, phone)
                VALUES (%s, %s, %s, %s, %s)
            """, (email, hashed_password, first_name, last_name, phone))
            
            mysql.get_db().commit()
            user_id = cursor.lastrowid
            cursor.close()
            
            # Set session
            session['user_id'] = user_id
            session['email'] = email
            session.permanent = True
            
            return jsonify({'success': True, 'message': 'Account created successfully'}), 201
        
        except Exception as e:
            mysql.get_db().rollback()
            cursor.close()
            return jsonify({'error': str(e)}), 500

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login endpoint"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        cursor = mysql.get_db().cursor()
        cursor.execute("""
            SELECT user_id, password, email FROM users WHERE email = %s
        """, (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['email'] = user['email']
            session.permanent = True
            
            return jsonify({'success': True, 'message': 'Login successful'}), 200
        
        return jsonify({'error': 'Invalid email or password'}), 401

    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout endpoint"""
    session.clear()
    return redirect(url_for('home'))

# ============================================================================
# PRODUCT ROUTES
# ============================================================================

@app.route('/api/perfumes', methods=['GET'])
def get_perfumes():
    """Get perfumes with filters and search"""
    
    page = request.args.get('page', 1, type=int)
    per_page = 12
    offset = (page - 1) * per_page
    
    # Filters
    search_query = request.args.get('search', '').strip()
    category_id = request.args.get('category', 0, type=int)
    brand = request.args.get('brand', '').strip()
    fragrance_type = request.args.get('fragrance_type', '').strip()
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 10000, type=float)
    sort = request.args.get('sort', 'latest')  # latest, price_low, price_high, rating
    
    cursor = mysql.get_db().cursor()
    
    # Build query
    where_clauses = ["p.price BETWEEN %s AND %s"]
    params = [min_price, max_price]
    
    if search_query:
        where_clauses.append("(MATCH(p.perfume_name, p.brand_name, p.description) AGAINST(%s IN BOOLEAN MODE) OR p.perfume_name LIKE %s OR p.brand_name LIKE %s)")
        search_like = f"%{search_query}%"
        params.extend([search_query, search_like, search_like])
    
    if category_id > 0:
        where_clauses.append("p.category_id = %s")
        params.append(category_id)
    
    if brand:
        where_clauses.append("p.brand_name = %s")
        params.append(brand)
    
    if fragrance_type:
        where_clauses.append("p.fragrance_type = %s")
        params.append(fragrance_type)
    
    where_sql = " AND ".join(where_clauses)
    
    # Sorting
    sort_sql = "ORDER BY p.created_at DESC"
    if sort == 'price_low':
        sort_sql = "ORDER BY p.price ASC"
    elif sort == 'price_high':
        sort_sql = "ORDER BY p.price DESC"
    elif sort == 'rating':
        sort_sql = "ORDER BY p.rating DESC"
    
    # Count total
    count_query = f"SELECT COUNT(*) as total FROM perfumes p WHERE {where_sql}"
    cursor.execute(count_query, params)
    total = cursor.fetchone()['total']
    
    # Get perfumes
    query = f"""
        SELECT p.perfume_id, p.perfume_name, p.brand_name, p.price, p.discount_percent,
               p.fragrance_type, p.rating, p.review_count, p.image_url, p.stock_quantity
        FROM perfumes p
        WHERE {where_sql}
        {sort_sql}
        LIMIT %s OFFSET %s
    """
    
    params.extend([per_page, offset])
    cursor.execute(query, params)
    perfumes = cursor.fetchall()
    
    # Add discounted price
    for perfume in perfumes:
        perfume['discounted_price'] = calculate_discount_price(
            perfume['price'], 
            perfume['discount_percent']
        )
    
    cursor.close()
    
    total_pages = (total + per_page - 1) // per_page
    
    return jsonify({
        'perfumes': perfumes,
        'pagination': {
            'current_page': page,
            'total_pages': total_pages,
            'total_items': total,
            'per_page': per_page
        }
    })

@app.route('/api/perfumes/<int:perfume_id>')
def get_perfume_detail(perfume_id):
    """Get detailed perfume information"""
    
    cursor = mysql.get_db().cursor()
    
    # Get perfume
    cursor.execute("""
        SELECT * FROM perfumes WHERE perfume_id = %s
    """, (perfume_id,))
    perfume = cursor.fetchone()
    
    if not perfume:
        cursor.close()
        return jsonify({'error': 'Perfume not found'}), 404
    
    # Get reviews
    cursor.execute("""
        SELECT r.review_id, r.rating, r.review_text, r.created_at,
               u.first_name, u.last_name
        FROM reviews r
        JOIN users u ON r.user_id = u.user_id
        WHERE r.perfume_id = %s
        ORDER BY r.created_at DESC
        LIMIT 10
    """, (perfume_id,))
    reviews = cursor.fetchall()
    
    # Check if user has favorited
    is_favorited = False
    if 'user_id' in session:
        cursor.execute("""
            SELECT favorite_id FROM favorites
            WHERE user_id = %s AND perfume_id = %s
        """, (session['user_id'], perfume_id))
        is_favorited = cursor.fetchone() is not None
    
    cursor.close()
    
    perfume['discounted_price'] = calculate_discount_price(
        perfume['price'],
        perfume['discount_percent']
    )
    perfume['bottle_sizes'] = json.loads(perfume['bottle_sizes']) if perfume['bottle_sizes'] else []
    perfume['reviews'] = reviews
    perfume['is_favorited'] = is_favorited
    
    return jsonify(perfume)

@app.route('/api/categories')
def get_categories():
    """Get all fragrance categories"""
    
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT category_id, category_name, description FROM categories ORDER BY category_name")
    categories = cursor.fetchall()
    cursor.close()
    
    return jsonify(categories)

@app.route('/api/brands')
def get_brands():
    """Get all brands"""
    
    cursor = mysql.get_db().cursor()
    cursor.execute("""
        SELECT DISTINCT brand_name FROM perfumes ORDER BY brand_name
    """)
    brands = [row['brand_name'] for row in cursor.fetchall()]
    cursor.close()
    
    return jsonify(brands)

@app.route('/api/fragrance-types')
def get_fragrance_types():
    """Get all fragrance types"""
    
    cursor = mysql.get_db().cursor()
    cursor.execute("""
        SELECT DISTINCT fragrance_type FROM perfumes ORDER BY fragrance_type
    """)
    types = [row['fragrance_type'] for row in cursor.fetchall()]
    cursor.close()
    
    return jsonify(types)

# ============================================================================
# CART ROUTES
# ============================================================================

@app.route('/api/cart', methods=['GET', 'POST', 'DELETE'])
@api_login_required
def cart():
    """Manage shopping cart"""
    user_id = session['user_id']
    
    if request.method == 'GET':
        # Get cart items
        cursor = mysql.get_db().cursor()
        cursor.execute("""
            SELECT c.cart_id, c.perfume_id, c.bottle_size, c.quantity,
                   p.perfume_name, p.price, p.discount_percent, p.image_url
            FROM cart c
            JOIN perfumes p ON c.perfume_id = p.perfume_id
            WHERE c.user_id = %s
            ORDER BY c.added_at DESC
        """, (user_id,))
        cart_items = cursor.fetchall()
        cursor.close()
        
        # Calculate totals
        subtotal = 0
        for item in cart_items:
            item['discounted_price'] = calculate_discount_price(
                item['price'],
                item['discount_percent']
            )
            item['item_total'] = item['discounted_price'] * item['quantity']
            subtotal += item['item_total']
        
        tax = round(subtotal * 0.05, 2)  # 5% tax
        total = subtotal + tax
        
        return jsonify({
            'items': cart_items,
            'summary': {
                'subtotal': subtotal,
                'tax': tax,
                'total': total,
                'item_count': len(cart_items)
            }
        })
    
    elif request.method == 'POST':
        # Add to cart
        data = request.get_json()
        perfume_id = data.get('perfume_id')
        bottle_size = data.get('bottle_size', '50ml')
        quantity = data.get('quantity', 1)
        
        if not perfume_id or quantity < 1:
            return jsonify({'error': 'Invalid request'}), 400
        
        cursor = mysql.get_db().cursor()
        
        try:
            # Check if item exists in cart
            cursor.execute("""
                SELECT cart_id, quantity FROM cart
                WHERE user_id = %s AND perfume_id = %s AND bottle_size = %s
            """, (user_id, perfume_id, bottle_size))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update quantity
                new_quantity = existing['quantity'] + quantity
                cursor.execute("""
                    UPDATE cart SET quantity = %s WHERE cart_id = %s
                """, (new_quantity, existing['cart_id']))
            else:
                # Insert new item
                cursor.execute("""
                    INSERT INTO cart (user_id, perfume_id, bottle_size, quantity)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, perfume_id, bottle_size, quantity))
            
            mysql.get_db().commit()
            return jsonify({'success': True, 'message': 'Added to cart'}), 201
        
        except Exception as e:
            mysql.get_db().rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
    
    elif request.method == 'DELETE':
        # Remove from cart
        data = request.get_json()
        cart_id = data.get('cart_id')
        
        cursor = mysql.get_db().cursor()
        
        try:
            cursor.execute("""
                DELETE FROM cart WHERE cart_id = %s AND user_id = %s
            """, (cart_id, user_id))
            
            mysql.get_db().commit()
            return jsonify({'success': True, 'message': 'Removed from cart'})
        
        except Exception as e:
            mysql.get_db().rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()

@app.route('/api/cart/update', methods=['PUT'])
@api_login_required
def update_cart():
    """Update cart item quantity"""
    user_id = session['user_id']
    data = request.get_json()
    
    cart_id = data.get('cart_id')
    quantity = data.get('quantity', 1)
    
    if quantity < 1:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    cursor = mysql.get_db().cursor()
    
    try:
        cursor.execute("""
            UPDATE cart SET quantity = %s
            WHERE cart_id = %s AND user_id = %s
        """, (quantity, cart_id, user_id))
        
        mysql.get_db().commit()
        return jsonify({'success': True, 'message': 'Cart updated'})
    
    except Exception as e:
        mysql.get_db().rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

# ============================================================================
# FAVORITES ROUTE
# ============================================================================

@app.route('/api/favorites/<int:perfume_id>', methods=['POST', 'DELETE'])
@api_login_required
def manage_favorites(perfume_id):
    """Add/remove from favorites"""
    user_id = session['user_id']
    cursor = mysql.get_db().cursor()
    
    try:
        if request.method == 'POST':
            cursor.execute("""
                INSERT IGNORE INTO favorites (user_id, perfume_id)
                VALUES (%s, %s)
            """, (user_id, perfume_id))
            mysql.get_db().commit()
            return jsonify({'success': True, 'message': 'Added to favorites'})
        
        elif request.method == 'DELETE':
            cursor.execute("""
                DELETE FROM favorites WHERE user_id = %s AND perfume_id = %s
            """, (user_id, perfume_id))
            mysql.get_db().commit()
            return jsonify({'success': True, 'message': 'Removed from favorites'})
    
    except Exception as e:
        mysql.get_db().rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/api/favorites')
@api_login_required
def get_favorites():
    """Get user's favorite perfumes"""
    user_id = session['user_id']
    
    cursor = mysql.get_db().cursor()
    cursor.execute("""
        SELECT p.perfume_id, p.perfume_name, p.brand_name, p.price,
               p.discount_percent, p.rating, p.image_url
        FROM favorites f
        JOIN perfumes p ON f.perfume_id = p.perfume_id
        WHERE f.user_id = %s
        ORDER BY f.created_at DESC
    """, (user_id,))
    favorites = cursor.fetchall()
    cursor.close()
    
    for fav in favorites:
        fav['discounted_price'] = calculate_discount_price(fav['price'], fav['discount_percent'])
    
    return jsonify(favorites)

# ============================================================================
# ORDERS ROUTES
# ============================================================================

@app.route('/api/orders', methods=['POST'])
@api_login_required
def create_order():
    """Create new order from cart"""
    user_id = session['user_id']
    data = request.get_json()
    
    payment_method = data.get('payment_method')
    shipping_address_id = data.get('shipping_address_id')
    
    if not payment_method or not shipping_address_id:
        return jsonify({'error': 'Payment method and shipping address required'}), 400
    
    cursor = mysql.get_db().cursor()
    
    try:
        # Get cart items
        cursor.execute("""
            SELECT c.perfume_id, c.quantity, c.bottle_size, p.price, p.discount_percent
            FROM cart c
            JOIN perfumes p ON c.perfume_id = p.perfume_id
            WHERE c.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate totals
        subtotal = 0
        for item in cart_items:
            discounted_price = calculate_discount_price(item['price'], item['discount_percent'])
            subtotal += discounted_price * item['quantity']
        
        tax = round(subtotal * 0.05, 2)
        shipping = 10.0
        final_price = subtotal + tax + shipping
        
        # Create order
        order_number = generate_order_number()
        cursor.execute("""
            INSERT INTO orders 
            (user_id, order_number, total_price, tax_amount, shipping_cost,
             final_price, payment_method, shipping_address_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, order_number, subtotal, tax, shipping, final_price,
              payment_method, shipping_address_id))
        
        order_id = cursor.lastrowid
        
        # Add order items
        for item in cart_items:
            discounted_price = calculate_discount_price(item['price'], item['discount_percent'])
            cursor.execute("""
                INSERT INTO order_items 
                (order_id, perfume_id, quantity, bottle_size, unit_price, subtotal)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (order_id, item['perfume_id'], item['quantity'], item['bottle_size'],
                  discounted_price, discounted_price * item['quantity']))
        
        # Clear cart
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        
        mysql.get_db().commit()
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'order_number': order_number,
            'total_price': final_price
        }), 201
    
    except Exception as e:
        mysql.get_db().rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/api/orders')
@api_login_required
def get_orders():
    """Get user's orders"""
    user_id = session['user_id']
    
    cursor = mysql.get_db().cursor()
    cursor.execute("""
        SELECT order_id, order_number, final_price, order_status, 
               payment_status, created_at, estimated_delivery
        FROM orders
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))
    orders = cursor.fetchall()
    cursor.close()
    
    return jsonify(orders)

@app.route('/api/orders/<int:order_id>')
@api_login_required
def get_order_detail(order_id):
    """Get order details"""
    user_id = session['user_id']
    
    cursor = mysql.get_db().cursor()
    
    # Get order
    cursor.execute("""
        SELECT * FROM orders WHERE order_id = %s AND user_id = %s
    """, (order_id, user_id))
    order = cursor.fetchone()
    
    if not order:
        cursor.close()
        return jsonify({'error': 'Order not found'}), 404
    
    # Get order items
    cursor.execute("""
        SELECT oi.order_item_id, oi.perfume_id, oi.quantity, oi.bottle_size,
               oi.unit_price, oi.subtotal, p.perfume_name, p.brand_name, p.image_url
        FROM order_items oi
        JOIN perfumes p ON oi.perfume_id = p.perfume_id
        WHERE oi.order_id = %s
    """, (order_id,))
    items = cursor.fetchall()
    
    cursor.close()
    
    order['items'] = items
    return jsonify(order)

# ============================================================================
# BLOG ROUTES
# ============================================================================

@app.route('/api/blogs')
def get_blogs():
    """Get all blog posts"""
    cursor = mysql.get_db().cursor()
    cursor.execute("""
        SELECT blog_id, title, slug, short_description, featured_image,
               author, created_at, views
        FROM blog_posts
        WHERE is_published = TRUE
        ORDER BY created_at DESC
    """)
    blogs = cursor.fetchall()
    cursor.close()
    
    return jsonify(blogs)

@app.route('/api/blogs/<slug>')
def get_blog_detail(slug):
    """Get blog post details"""
    cursor = mysql.get_db().cursor()
    cursor.execute("""
        SELECT * FROM blog_posts WHERE slug = %s AND is_published = TRUE
    """, (slug,))
    blog = cursor.fetchone()
    
    if not blog:
        cursor.close()
        return jsonify({'error': 'Blog not found'}), 404
    
    # Increment views
    cursor.execute("""
        UPDATE blog_posts SET views = views + 1 WHERE blog_id = %s
    """, (blog['blog_id'],))
    
    mysql.get_db().commit()
    cursor.close()
    
    return jsonify(blog)

# ============================================================================
# USER PROFILE ROUTES
# ============================================================================

@app.route('/api/profile')
@api_login_required
def get_profile():
    """Get user profile"""
    user_id = session['user_id']
    user = get_user_data(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user)

@app.route('/api/profile', methods=['PUT'])
@api_login_required
def update_profile():
    """Update user profile"""
    user_id = session['user_id']
    data = request.get_json()
    
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    phone = data.get('phone', '').strip()
    birth_date = data.get('birth_date')
    gender = data.get('gender')
    
    cursor = mysql.get_db().cursor()
    
    try:
        cursor.execute("""
            UPDATE users
            SET first_name = %s, last_name = %s, phone = %s,
                birth_date = %s, gender = %s
            WHERE user_id = %s
        """, (first_name, last_name, phone, birth_date, gender, user_id))
        
        mysql.get_db().commit()
        return jsonify({'success': True, 'message': 'Profile updated'})
    
    except Exception as e:
        mysql.get_db().rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/api/addresses')
@api_login_required
def get_addresses():
    """Get user's addresses"""
    user_id = session['user_id']
    
    cursor = mysql.get_db().cursor()
    cursor.execute("""
        SELECT * FROM addresses WHERE user_id = %s ORDER BY is_default DESC
    """, (user_id,))
    addresses = cursor.fetchall()
    cursor.close()
    
    return jsonify(addresses)

@app.route('/api/addresses', methods=['POST'])
@api_login_required
def add_address():
    """Add new address"""
    user_id = session['user_id']
    data = request.get_json()
    
    cursor = mysql.get_db().cursor()
    
    try:
        cursor.execute("""
            INSERT INTO addresses
            (user_id, address_type, street_address, city, state,
             postal_code, country, is_default)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, data.get('address_type'), data.get('street_address'),
              data.get('city'), data.get('state'), data.get('postal_code'),
              data.get('country'), data.get('is_default', False)))
        
        mysql.get_db().commit()
        return jsonify({'success': True, 'message': 'Address added'}), 201
    
    except Exception as e:
        mysql.get_db().rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

# ============================================================================
# FRAGRANCE RECOMMENDATION SYSTEM (AI-based)
# ============================================================================

@app.route('/api/recommendation/quiz', methods=['POST'])
def fragrance_quiz():
    """Get fragrance recommendations based on quiz"""
    data = request.get_json()
    
    preference_type = data.get('preference_type')  # male, female, unisex
    fragrance_families = data.get('fragrance_families', [])  # floral, woody, citrus, oriental
    occasions = data.get('occasions', [])
    price_range = data.get('price_range', 'medium')
    skin_type = data.get('skin_type')
    
    cursor = mysql.get_db().cursor()
    
    try:
        # Build recommendation query
        where_parts = []
        
        # Category preference
        category_map = {
            'male': 1,
            'female': 2,
            'unisex': 3
        }
        if preference_type and preference_type in category_map:
            where_parts.append(f"category_id = {category_map[preference_type]}")
        
        # Price range
        price_ranges = {
            'budget': (0, 50),
            'medium': (50, 150),
            'luxury': (150, 350),
            'premium': (350, 10000)
        }
        if price_range in price_ranges:
            min_p, max_p = price_ranges[price_range]
            where_parts.append(f"price BETWEEN {min_p} AND {max_p}")
        
        # Fragrance families
        if fragrance_families:
            family_filter = " OR ".join([f"fragrance_type LIKE '%{f}%'" for f in fragrance_families])
            where_parts.append(f"({family_filter})")
        
        where_sql = " AND ".join(where_parts) if where_parts else "1=1"
        
        # Get recommendations
        query = f"""
            SELECT perfume_id, perfume_name, brand_name, price, discount_percent,
                   fragrance_type, rating, review_count, image_url
            FROM perfumes
            WHERE {where_sql}
            ORDER BY rating DESC, review_count DESC
            LIMIT 12
        """
        
        cursor.execute(query)
        recommendations = cursor.fetchall()
        
        for rec in recommendations:
            rec['discounted_price'] = calculate_discount_price(rec['price'], rec['discount_percent'])
        
        return jsonify({
            'recommendations': recommendations,
            'count': len(recommendations)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/api/recommendation/similar/<int:perfume_id>')
def get_similar_perfumes(perfume_id):
    """Get similar perfume recommendations"""
    
    cursor = mysql.get_db().cursor()
    
    # Get original perfume
    cursor.execute("""
        SELECT category_id, fragrance_type, price FROM perfumes
        WHERE perfume_id = %s
    """, (perfume_id,))
    perfume = cursor.fetchone()
    
    if not perfume:
        cursor.close()
        return jsonify({'error': 'Perfume not found'}), 404
    
    # Get similar perfumes
    cursor.execute("""
        SELECT perfume_id, perfume_name, brand_name, price, discount_percent,
               fragrance_type, rating, review_count, image_url
        FROM perfumes
        WHERE perfume_id != %s
        AND (category_id = %s OR fragrance_type = %s)
        AND price BETWEEN %s AND %s
        ORDER BY rating DESC, review_count DESC
        LIMIT 6
    """, (perfume_id, perfume['category_id'], perfume['fragrance_type'],
          perfume['price'] * 0.8, perfume['price'] * 1.2))
    
    similar = cursor.fetchall()
    
    for sim in similar:
        sim['discounted_price'] = calculate_discount_price(sim['price'], sim['discount_percent'])
    
    cursor.close()
    
    return jsonify(similar)

# ============================================================================
# PAGE ROUTES
# ============================================================================

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/perfumes')
def perfumes():
    return render_template('perfumes.html')

@app.route('/perfume/<int:perfume_id>')
def perfume_detail(perfume_id):
    return render_template('perfume-details.html', perfume_id=perfume_id)

@app.route('/collections')
def collections():
    return render_template('collections.html')

@app.route('/offers')
def offers():
    return render_template('offers.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

@app.route('/blog/<slug>')
def blog_detail(slug):
    return render_template('blog-detail.html', slug=slug)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/cart')
def cart_page():
    return render_template('cart.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/orders')
@login_required
def orders():
    return render_template('orders.html')

# ============================================================================
# CLASSIFICATION ROUTES (26 Fragrance Types)
# ============================================================================

@app.route('/classifications')
def classifications():
    return render_template('classifications.html')

@app.route('/classification/<classification>')
def classification_page(classification):
    classifications_list = [
        'floral', 'fresh', 'spicy', 'vanilla', 'powdery', 'sweet', 'fruity', 
        'tropical', 'soft', 'citrus', 'musky', 'woody', 'leather', 'green', 
        'aromatic', 'patchouli', 'amber', 'oud', 'animalic', 'tobacco', 
        'aquatic', 'oriental', 'light', 'boozy', 'coffee', 'chypre'
    ]
    if classification.lower() not in classifications_list:
        return render_template('404.html'), 404
    return render_template(f'{classification.lower()}.html', classification=classification)

@app.route('/api/classifications/<classification>', methods=['GET'])
def get_classification_products(classification):
    """Get products for a specific classification with gender filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        gender = request.args.get('gender', 'all', type=str)
        sort = request.args.get('sort', 'latest', type=str)
        limit = 20
        offset = (page - 1) * limit
        
        cursor = mysql.get_db().cursor()
        
        # Build query based on gender filter
        where_clause = "p.classification = %s"
        params = [classification.lower()]
        
        if gender != 'all' and gender in ['male', 'female', 'unisex']:
            where_clause += " AND p.gender IN (%s, 'unisex')"
            params.append(gender)
        
        # Sorting options
        sort_map = {
            'latest': 'p.created_at DESC',
            'price_low': 'p.price ASC',
            'price_high': 'p.price DESC',
            'rating': 'p.rating DESC',
            'featured': 'p.is_featured DESC'
        }
        order_by = sort_map.get(sort, 'p.created_at DESC')
        
        # Get total count
        count_query = f"SELECT COUNT(*) as total FROM perfumes p WHERE {where_clause}"
        cursor.execute(count_query, params)
        total = cursor.fetchone()['total']
        
        # Get products
        query = f"""
            SELECT p.perfume_id, p.perfume_name, p.brand_name, p.price, 
                   p.discount_percent, p.rating, p.review_count, p.gender,
                   p.classification, p.image_url, p.is_featured, p.is_new
            FROM perfumes p
            WHERE {where_clause}
            ORDER BY {order_by}
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        cursor.execute(query, params)
        products = cursor.fetchall()
        cursor.close()
        
        # Calculate discounted prices
        for product in products:
            original_price = float(product['price'])
            discount = float(product['discount_percent'])
            product['discounted_price'] = round(original_price * (1 - discount / 100), 2)
        
        return jsonify({
            'products': products,
            'pagination': {
                'page': page,
                'total': total,
                'pages': (total + limit - 1) // limit,
                'limit': limit
            }
        })
    except Exception as e:
        print(f"Error fetching classification products: {str(e)}")
        return jsonify({'error': 'Failed to fetch products'}), 500

@app.route('/api/classifications', methods=['GET'])
def get_all_classifications():
    """Get all available classifications"""
    classifications = [
        {'name': 'Floral', 'slug': 'floral', 'count': 100},
        {'name': 'Fresh', 'slug': 'fresh', 'count': 100},
        {'name': 'Spicy', 'slug': 'spicy', 'count': 100},
        {'name': 'Vanilla', 'slug': 'vanilla', 'count': 100},
        {'name': 'Powdery', 'slug': 'powdery', 'count': 100},
        {'name': 'Sweet', 'slug': 'sweet', 'count': 100},
        {'name': 'Fruity', 'slug': 'fruity', 'count': 100},
        {'name': 'Tropical', 'slug': 'tropical', 'count': 100},
        {'name': 'Soft', 'slug': 'soft', 'count': 100},
        {'name': 'Citrus', 'slug': 'citrus', 'count': 100},
        {'name': 'Musky', 'slug': 'musky', 'count': 100},
        {'name': 'Woody', 'slug': 'woody', 'count': 100},
        {'name': 'Leather', 'slug': 'leather', 'count': 100},
        {'name': 'Green', 'slug': 'green', 'count': 100},
        {'name': 'Aromatic', 'slug': 'aromatic', 'count': 100},
        {'name': 'Patchouli', 'slug': 'patchouli', 'count': 100},
        {'name': 'Amber', 'slug': 'amber', 'count': 100},
        {'name': 'Oud', 'slug': 'oud', 'count': 100},
        {'name': 'Animalic', 'slug': 'animalic', 'count': 100},
        {'name': 'Tobacco', 'slug': 'tobacco', 'count': 100},
        {'name': 'Aquatic', 'slug': 'aquatic', 'count': 100},
        {'name': 'Oriental', 'slug': 'oriental', 'count': 100},
        {'name': 'Light', 'slug': 'light', 'count': 100},
        {'name': 'Boozy', 'slug': 'boozy', 'count': 100},
        {'name': 'Coffee', 'slug': 'coffee', 'count': 100},
        {'name': 'Chypre', 'slug': 'chypre', 'count': 100}
    ]
    
    try:
        cursor = mysql.get_db().cursor()
        for classification in classifications:
            cursor.execute(
                "SELECT COUNT(*) as count FROM perfumes WHERE classification = %s",
                [classification['slug']]
            )
            result = cursor.fetchone()
            if result:
                classification['count'] = result['count']
        cursor.close()
    except:
        pass
    
    return jsonify(classifications)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
