# E-commerce Discount Service

A discount calculation system for fashion e-commerce that handles brand discounts, voucher codes, and bank offers with proper 

## Features
✅ Multiple discount types (brand, category, voucher, bank offers)  
✅ Proper discount stacking order  
✅ Decimal precision for currency  
✅ Comprehensive validation  
✅ Extensible architecture  

---

## How It Works

### Discount Flow
```
Cart → Brand/Category Discounts → Voucher Codes → Bank Offers → Final Price
```

### Example Calculation
```
PUMA T-shirt Original:    ₹1000
After Brand Discount:     ₹600  (40% off)
After Bank Offer:         ₹540  (10% ICICI)
────────────────────────────────
You Saved:                ₹460  (46%)
```

---

## Project Structure
```
├── models.py              # Data models
├── dummy_data.py          # Sample data & fixtures
├── discount_service.py    # Core business logic
├── test.py               # Test cases
└── README.md
```

---

## Quick Start

```bash
# Run tests
python3 test.py

# Expected output
============================================================
TEST: Multiple Discount Scenario
============================================================
Original Price: ₹1000
Final Price: ₹540
Applied Discounts:
  - Brand/Category Discount: ₹400
  - Bank Offer (ICICI): ₹60
✅ Test Passed!
```

---

## Architecture

### Core Components
- `calculate_cart_discounts()` - Main discount calculation
- `validate_discount_code()` - Voucher validation
- `_calculate_voucher_discount()` - Handles percentage/flat/tiered discounts

### Design Patterns
- **Service Layer**: Business logic separated from models
- **Repository Pattern**: Data access abstracted
- **Strategy Pattern**: Different discount types handled cleanly

---

## Extensibility

### Supported Discount Types
- Percentage (10% off, 69% off)
- Flat (₹500 off)
- Tiered (₹100 on ₹500+, ₹300 on ₹1000+)

### Easy to Add
- Buy X Get Y (Buy 2 get 1 free)
- Loyalty Points redemption
- Combo Offers (Buy 3, get 20% off)
- First-time user discounts
- Weekend-only offers

Simply extend `_calculate_voucher_discount()` or `validate_discount_code()` methods.

---

**Key Strategies**
1. **Horizontal Scaling**: Stateless service, deploy multiple instances
2. **Caching**: Redis for discount rules (95%+ hit ratio)
3. **Database**: Indexes on codes/brands, read replicas
4. **Async**: Non-blocking I/O, parallel processing
5. **Monitoring**: Track latency, error rates, cache hits
---

## Design Decisions

**1. Why Decimal not Float?**  
Float precision errors: `0.1 + 0.2 = 0.30000000000004`

**2. Why base_price and current_price?**  
Brand discounts pre-applied on product page, vouchers at checkout

**3. Why Async/Await?**  
Future-proof for DB/API calls, better concurrency

**4. Why Validate First?**  
Fail fast, clear errors, prevent partial application

---

## Edge Cases Handled
✅ Negative prices (max with 0)  
✅ Expired vouchers  
✅ Minimum cart values  
✅ Tier restrictions  
✅ Brand exclusions  
✅ Max discount caps  

---

## Test Scenarios

**Test 1**: Single product + bank offer → ✅  
**Test 2**: Voucher validation (valid/invalid) → ✅  
**Test 3**: Multiple products + voucher + bank → ✅  

---

## Future Enhancements
- Database integration (PostgreSQL/MongoDB)
- Redis caching layer
- Analytics dashboard
- Gift cards & referral system
- ML-based personalized offers

---

**Built for production e-commerce systems**