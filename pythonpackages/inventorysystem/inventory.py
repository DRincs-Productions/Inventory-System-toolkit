import renpy.store as store
from typing import Optional
from typing import Literal

__all__ = [
    "InventoryItem",
    "Inventory",
    "INVENTORY_ITEM_TYPE",
]

INVENTORY_ITEM_TYPE = type(Literal["Item"])


class InventoryItem(store.object):
    """Wiki: https://github.com/DRincs-Productions/Inventory-System-toolkit/wiki/Inventory-Items """

    def __init__(
        self,
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
    """Wiki: https://github.com/DRincs-Productions/Inventory-System-toolkit/wiki/Inventory """

    def __init__(
        self,
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

    def addItem(self, item_id: str, amt: int = 1, max: int = 100, min: int = 0):
        """Wiki: https://github.com/DRincs-Productions/Inventory-System-toolkit/wiki/Inventory#add-an-item-in-inventory """
        self.change(item_id, amt, max, min)

    def dropItem(self, item_id: str, amt: int = 1, max: int = 100, min: int = 0):
        """Wiki: https://github.com/DRincs-Productions/Inventory-System-toolkit/wiki/Inventory#remove-an-item-in-inventory """
        self.change(item_id, -amt, max, min)

    def depositMoney(self, amt: int):
        """Wiki: https://github.com/DRincs-Productions/Inventory-System-toolkit/wiki/Inventory#deposit-money """
        self.money -= amt

    def withdrawMoney(self, amt: int):
        """Wiki: https://github.com/DRincs-Productions/Inventory-System-toolkit/wiki/Inventory#withdraw-money """
        self.money += amt

    def sell(self, item_id: str, price: int):
        self.withdrawMoney(price)
        self.dropItem(item_id)

    def buy(self, item_id: str, price: int):
        self.depositMoney(price)
        self.addItem(item_id)

    def calculatePrice(self, item_id: str, inventory_items: dict[str, InventoryItem]) -> float:
        """Calculate price"""
        price = inventory_items[item_id].value + \
            (inventory_items[item_id].value * (self.interest_percentage))
        return float(price)
