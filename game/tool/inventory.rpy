init python: 
    import renpy.store as store
    from typing import Optional
    from typing import Literal

    INVENTORY_ITEM_TYPE = type(Literal["Item"])

    class InventoryItem(store.object):
        """Inventory item"""
        def __init__(self,
            name: str,
            description: str,
            icon: str,
            value: Optional[int] = None,
            type: INVENTORY_ITEM_TYPE="item",
        ):

            self.name = name
            self.description = description
            self.icon = icon
            self.value = value
            # type of item
            self.type = type

        def change(self, name, description=False, icon=False, value=False):
            self.name = name
            if description:
                self.description = description
            if icon:
                self.icon = icon
            if value:
                self.value = value

    class Inventory(store.object):
        """Inventory of a character"""
        def __init__(self,
            name,
            money = 0,
            barter = 100,
            inv = {}):

            self.name = name
            self.money = money
            # percentage of value paid for items
            self.barter = barter
            # items stored in nested list [item object, qty]
            self.inv = {}
            self.inv.update(inv)

            self.sort_order = True
            self.grid_view = True

        def set(self, text, value):
            """Function to set or add a new value"""
            if (text != None and text != ""):
                self.inv[text] = value
            else:
                self.remove(text)
        def remove(self, text):
            """Delete the text value"""
            del self.inv[text]
        def change(self, text, amt, max=100, min=0):
            """Changes a value, if it does not exist adds it"""
            if (self.get(text) != None):
                self.inv[text] += amt
                if (self.get(text) == 0):
                    self.remove(text)
            else:
                self.set(text, amt)
        def get(self, text):
            """Returns the value "text", in case it does not exist returns None"""
            if text in self.inv:
                return self.inv[text]
            else:
                return None

        def take(self, item, qty=1):
            """++++++"""
            self.change(item, qty)
        def drop(self, item, qty=1):
            """------"""
            self.change(item, -qty)
        def qty(self, item):
            """Returns quantity"""
            return self.get(item)

        def deposit(self, amount):
            self.money -= amount
        def withdraw(self, amount):
            self.money += amount

        def sell(self, item, price):
            self.withdraw(price)
            self.drop(item)
        def buy(self, item, price):
            self.deposit(price)
            self.take(item)

    def calculate_price(item, buyer):
        """Calculate price"""
        if buyer:
            price = inventory_items[item].value * (buyer.barter * 0.01)
            return int(price)

    def money_transfer(depositor, withdrawer, amount):
        """Money transfer"""
        if depositor.money >= amount:
            depositor.deposit(amount)
            withdrawer.withdraw(amount) 
        else:
            message = _("Sorry, %s doesn't have %d!") % (buyer.name, amount)
            renpy.show_screen("popup", message=message) 

    def trade(seller, buyer, item):
        """Trade"""
        seller.drop(item)
        buyer.take(item)

    def transaction(seller, buyer, item):
        """Transaction"""
        price = calculate_price(item, buyer)
        if buyer.money >= price:
            seller.sell(item, price)
            buyer.buy(item, price)
        else:
            message = _("Sorry, %s doesn't have enough money!") % (buyer.name)
            renpy.show_screen("popup", message = message)

    def getItemNumberInInventory(inventory1, inventory2) -> int:
        return getItemNumberInInventory(inventory1 | inventory2)

    def getItemNumberInInventory(inventory) -> int:
        """Returns the number of items in the inventory"""
        return len(inventory.inv)
