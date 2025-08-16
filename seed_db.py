import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
django.setup()

from crm.models import Customer, Product

def seed():
    # Clear existing data
    Customer.objects.all().delete()
    Product.objects.all().delete()

    # Customers
    Customer.objects.create(name="Alice", email="alice@example.com", phone="+1234567890")
    Customer.objects.create(name="Bob", email="bob@example.com", phone="123-456-7890")

    # Products
    Product.objects.create(name="Laptop", price=999.99, stock=10)
    Product.objects.create(name="Phone", price=499.99, stock=20)

    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
