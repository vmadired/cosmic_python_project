class OutOfStockEx(Exception):
    def __init__(self, order_sku):
        raise Exception(f'Out of stock for sku: {order_sku}')
