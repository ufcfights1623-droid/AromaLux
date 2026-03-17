-- AromaLux Luxury Perfume Marketplace Database
-- Production-grade schema for enterprise e-commerce platform

CREATE DATABASE IF NOT EXISTS aromalux;
USE aromalux;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    profile_image VARCHAR(255),
    birth_date DATE,
    gender ENUM('male', 'female', 'other'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Addresses Table
CREATE TABLE IF NOT EXISTS addresses (
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    address_type ENUM('shipping', 'billing', 'both') DEFAULT 'shipping',
    street_address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Perfume Categories Table
CREATE TABLE IF NOT EXISTS categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Perfume Products Table
CREATE TABLE IF NOT EXISTS perfumes (
    perfume_id INT PRIMARY KEY AUTO_INCREMENT,
    perfume_name VARCHAR(255) NOT NULL,
    brand_name VARCHAR(100) NOT NULL,
    category_id INT NOT NULL,
    fragrance_type VARCHAR(100),
    classification VARCHAR(100),
    gender ENUM('male', 'female', 'unisex') DEFAULT 'unisex',
    description TEXT,
    top_notes TEXT,
    middle_notes TEXT,
    base_notes TEXT,
    price DECIMAL(10, 2) NOT NULL,
    discount_percent DECIMAL(5, 2) DEFAULT 0,
    bottle_sizes VARCHAR(255),
    stock_quantity INT DEFAULT 0,
    rating DECIMAL(3, 2) DEFAULT 0,
    review_count INT DEFAULT 0,
    image_url VARCHAR(255),
    is_featured BOOLEAN DEFAULT FALSE,
    is_new BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    INDEX idx_brand (brand_name),
    INDEX idx_category (category_id),
    INDEX idx_price (price),
    INDEX idx_classification (classification),
    INDEX idx_gender (gender),
    FULLTEXT INDEX ft_search (perfume_name, brand_name, description)
);

-- Reviews Table
CREATE TABLE IF NOT EXISTS reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    perfume_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (perfume_id) REFERENCES perfumes(perfume_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Favorites Table
CREATE TABLE IF NOT EXISTS favorites (
    favorite_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    perfume_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (perfume_id) REFERENCES perfumes(perfume_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_perfume (user_id, perfume_id)
);

-- Shopping Cart Table
CREATE TABLE IF NOT EXISTS cart (
    cart_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    perfume_id INT NOT NULL,
    bottle_size VARCHAR(20) DEFAULT '50ml',
    quantity INT NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (perfume_id) REFERENCES perfumes(perfume_id) ON DELETE CASCADE,
    UNIQUE KEY unique_cart_item (user_id, perfume_id, bottle_size)
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    total_price DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    tax_amount DECIMAL(10, 2) DEFAULT 0,
    shipping_cost DECIMAL(10, 2) DEFAULT 0,
    final_price DECIMAL(10, 2) NOT NULL,
    order_status ENUM('pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    payment_method ENUM('credit_card', 'debit_card', 'paypal', 'stripe', 'cash_on_delivery') NOT NULL,
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    shipping_address_id INT NOT NULL,
    tracking_number VARCHAR(100),
    estimated_delivery DATE,
    shipped_date DATETIME,
    delivered_date DATETIME,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (shipping_address_id) REFERENCES addresses(address_id),
    INDEX idx_user (user_id),
    INDEX idx_status (order_status),
    INDEX idx_created (created_at)
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    perfume_id INT NOT NULL,
    quantity INT NOT NULL,
    bottle_size VARCHAR(20),
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (perfume_id) REFERENCES perfumes(perfume_id)
);

-- Blog Posts Table
CREATE TABLE IF NOT EXISTS blog_posts (
    blog_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    short_description TEXT,
    full_content LONGTEXT NOT NULL,
    featured_image VARCHAR(255),
    author VARCHAR(100) DEFAULT 'AromaLux',
    category VARCHAR(100),
    tags VARCHAR(255),
    views INT DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- User Preferences (for AI recommendations)
CREATE TABLE IF NOT EXISTS user_preferences (
    preference_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    preferred_fragrance_types TEXT,
    preferred_notes TEXT,
    price_range_min DECIMAL(10, 2),
    price_range_max DECIMAL(10, 2),
    skin_type VARCHAR(50),
    climate_preference VARCHAR(50),
    occasion VARCHAR(100),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Coupons/Discount Codes Table
CREATE TABLE IF NOT EXISTS coupons (
    coupon_id INT PRIMARY KEY AUTO_INCREMENT,
    coupon_code VARCHAR(50) NOT NULL UNIQUE,
    discount_type ENUM('percentage', 'fixed_amount') NOT NULL,
    discount_value DECIMAL(10, 2) NOT NULL,
    min_purchase DECIMAL(10, 2) DEFAULT 0,
    max_usage INT DEFAULT -1,
    current_usage INT DEFAULT 0,
    expiry_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Default Categories
INSERT INTO categories (category_name, description) VALUES
('Men\'s Perfumes', 'Premium fragrances designed for men'),
('Women\'s Perfumes', 'Elegant fragrances designed for women'),
('Unisex Fragrances', 'Versatile fragrances for everyone'),
('Luxury Designer Perfumes', 'High-end luxury brand fragrances'),
('Arabic Oud Perfumes', 'Traditional Arabic and oud-based fragrances'),
('Floral Fragrances', 'Delicate floral-based fragrances'),
('Woody Fragrances', 'Rich woody and earthy fragrances'),
('Fresh Citrus Perfumes', 'Bright and refreshing citrus fragrances'),
('Oriental Fragrances', 'Warm and sensual oriental fragrances'),
('Limited Edition Perfumes', 'Exclusive limited edition collections');

-- Insert Sample Blog Posts
INSERT INTO blog_posts (title, slug, short_description, full_content, featured_image, category) VALUES
('How to Choose the Perfect Perfume', 'how-to-choose-perfect-perfume', 
'Discover the essential guide to finding your signature scent',
'<h2>Finding Your Signature Scent</h2><p>Choosing the perfect perfume is a personal journey that requires understanding your preferences and the characteristics of different fragrances. Start by exploring the fragrance families...</p><h3>Key Factors to Consider</h3><ul><li>Your skin type and pH level</li><li>Your lifestyle and daily activities</li><li>Your preferred fragrance families</li><li>Season and climate</li><li>Budget considerations</li></ul>',
'/static/images/blog1.jpg', 'Fragrance Tips'),

('Top Luxury Perfume Brands', 'top-luxury-perfume-brands',
'Explore the most prestigious fragrance houses in the world',
'<h2>Luxury Fragrance Houses</h2><p>The world of luxury perfumes is dominated by prestigious houses known for their craftsmanship, heritage, and innovation...</p>',
'/static/images/blog2.jpg', 'Luxury Brands'),

('Best Perfumes for Men', 'best-perfumes-for-men',
'Curated selection of the finest masculine fragrances',
'<h2>Masculine Fragrances</h2><p>Men\'s perfumes come in various styles, from fresh citrus to deep woody and spicy fragrances...</p>',
'/static/images/blog3.jpg', 'For Men'),

('Best Perfumes for Women', 'best-perfumes-for-women',
'Discover the most elegant and sophisticated fragrances for women',
'<h2>Feminine Elegance</h2><p>Women\'s fragrances showcase the full spectrum of scent possibilities, from light florals to deep orientals...</p>',
'/static/images/blog4.jpg', 'For Women'),

('Understanding Fragrance Notes', 'understanding-fragrance-notes',
'Learn the science behind top, middle, and base notes',
'<h2>The Structure of Perfume</h2><p>Every perfume is composed of three layers of fragrance notes that create a complete olfactory experience...</p>',
'/static/images/blog5.jpg', 'Education'),

('How to Make Your Perfume Last Longer', 'make-perfume-last-longer',
'Expert tips to maximize fragrance longevity and sillage',
'<h2>Extending Your Fragrance</h2><p>Understanding how to apply perfume correctly can significantly extend its longevity and impact...</p>',
'/static/images/blog6.jpg', 'Tips & Tricks');
