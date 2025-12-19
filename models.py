from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime
from decimal import Decimal
from enum import Enum


class BrandTier(Enum):
   PREMIUM = "premium"
   REGULAR = "regular"
   BUDGET = "budget"


@dataclass
class Product:
    id: str
    brand: str
    category: str
    base_price: Decimal
    current_price: Decimal
    brand_tier: Optional[BrandTier] = None  


@dataclass
class CartItem:
    product: Product
    quantity: int
    size: str


@dataclass
class PaymentInfo:
    method: str  
    bank_name: Optional[str]
    card_type: Optional[str]  


@dataclass
class CustomerProfile:
    id: str
    name: str
    tier: str  
    total_orders: int
    applied_voucher: Optional[str] = None 

@dataclass
class DiscountedPrice:
    original_price: Decimal
    final_price: Decimal
    applied_discounts: Dict[str, Decimal]
    message: str
