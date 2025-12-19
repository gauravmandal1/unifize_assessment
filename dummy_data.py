from decimal import Decimal
from datetime import datetime, timedelta
from typing import List
from models import Product, CustomerProfile


# Vouchers Database
VOUCHERS_DB = {
    'SUPER69': {
        'discount_percent': Decimal('69'),
        'valid_until': datetime.now() + timedelta(days=30),
        'min_cart_value': Decimal('0'),
    },
    'FIRST20': {
        'discount_percent': Decimal('20'),
        'valid_until': datetime.now() + timedelta(days=30),
        'min_cart_value': Decimal('500'),
        'required_tier': 'GOLD',
    },
    'TSHIRT10': {
        'discount_percent': Decimal('10'),
        'valid_until': datetime.now() + timedelta(days=30),
        'min_cart_value': Decimal('0'),
        'allowed_categories': {'T-shirts'},
    }
}

BANK_OFFERS_DB = {
    'ICICI': {
        'discount_percent': Decimal('10'),
        'max_discount': Decimal('500'),
    },
    'HDFC': {
        'discount_percent': Decimal('15'),
        'max_discount': Decimal('1000'),
    }
}


def get_sample_products() -> List[Product]:
    """Create sample products for testing"""
    
    puma_tshirt = Product(
        id="P001",
        brand="PUMA",
        category="T-shirts",
        base_price=Decimal('1000'),
        current_price=Decimal('600')  
    )
    
    adidas_shoes = Product(
        id="P002",
        brand="ADIDAS",
        category="Shoes",
        base_price=Decimal('3000'),
        current_price=Decimal('2100') 
    )
    
    generic_tshirt = Product(
        id="P003",
        brand="LocalBrand",
        category="T-shirts",
        base_price=Decimal('500'),
        current_price=Decimal('450')  
    )
    
    return [puma_tshirt, adidas_shoes, generic_tshirt]


def get_sample_customer() -> CustomerProfile:
    """Create sample customer"""
    return CustomerProfile(
        id="C001",
        name="Rahul Sharma",
        tier="GOLD",
        total_orders=5
    )
