from database.models import sql_cursor, Product


def add_sample_products():
    """Add some sample products to test the system"""

    sample_products = [
        {"name": "Premium VPN Access", "description": "1-month premium VPN access", "price": 9.99, "stock": 50},
        {"name": "Netflix Account", "description": "30-day Netflix premium access", "price": 15.99, "stock": 25},
        {"name": "Spotify Premium", "description": "3-month Spotify premium", "price": 12.99, "stock": 30},
        {"name": "Gaming Credits", "description": "25 gaming platform credits", "price": 20.00, "stock": 100},
        {"name": "Domain Registration (.com)", "description": "1-year domain registration", "price": 11.50,
         "stock": 75},
        {"name": "Web Hosting Plan (Basic)", "description": "1-month basic web hosting", "price": 5.99, "stock": 0},
        {"name": "Discord Nitro", "description": "1-month Discord Nitro subscription", "price": 9.99, "stock": 40},
        {"name": "YouTube Premium", "description": "1-month YouTube Premium", "price": 13.99, "stock": 0},
        {"name": "Online Course: Python Basics", "description": "Self-paced course on Python", "price": 49.99,
         "stock": 20},
        {"name": "Antivirus Software", "description": "1-year antivirus software license", "price": 29.99, "stock": 0}
    ]

    with sql_cursor() as session:
        for product_data in sample_products:
            existing = session.query(Product).filter(Product.name == product_data["name"]).first()
            if not existing:
                product = Product(**product_data)
                session.add(product)
        session.commit()
        print("Sample products added successfully!")


if __name__ == "__main__":
    add_sample_products()
