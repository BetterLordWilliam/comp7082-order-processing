import sqlite3
from setup_db import initialize
from repository import StoreRepository
from cart import ShoppingCart
from payments import FakePaymentGateway
from checkout import CheckoutService
from models import OrderResult


def test_checkout_service(test_repo: StoreRepository, test_cart: ShoppingCart):
    repo = test_repo
    cart = test_cart
    check = CheckoutService(repo, FakePaymentGateway(True, 0))
    
    item = repo.get_product('MOU-02')
    assert item is not None
    assert item.stock == 10
    assert cart.add_item('MOU-02', 1) is True
    order: OrderResult = check.checkout(cart, 'TOKEN', 'TEST')
    assert order.status == 'paid'
    item = repo.get_product('MOU-02')
    assert item is not None
    assert item.stock == 10 - 1
  
def test_checkout_empty_cart(test_repo: StoreRepository, test_cart: ShoppingCart):
    repo = test_repo
    cart = test_cart
    check = CheckoutService(repo, FakePaymentGateway(True, 0))
    
    order: OrderResult = check.checkout(cart, 'TOKEN', 'TEST')
    assert order.status == 'empty'
   
def test_checkout_service_payment_failure(test_repo: StoreRepository, test_cart: ShoppingCart):
    repo = test_repo
    cart = test_cart
    check = CheckoutService(repo, FakePaymentGateway(False, 0))
    
    item = repo.get_product('MOU-02')
    assert item is not None
    assert item.stock == 10
    assert cart.add_item('MOU-02', 1) is True
    order: OrderResult = check.checkout(cart, 'TOKEN', 'TEST')
    assert order.status == 'declined'
    item = repo.get_product('MOU-02')
    assert item is not None
    assert item.stock != 10 - 1
    

