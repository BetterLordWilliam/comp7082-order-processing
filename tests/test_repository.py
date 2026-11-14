import sqlite3

from pytest import fixture
from setup_db import initialize, SCHEMA
from repository import StoreRepository
from cart import ShoppingCart
from checkout import CheckoutService

insert_products_query = 'insert into products (sku, name, price, stock) values (?, ?, ?, ?)'

@fixture(scope='module')
def test_db():
    db = 'test.db' # a temporary database file for testing
    conn = sqlite3.connect(str(db))
    conn.executescript(SCHEMA)
    conn.execute(insert_products_query, ('MOU-02', 'Wireless mouse', 25.0, 10))
    conn.execute(insert_products_query, ('USB-02', 'USB-C cable', 10.0, 20))
    conn.commit()
    yield str(db)
    conn.execute('delete from products')
    conn.execute('delete from saved_cart')
    conn.execute('delete from orders')
    conn.commit()
    conn.close()
    
@fixture(scope='module')
def test_repo(test_db: str):
    return StoreRepository(test_db)


def test_get_product(test_db: str, test_repo: StoreRepository):
    repo = test_repo
    product = repo.get_product('MOU-02') 
    
    assert product is not None  
    assert product.sku == 'MOU-02'
    assert product.name == 'Wireless mouse'
    assert product.price == 25.0
    assert product.stock == 10

def test_save_order(test_db: str, test_repo: StoreRepository):
    repo = test_repo
    oid = repo.save_order('test', 50.0, 'pending', '1234')
    assert oid is not None
    
def test_list_orders(test_db: str, test_repo: StoreRepository):
    repo = test_repo
    oid = repo.save_order('test', 50.0, 'pending', '1234')
    assert oid is not None
    os = repo.list_orders('test')
    assert len(os) > 0
    assert any(order[0] == 'test' for order in os) is not None
   
def test_list_orders_no_orders(test_db: str, test_repo: StoreRepository):
    os = test_repo.list_orders('idontexist')
    assert len(os) == 0
    
    
