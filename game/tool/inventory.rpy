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
                    value: Optional[float] = None,
                    type: INVENTORY_ITEM_TYPE = "item",
                    ):

            self.name = name
            self.description = description
            self.icon = icon
            self.value = value
            # type of item
            self.type = type


    class Inventory(store.object):
        """Inventory of a character"""

        def __init__(self,
                    name: str,
                    money: int = 0,
                    interest_percentage: float = 1,
                    inventoryItems: Optional[dict[str, int]] = None,
                    ):

            self.name = name
            self.money = money
            # percentage of value paid for items
            self.interest_percentage = interest_percentage
            # items stored in nested list [item object, quantity]
            self.memory = {}
            self.memory.update(inventoryItems if inventoryItems else {})

            self.sort_order = True
            self.grid_view = True

        def set(self, text: str, value: int) -> None:
            """Function to set or add a new value"""
            if (text != None and text != ""):
                self.memory[text] = value
            else:
                self.remove(text)
            return

        def remove(self, text: str) -> None:
            """Delete the text value"""
            del self.memory[text]
            return

        def change(self, text: str, amt: int, max: int = 100, min: int = 0) -> None:
            """Changes a value, if it does not exist adds it"""
            if (self.getQuantity(text) != None):
                self.memory[text] += amt
                if (self.getQuantity(text) == 0):
                    self.remove(text)
            else:
                self.set(text, amt)
            return

        def getQuantity(self, text: str) -> Optional[int]:
            """Returns the value "text", in case it does not exist returns None"""
            if text in self.memory:
                return self.memory[text]
            else:
                return None

        def getValues(self) -> dict[str, int]:
            return self.memory

        def addItem(self, item_id, amt=1, max: int = 100, min: int = 0):
            """++++++"""
            self.change(item_id, amt, max, min)

        def dropItem(self, item_id, amt=1, max: int = 100, min: int = 0):
            """------"""
            self.change(item_id, -amt, max, min)

        def depositMoney(self, amt):
            self.money -= amt

        def withdrawMoney(self, amt):
            self.money += amt

        def sell(self, item_id, price):
            self.withdrawMoney(price)
            self.dropItem(item_id)

        def buy(self, item_id, price):
            self.depositMoney(price)
            self.addItem(item_id)

        def calculatePrice(self, item_id) -> float:
            """Calculate price"""
            price = inventory_items[item_id].value + \
                (inventory_items[item_id].value * (self.interest_percentage))
            return float(price)


    def moneyTransfer(depositor, withdrawer, amount):
        """Money transfer"""
        if depositor.money >= amount:
            depositor.depositMoney(amount)
            withdrawer.withdrawMoney(amount)
        else:
            message = _("Sorry, %s doesn't have %d!") % (buyer.name, amount)
            renpy.show_screen("popup", message=message)


    def trade(seller, buyer, item_id):
        """Trade"""
        seller.dropItem(item_id)
        buyer.addItem(item_id)


    def transaction(seller, buyer, item_id):
        """Transaction"""
        price = seller.calculatePrice(item_id)
        if buyer.money >= price:
            seller.sell(item_id, price)
            buyer.buy(item_id, price)
        else:
            message = _("Sorry, %s doesn't have enough money!") % (buyer.name)
            renpy.show_screen("popup", message=message)


    def getItemNumberInInventory(inventory1, inventory2) -> int:
        return getItemNumberInInventory(inventory1 | inventory2)


    def getItemNumberInInventory(inventory) -> int:
        """Returns the number of items in the inventory"""
        return len(inventory.getValues())
