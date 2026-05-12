"""This is a place to sore the classes for my Python program to make the code
smaller on each page
By: Matt Smith                                                    13/05/2026"""


class products:
    # The main class for items in the ivotory
    def __init__(self, barcode, name, type, subtype, cost, amount):
        # initial information
        self.barcode = barcode
        self.product_name = name
        self.product_type = type
        self.subtype = subtype
        self.cost = cost
        self.old = amount
        self.curent = 0
        self.purcase = 0

    def invotory_count(self, amount):
        # tool to complete a invotory count
        self.curent = amount

    def stock_purcase(self, amount):
        # to increce the purcase amount
        self.purcase = amount

    def finish_report(self):
        # to reset the item after a repot is genarated
        self.old = self.curent
        self.curent = 0
        self.purcase = 0

    def description(self):
        # info for the report
        return [self.barcode, self.product_name, self.old, self.purcase,
                self.curent, self.cost]
