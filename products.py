"""This is a place to sore the classes for my Python program to make the code
smaller on each page
By: Matt Smith                                                    13/05/2026"""


class products:
    # The main class for items in the inventory
    def __init__(self, barcode, name, type, subtype, cost, amount):
        # initial information
        self.barcode = barcode
        self.product_name = name
        self.product_type = type
        self.subtype = subtype
        self.cost = cost
        self.old = amount
        self.current = 0
        self.purchase = 0
        self.sold = 0

    def inventory_count(self, amount):
        # tool to complete a inventory count
        self.current = amount

    def stock_sold(self, amount):
        # to increase the sold amount
        self.sold = amount

    def stock_purchase(self, amount):
        # to increase the purchase amount
        self.purchase = amount

    def finish_report(self):
        # to reset the item after a report is generated
        self.old = self.current
        self.current = 0
        self.purchase = 0

    def description(self):
        # info for the report
        return [self.barcode, self.product_name, self.old, self.purchase,
                self.current, self.cost, self.sold]
