from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict
from models import CartItem, CustomerProfile, PaymentInfo, DiscountedPrice

class DiscountService:
   
    def __init__(self, vouchers_db: Dict, bank_offers_db: Dict):
        self.vouchers_db = vouchers_db
        self.bank_offers_db = bank_offers_db

    async def calculate_cart_discounts(
        self,
        cart_items: List[CartItem],
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None
    ) -> DiscountedPrice:
        """
        Calculate final price after applying discounts in order:
        1. Brand/Category discounts (already in current_price)
        2. Voucher codes
        3. Bank offers
        """
        
        applied_discounts = {}
        
        original_total = sum(item.product.base_price * item.quantity for item in cart_items)
        after_brand_discount = sum(item.product.current_price * item.quantity for item in cart_items)
        
        brand_category_discount = original_total - after_brand_discount
        if brand_category_discount > 0:
            applied_discounts["Brand/Category Discount"] = brand_category_discount
        
        current_total = after_brand_discount
        
        voucher_discount = Decimal('0')
        voucher_code = customer.applied_voucher
        
        if voucher_code:
            voucher = self.vouchers_db.get(voucher_code)
            if voucher and await self.validate_discount_code(voucher_code, cart_items, customer):
                voucher_discount = self._calculate_voucher_discount(voucher, current_total)
                applied_discounts[f"Voucher ({voucher_code})"] = voucher_discount
                current_total -= voucher_discount
        
        bank_discount = Decimal('0')
        if payment_info and payment_info.bank_name:
            bank_offer = self.bank_offers_db.get(payment_info.bank_name)
            if bank_offer:
                bank_discount = current_total * (bank_offer['discount_percent'] / 100)
                if 'max_discount' in bank_offer:
                    bank_discount = min(bank_discount, bank_offer['max_discount'])
                applied_discounts[f"Bank Offer ({payment_info.bank_name})"] = bank_discount
                current_total -= bank_discount
        
        final_price = max(Decimal('0'), current_total)
        message = self._generate_message(original_total, final_price, applied_discounts)
        
        return DiscountedPrice(
            original_price=original_total,
            final_price=final_price,
            applied_discounts=applied_discounts,
            message=message
        )
    
    def _calculate_voucher_discount(self, voucher: Dict, current_total: Decimal) -> Decimal:
        """Calculate discount based on voucher type - simple and clean"""
        
        discount_type = voucher.get('discount_type', 'percentage') 
        
        if discount_type == 'percentage':
            discount = current_total * (voucher['discount_percent'] / 100)
            return discount
        
        elif discount_type == 'flat':
            return min(voucher['discount_value'], current_total)
        
        elif discount_type == 'tiered':
            for tier in voucher['tiers']:
                if current_total >= tier['min']:
                    return min(tier['discount'], current_total)
            return Decimal('0')
        
        return Decimal('0')
    


    async def validate_discount_code(
        self,
        code: str,
        cart_items: List[CartItem],
        customer: CustomerProfile
    ) -> bool:
        """
        Validate if a discount code can be applied
        """
        voucher = self.vouchers_db.get(code)
        
        if not voucher:
            return False
        
        if datetime.now() > voucher['valid_until']:
            return False
        
        cart_total = sum(item.product.current_price * item.quantity for item in cart_items)
        if cart_total < voucher.get('min_cart_value', Decimal('0')):
            return False
        
        if 'required_tier' in voucher:
            if customer.tier != voucher['required_tier']:
                return False
        
        if 'excluded_brands' in voucher:
            for item in cart_items:
                if item.product.brand in voucher['excluded_brands']:
                    return False
        
        if 'allowed_categories' in voucher:
            cart_categories = {item.product.category for item in cart_items}
            if not cart_categories.intersection(voucher['allowed_categories']):
                return False
        
        return True
    
    def _generate_message(self, original: Decimal, final: Decimal, discounts: Dict[str, Decimal]) -> str:
            """Generate a user-friendly message"""
            if not discounts:
                return f"Total: ₹{final}"
            
            savings = original - final
            message = f"You saved ₹{savings}! "
            
            discount_parts = [f"{name}: ₹{amount}" for name, amount in discounts.items()]
            message += " | ".join(discount_parts)
            
            return message

    
