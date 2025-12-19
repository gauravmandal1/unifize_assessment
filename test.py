import asyncio
from decimal import Decimal
from models import CartItem, PaymentInfo
from discount_service import DiscountService
from dummy_data import BANK_OFFERS_DB, VOUCHERS_DB, get_sample_customer, get_sample_products


async def test_multiple_discount_scenario():
    """
    """
    print("=" * 60)
    print("TEST: Multiple Discount Scenario")
    print("=" * 60)
    
    # Setup
    service = DiscountService(VOUCHERS_DB, BANK_OFFERS_DB)
    products = get_sample_products()
    customer = get_sample_customer()
    
    # Create cart with PUMA T-shirt
    cart_items = [
        CartItem(product=products[0], quantity=1, size="M")  # PUMA T-shirt
    ]
    
    # Payment with ICICI bank
    payment_info = PaymentInfo(
        method="CARD",
        bank_name="ICICI",
        card_type="CREDIT"
    )
    
    # Calculate discounts
    result = await service.calculate_cart_discounts(cart_items, customer, payment_info)
    
    for discount_name, amount in result.applied_discounts.items():
        print(f"  - {discount_name}: ₹{amount}")
    print(f"\n{result.message}")
    
    # Assertions
    assert result.original_price == Decimal('1000')
    assert result.final_price == Decimal('540')  # 600 - 10% bank = 540
    assert len(result.applied_discounts) == 2
    
    

async def test_voucher_validation():
    """Test voucher code validation"""
    print("\n" + "=" * 60)
    print("TEST: Voucher Validation")
    print("=" * 60)
    
    service = DiscountService(VOUCHERS_DB, BANK_OFFERS_DB)
    products = get_sample_products()
    customer = get_sample_customer()
    
    cart_items = [CartItem(product=products[0], quantity=1, size="M")]
    
    # Test valid voucher
    is_valid = await service.validate_discount_code('SUPER69', cart_items, customer)
    print(f"\nVoucher 'SUPER69' validation: {is_valid}")
    assert is_valid == True
    
    # Test invalid voucher
    is_valid = await service.validate_discount_code('INVALID', cart_items, customer)
    print(f"Voucher 'INVALID' validation: {is_valid}")
    assert is_valid == False
    


async def test_with_voucher():
    """Test with voucher code applied"""
    print("\n" + "=" * 60)
    print("TEST: Cart with Voucher Code")
    print("=" * 60)
    
    service = DiscountService(VOUCHERS_DB, BANK_OFFERS_DB)
    products = get_sample_products()
    customer = get_sample_customer()
    
    # Apply voucher to customer
    customer.applied_voucher = 'TSHIRT10'
    
    cart_items = [CartItem(product=products[0], quantity=2, size="M")]  # 2 PUMA T-shirts
    
    payment_info = PaymentInfo(method="CARD", bank_name="ICICI", card_type="CREDIT")
    
    result = await service.calculate_cart_discounts(cart_items, customer, payment_info)
    
    print(f"\nOriginal Price: ₹{result.original_price}")
    print(f"Final Price: ₹{result.final_price}")
    print(f"\nApplied Discounts:")
    for discount_name, amount in result.applied_discounts.items():
        print(f"  - {discount_name}: ₹{amount}")
    
    
async def test_flat_discount():
    """Test flat discount - super simple"""
    print("\n" + "=" * 60)
    print("TEST: Flat Discount (₹500 off)")
    print("=" * 60)
    
    service = DiscountService(VOUCHERS_DB, BANK_OFFERS_DB)
    products = get_sample_products()
    customer = get_sample_customer()
    customer.applied_voucher = 'FLAT500'
    
    # ADIDAS shoes: ₹2100
    cart_items = [CartItem(product=products[1], quantity=1, size="10")]
    
    result = await service.calculate_cart_discounts(cart_items, customer)
    
    print(f"\nOriginal Price: ₹{result.original_price}")
    print(f"After Brand Discount: ₹2100")
    print(f"After Flat ₹500: ₹{result.final_price}")
    print(f"\nExpected: ₹1600")
    
    assert result.final_price == Decimal('1600')


async def test_tiered_discount():
    """Test tiered discount - also simple"""
    print("\n" + "=" * 60)
    print("TEST: Tiered Discount")
    print("=" * 60)
    
    service = DiscountService(VOUCHERS_DB, BANK_OFFERS_DB)
    products = get_sample_products()
    customer = get_sample_customer()
    customer.applied_voucher = 'TIERED'
    
    # 2 PUMA T-shirts: 2 × ₹600 = ₹1200
    cart_items = [CartItem(product=products[0], quantity=2, size="M")]
    
    result = await service.calculate_cart_discounts(cart_items, customer)
    
    print(f"\nCart Total: ₹1200")
    print(f"Tier Matched: ₹1000+ → ₹200 off")
    print(f"Final Price: ₹{result.final_price}")
    print(f"\nExpected: ₹1000")
    
    assert result.final_price == Decimal('1000')



async def main():
   
    await test_multiple_discount_scenario()

    await test_voucher_validation()

    await test_with_voucher()

    await test_flat_discount()
    
    await test_tiered_discount()
    


if __name__ == "__main__":
    asyncio.run(main())
    