import sqlite3
from setup_db import initialize
from repository import StoreRepository
from cart import ShoppingCart
from checkout import CheckoutService



def test_add_item_to_cart(test_cart: ShoppingCart):
    cart = test_cart
    assert cart.add_item('MOU-02', 1) is True
    
def test_add_invalid_item_to_cart(test_cart: ShoppingCart):
    cart = test_cart
    assert cart.add_item('imnotreal', 1) is False
    
def test_add_same_item_to_cart(test_cart: ShoppingCart):
    cart = test_cart
    assert cart.add_item('MOU-02', 1) is True
    assert cart.add_item('MOU-02', 1) is True
    assert len(cart.lines) == 1
    assert cart.lines[0].quantity == 2
    
def test_add_different_item_to_cart(test_cart: ShoppingCart):
    cart = test_cart
    assert cart.add_item('MOU-02', 1) is True
    assert cart.add_item('USB-02', 2) is True
    assert len(cart.lines) == 2
    assert cart.lines[0].quantity == 1
    assert cart.lines[1].quantity == 2

def test_remove_item_from_cart(test_cart: ShoppingCart):
    cart = test_cart
    assert cart.add_item('MOU-02', 1) is True
    assert cart.remove_item('MOU-02') is True
    
def test_remove_same_item_from_cart(test_cart: ShoppingCart):
    cart = test_cart
    assert cart.add_item('MOU-02', 1) is True
    assert cart.add_item('MOU-02', 1) is True
    assert len(cart.lines) == 1
    assert cart.lines[0].quantity == 2
    assert cart.remove_item('MOU-02', 1) is True
    assert len(cart.lines) == 1
    assert cart.lines[0].quantity == 1
    
def test_remove_invalid_item_from_cart(test_cart: ShoppingCart):
    cart = test_cart
    assert cart.remove_item('imnotreal') is False
   
def test_add_too_many_items(test_cart: ShoppingCart):
    cart = test_cart
    assert cart.add_item('MOU-02', 10) is True
    assert cart.add_item('MOU-02', 1) is False
   
def test_add_item_correct_total(test_repo: StoreRepository, test_cart: ShoppingCart):
    cart = test_cart
    repo = test_repo
    item = repo.get_product('MOU-02')
    assert item is not None
    assert cart.add_item(item.sku, 1) is True
    assert cart.total() == item.price
    
    
def test_welcome10_discount(test_repo: StoreRepository, test_cart: ShoppingCart):
    cart = test_cart
    repo = test_repo
    item = repo.get_product('MOU-02')
    assert item is not None
    assert cart.add_item('MOU-02', 1) is True
    assert cart.total() >= 0
    assert cart.apply_discount('WELCOME10') is True
    assert cart.total() == item.price * 0.9
    
def test_student20_discount(test_repo: StoreRepository, test_cart: ShoppingCart):
    cart = test_cart
    repo = test_repo
    item = repo.get_product('MOU-02')
    assert item is not None
    assert cart.add_item(item.sku, 1) is True
    assert cart.total() >= 0
    assert cart.apply_discount('STUDENT20') is True
    assert cart.total() == item.price * 0.8
    
def test_save15_discount(test_repo: StoreRepository, test_cart: ShoppingCart):
    cart = test_cart
    repo = test_repo
    item = repo.get_product('MOU-02')
    assert item is not None
    assert cart.add_item(item.sku, 1) is True
    assert cart.total() >= 0
    assert cart.apply_discount('SAVE15') is True
    assert cart.total() == item.price - 15 if item.price >= 15 else 0
    
def test_save15_repeat_discount(test_repo: StoreRepository, test_cart: ShoppingCart):
    cart = test_cart
    repo = test_repo
    item = repo.get_product('MOU-02')
    assert item is not None
    assert cart.add_item(item.sku, 1) is True
    assert cart.total() >= 0
    assert cart.apply_discount('SAVE15') is True
    assert cart.apply_discount('SAVE15') is True
    assert cart.total() == item.price - 15 if item.price >= 15 else 0

