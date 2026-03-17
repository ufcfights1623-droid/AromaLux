"""
AromaLux Perfume Database Seeder
Generates 1000+ realistic luxury perfume products using Faker library
Production-grade data generation for e-commerce platform
"""

import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta
import json

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  # Change as needed
    'database': 'aromalux'
}

# Fragrance Data
BRANDS = [
    'Chanel', 'Dior', 'Guerlain', 'Hermès', 'Lancôme', 'Yves Saint Laurent',
    'Tom Ford', 'Creed', 'Heeley', 'Xerjoff', 'Givenchy', 'Versace',
    'Prada', 'Burberry', 'Calvin Klein', 'Armani', 'Hugo Boss', 'Davidoff',
    'Montblanc', 'Cartier', 'Bulgari', 'Chopard', 'Van Cleef & Arpels',
    'Penhaligon\'s', 'Acqua di Parma', 'Olfactory Art', 'L\'Artisan Parfumeur',
    'Maison Margiela', 'Serge Lutens', 'Niche Fragrances Co', 'Frederic Malle',
    'Eros', 'Poison', 'Obsession', 'Scandal', 'La Vie Est Belle', 'Hypnotic Poison',
    'Miss Dior', 'Allure', 'Black Opium', 'Sauvage', 'Bleu de Chanel', 'Acqua di Gioia'
]

FRAGRANCE_TYPES = [
    'Eau de Parfum', 'Eau de Toilette', 'Eau de Cologne', 'Fragrance Oil',
    'Extrait de Parfum', 'Eau Fraîche', 'Perfume Spray', 'Concentrated Perfume'
]

# Classification/Fragrance Families (26 types)
CLASSIFICATIONS = [
    'floral', 'fresh', 'spicy', 'vanilla', 'powdery', 'sweet', 'fruity',
    'tropical', 'soft', 'citrus', 'musky', 'woody', 'leather', 'green',
    'aromatic', 'patchouli', 'amber', 'oud', 'animalic', 'tobacco',
    'aquatic', 'oriental', 'light', 'boozy', 'coffee', 'chypre'
]

# Gender classification
GENDERS = ['male', 'female', 'unisex']

TOP_NOTES = [
    'Bergamot', 'Lemon', 'Grapefruit', 'Orange', 'Neroli', 'Petitgrain',
    'Mandarin', 'Tangerine', 'Pink Pepper', 'Cardamom', 'Cinnamon', 'Ginger',
    'Black Pepper', 'Coriander', 'Sage', 'Mint', 'Lavender', 'Basil',
    'Thyme', 'Fennel', 'Anise', 'Saffron', 'Cumin', 'Clove'
]

MIDDLE_NOTES = [
    'Rose', 'Jasmine', 'Peony', 'Orchid', 'Iris', 'Violet', 'Carnation',
    'Tuberose', 'Honeysuckle', 'Lilac', 'Hyacinth', 'Freesia', 'Gardenia',
    'Magnolia', 'Geranium', 'Patchouli', 'Cedar', 'Sandalwood', 'Vetiver',
    'Oakmoss', 'Lily', 'Musk', 'Vanilla', 'Cocoa', 'Almond', 'Coconut',
    'Hazelnut', 'Chestnut', 'Spice', 'Anise', 'Nutmeg'
]

BASE_NOTES = [
    'Sandalwood', 'Cedar', 'Vetiver', 'Patchouli', 'Oakmoss', 'Musk',
    'Vanilla', 'Tonka Bean', 'Amber', 'Oud', 'Agarwood', 'Benzoin',
    'Myrrh', 'Frankincense', 'Labdanum', 'Heliotrope', 'Iris Root',
    'Castoreum', 'Leather', 'Tobacco', 'Caramel', 'Cocoa', 'Coffee',
    'Cedarwood', 'Ebony Wood', 'Teak Wood', 'Fir Needle', 'Cade Oil'
]

PERFUME_NAMES_PATTERNS = [
    'Eternal {brand}', '{brand} Essence', 'Luxe {adjective}', 'Divine {noun}',
    '{brand} Noir', '{brand} Bleu', 'Opulent {noun}', 'Midnight {noun}',
    'Golden {noun}', 'Silken {adjective}', 'Crystal {noun}', '{brand} Pour Lui',
    '{brand} Pour Elle', 'Signature {noun}', 'Precious {noun}', 'Enchanted {noun}',
    'Elixir {noun}', 'Royal {noun}', 'Imperial {noun}', 'Majestic {noun}'
]

ADJECTIVES = [
    'Sublime', 'Exquisite', 'Elegant', 'Refined', 'Luxurious', 'Precious',
    'Enchanting', 'Captivating', 'Sensual', 'Alluring', 'Mysterious', 'Serene',
    'Radiant', 'Opulent', 'Magnificent', 'Regal', 'Divine', 'Eternal'
]

NOUNS = [
    'Essence', 'Elixir', 'Nectar', 'Treasure', 'Crown', 'Jewel', 'Dream',
    'Fantasy', 'Paradise', 'Garden', 'Palace', 'Kingdom', 'Empire', 'Dynasty'
]

CATEGORIES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Category IDs from database

