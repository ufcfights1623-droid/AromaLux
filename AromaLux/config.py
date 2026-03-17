# AromaLux Configuration
# Production configuration file

DEBUG = False
TESTING = False
ENVIRONMENT = "production"

# Database Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "aromalux"
DB_PORT = 3306

# Session Configuration
PERMANENT_SESSION_LIFETIME = 604800  # 7 days
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# Security
SECRET_KEY = "change_this_to_a_secure_random_key_in_production"
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file upload

# Application Settings
APP_NAME = "AromaLux"
APP_VERSION = "1.0.0"
ITEMS_PER_PAGE = 12
TIMEZONE = "UTC"

# Email Configuration (optional)
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "your_email@gmail.com"
MAIL_PASSWORD = "your_app_password"
DEFAULT_MAIL_SENDER = "noreply@aromalux.com"

# Payment Gateway Settings
STRIPE_PUBLIC_KEY = "pk_test_..."
STRIPE_SECRET_KEY = "sk_test_..."
PAYPAL_CLIENT_ID = "..."
PAYPAL_CLIENT_SECRET = "..."

# Feature Flags
ENABLE_RECOMMENDATIONS = True
ENABLE_REVIEWS = True
ENABLE_WISHLIST = True
ENABLE_COUPON = True
ENABLE_SHIPPING_TRACKING = True

# API Settings
API_RATE_LIMIT = 100
API_RATE_LIMIT_WINDOW = 3600

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/aromalux.log"
LOG_MAX_BYTES = 10485760  # 10MB
LOG_BACKUP_COUNT = 5

# Cache
CACHE_TYPE = "simple"  # Use "redis" for production
CACHE_DEFAULT_TIMEOUT = 300

# Currency & Locale
CURRENCY = "USD"
CURRENCY_SYMBOL = "$"
DEFAULT_LANGUAGE = "en"

# Pagination
PAGINATION_PER_PAGE = 12

# Upload Settings
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}

# Third-party Services
GOOGLE_ANALYTICS_ID = "UA-XXXXXXXXX-X"
SENTRY_DSN = ""

# Timezone Settings
TIMEZONE = "UTC"
DATE_FORMAT = "MM/DD/YYYY"
TIME_FORMAT = "HH:MM:SS"
