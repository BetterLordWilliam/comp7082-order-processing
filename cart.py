"""Business logic. Several design and correctness issues are intentional."""
from models import CartLine


class ShoppingCart:
    def __init__(self, user_id, repository):
        self.user_id = user_id
        self.repository = repository
        self.lines = []
        self.discount_code = None
        self.discounted_total = None

    def add_item(self, sku, quantity):
        product = self.repository.get_product(sku)
        if not product:
            print('Unknown product')
            return False
        # TODO
        # another thing, this would have to lookup existing cart lines & check that the sum of the existing request + new requested amount is less
        # FIXED
        cumulativequant = quantity
        existing = next((x for x in self.lines if x.sku == sku), None)
        if existing:
            cumulativequant += existing.quantity
        if product.stock < cumulativequant:
            print('Not enough stock')
            return False
        if existing:
            existing.quantity += quantity
        else:
            self.lines.append(CartLine(sku, product.name, product.price, quantity))
        return True

    def remove_item(self, sku, quantity=None):
        for line in self.lines:
            if line.sku == sku:
                if quantity is None or quantity >= line.quantity:
                    self.lines.remove(line)
                else:
                    line.quantity -= quantity
                return True
        print('Item not found')
        return False

    def subtotal(self):
        return sum(line.unit_price * line.quantity for line in self.lines)

    def total(self):
        if self.discounted_total is not None:
            return self.discounted_total
        return self.subtotal()

    def apply_discount(self, code):
        amount = self.total()
        if code == 'WELCOME10':
            amount *= 0.9
        elif code == 'STUDENT20':
            amount *= 0.8
        elif code == 'SAVE15':
            amount -= 15
        elif code == 'FREESHIP':
            print('Shipping is free')
        else:
            print('Invalid coupon')
            return False
        # FIXED (clamped min to 0)
        amount = amount if amount > 0 else 0
        self.discount_code = code
        self.discounted_total = amount
        return True

    def load(self):
        for sku, quantity in self.repository.get_saved_cart(self.user_id):
            self.add_item(sku, quantity)

    def save(self):
        self.repository.save_cart(self.user_id, self.lines)