def generate_perfume_data(fake):
    """Generate realistic perfume product data"""
    
    brand = random.choice(BRANDS)
    adjective = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    
    # Generate perfume name
    pattern = random.choice(PERFUME_NAMES_PATTERNS)
    if '{brand}' in pattern:
        if '{adjective}' in pattern:
            perfume_name = pattern.format(brand=brand, adjective=adjective)
        elif '{noun}' in pattern:
            perfume_name = pattern.format(brand=brand, noun=noun)
        else:
            perfume_name = pattern.format(brand=brand)
    else:
        if '{adjective}' in pattern:
            perfume_name = pattern.format(adjective=adjective)
        else:
            perfume_name = pattern.format(noun=noun)
    
    # Generate fragrance composition
    top_notes = ', '.join(random.sample(TOP_NOTES, random.randint(2, 4)))
    middle_notes = ', '.join(random.sample(MIDDLE_NOTES, random.randint(2, 4)))
    base_notes = ', '.join(random.sample(BASE_NOTES, random.randint(1, 3)))
    
    # Generate pricing
    base_price = round(random.uniform(45, 350), 2)
    discount = round(random.uniform(0, 35), 2) if random.random() > 0.7 else 0
    
    # Generate description
    descriptions = [
        f"A luxurious {random.choice(FRAGRANCE_TYPES).lower()} by {brand} that captures the essence of elegance and sophistication. Perfect for those who appreciate fine fragrances.",
        f"Exquisite composition featuring {top_notes.lower()} and rich {base_notes.lower()}. A timeless masterpiece from {brand}.",
        f"An enchanting fragrance that blends {middle_notes.lower()} with a sophisticated base. Designed for the discerning individual.",
        f"Experience the luxury of {brand} with this stunning fragrance. A perfect balance of freshness and depth.",
        f"A magnificent {random.choice(FRAGRANCE_TYPES).lower()} that evokes elegance and refinement. Ideal for special occasions or everyday wear."
    ]
    
    perfume_data = {
        'perfume_name': perfume_name,
        'brand_name': brand,
        'category_id': random.choice(CATEGORIES),
        'fragrance_type': random.choice(FRAGRANCE_TYPES),
        'classification': random.choice(CLASSIFICATIONS),
        'gender': random.choice(GENDERS),
        'description': random.choice(descriptions),
        'top_notes': top_notes,
        'middle_notes': middle_notes,
        'base_notes': base_notes,
        'price': base_price,
        'discount_percent': discount,
        'bottle_sizes': json.dumps(['30ml', '50ml', '100ml', '150ml']),
        'stock_quantity': random.randint(10, 500),
        'rating': round(random.uniform(3.5, 5.0), 1),
        'review_count': random.randint(5, 500),
        'is_featured': random.choice([True, False]),
        'is_new': random.choice([True, False])
    }
    
    return perfume_data

def seed_database():
    """Seed the database with 1000 perfume products"""
    
    try:
        # Connect to database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("🌟 AromaLux Database Seeder Starting...")
        print(f"📦 Generating 1000 premium perfume products...")
        
        # SQL insert query
        insert_query = """
        INSERT INTO perfumes 
        (perfume_name, brand_name, category_id, fragrance_type, classification, gender, description, 
         top_notes, middle_notes, base_notes, price, discount_percent, 
         bottle_sizes, stock_quantity, rating, review_count, is_featured, is_new)
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        fake = Faker()
        batch_size = 100
        total_inserted = 0
        
        # Generate and insert perfumes in batches
        for batch in range(10):  # 10 batches of 100 = 1000 perfumes
            batch_data = []
            
            for _ in range(batch_size):
                perfume_data = generate_perfume_data(fake)
                batch_data.append((
                    perfume_data['perfume_name'],
                    perfume_data['brand_name'],
                    perfume_data['category_id'],
                    perfume_data['fragrance_type'],
                    perfume_data['classification'],
                    perfume_data['gender'],
                    perfume_data['description'],
                    perfume_data['top_notes'],
                    perfume_data['middle_notes'],
                    perfume_data['base_notes'],
                    perfume_data['price'],
                    perfume_data['discount_percent'],
                    perfume_data['bottle_sizes'],
                    perfume_data['stock_quantity'],
                    perfume_data['rating'],
                    perfume_data['review_count'],
                    perfume_data['is_featured'],
                    perfume_data['is_new']
                ))
            
            # Execute batch insert
            cursor.executemany(insert_query, batch_data)
            connection.commit()
            
            total_inserted += len(batch_data)
            progress = (total_inserted / 1000) * 100
            print(f"✅ Progress: {total_inserted}/1000 perfumes inserted ({progress:.0f}%)")
        
        print("\n" + "="*50)
        print("🎉 Database seeding completed successfully!")
        print(f"📊 Total perfumes inserted: {total_inserted}")
        print("="*50)
        
        # Verify insertion
        cursor.execute("SELECT COUNT(*) FROM perfumes")
        count = cursor.fetchone()[0]
        print(f"✨ Verified: {count} perfumes in database")
        
        # Close connection
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        if err.errno == 2003:
            print("❌ Error: Cannot connect to MySQL. Please ensure MySQL is running.")
            print("   Start MySQL with: mysql -u root -p")
        elif err.errno == 1049:
            print("❌ Error: Database 'aromalux' not found.")
            print("   Run database.sql first to create the database schema.")
        else:
            print(f"❌ Database Error: {err}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    seed_database()
