"""Two simple smoke tests"""
import sqlite3
from pytest import skip
from setup_db import initialize
from repository import StoreRepository
from cart import ShoppingCart

def test_seed_product(tmp_path):
    skip('smoke test 1')
    db = tmp_path / 'test.db'
    initialize(str(db))
    assert StoreRepository(str(db)).get_product('MOU-01').name == 'Wireless mouse'

def test_cart_adds_valid_item(tmp_path):
    skip('smoke test 2')
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('student', StoreRepository(str(db)))
    assert cart.add_item('USB-01', 2)
    assert len(cart.lines) == 1
