# identified defects
First step is to go through the code to attempt to identify the defects in it.

*at least 8 requried*

- `StoreRepository` class
    - `get_product` method does not use a parameterized query for its sqlite execute statement.
        - SQL injection
    - `get_saved_cart` method does not use a parameterized query for its sqlite execute statement.
        - SQL injection
    - `save_cart` we could just insert the new cart items with 1 statement, `INSERT` is capable of doing that.
        - `executemany` method of the `Cursor` class
    - `list_orders` ignores the `user_id`

- `ShoppingCart` class
    - `apply_discount` code SAVE15 just subtracts from  the total, so that would potentially leave a negative amount which doesn't really make sense, it should subtract up to 15 dollars, but then I guess they just get free stuff if the cart is less than 15 dollars (not negative totals or refunds)
    - general issue w/ discount calculation
        - discounts are applied to whatever is in the cart at the time of their application, but they do not apply to items added to the cart after wards.
        - it makes more sense to keep a list of applied discounts & then iterate & apply these at the time of checkout so that items added at any point will be discounted

- `FakePaymentGateway` class
    -

- `CheckoutService` class
    - `checkout` method

        ```python
        if amount > 1000:
            if cart.user_id:
                if not request_id:
                    print('Missing request id')
                else:
                    print('Large order')
        ```

        - I do not really understand the intention of this logic
            - I think it would make more sense to switch a a fail fast approach (these 2 things seem like actions we would take regardless of total, though this is admittedly an assumption on my part about the business logic)
                - I wont make the code fail because it doesn't do that in the original & there's no indication about business logic for this assignment, so its not clear if these cases should even result in failure, I will print the issues though
            - then we can keep the logic that checks if the amount is large
            - not a bug, but confusing logic that should be flattened

        ```python
        # my only assumption is `request_id` & `cart.user_id` seem like they should be checked regardless of whether or not the order is large
        if not request_id:
            print('Missing request ID') # a real application would have some rules about this, but we aren't given these and I wont make any more assumptions
        if not cart.user_id:
            print('Missing user id') # a real application would have some rules about this, but we aren't given these and I wont make any more assumptions
        if amount > 1000:
            print('Large order') # not clear whether some other action should be taken for this case
        ```

        - payment should happen first, the if payment succeeds then update stock
            - this should also be done as one transaction, instead of multiple
        - checkout will just be repeated on the cart, although checkout does clear the cars lines (if it is invoked again)
            - not an issue


# planned unit tests
*at least 12 required*

## `test_repository`

- `test_insert_order`
- `test_list_orders`
- `test_update_stock`

## `test_cart`

## `test_payments`

## `test_checkout`




# references
- https://docs.python.org/3/library/sqlite3.html#
    - https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor
    - https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.executemany

