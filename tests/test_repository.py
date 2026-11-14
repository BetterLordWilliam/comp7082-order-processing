import sqlite3

from pytest import fixture
from setup_db import initialize, SCHEMA
from repository import StoreRepository
from cart import ShoppingCart
from checkout import CheckoutService


def test_get_product(test_repo: StoreRepository):
    repo = test_repo
    product = repo.get_product('MOU-02') 
    
    assert product is not None  
    assert product.sku == 'MOU-02'
    assert product.name == 'Wireless mouse'
    assert product.price == 25.0
    assert product.stock == 10

def test_save_order(test_repo: StoreRepository):
    repo = test_repo
    oid = repo.save_order('test', 50.0, 'pending', '1234')
    assert oid is not None
    
def test_list_orders(test_repo: StoreRepository):
    repo = test_repo
    oid = repo.save_order('test', 50.0, 'pending', '1234')
    assert oid is not None
    os = repo.list_orders('test')
    assert len(os) > 0
    assert any(order[0] == 'test' for order in os) is not None
   
def test_list_orders_no_orders(test_repo: StoreRepository):
    os = test_repo.list_orders('idontexist')
    assert len(os) == 0
    
def test_update_stock(test_db: str, test_repo: StoreRepository):
    pass
    
