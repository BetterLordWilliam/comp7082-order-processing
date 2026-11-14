import sqlite3

from pytest import fixture
from setup_db import initialize, SCHEMA
from repository import StoreRepository
from cart import ShoppingCart
from checkout import CheckoutService


insert_products_query = 'insert into products (sku, name, price, stock) values (?, ?, ?, ?)'

test_db_file: str   = 'test.db'
test_user: str      = 'test_user'


@fixture(scope='session')
def test_db():
    db = test_db_file # a temporary database file for testing
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
    
@fixture(scope='session')
def test_repo(test_db: str):
    return StoreRepository(test_db)

@fixture(scope='function')
def test_cart(test_repo: StoreRepository):
    return ShoppingCart(test_user, test_repo)

