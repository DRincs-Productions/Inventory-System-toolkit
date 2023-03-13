init python:
    def moneyTransfer(depositor, withdrawer, amount):
        """Money transfer"""
        if depositor.money >= amount:
            depositor.depositMoney(amount)
            withdrawer.withdrawMoney(amount)
        else:
            message = _("Sorry, %s doesn't have %d!") % (withdrawer.name, amount)
            renpy.show_screen("popup", message=message)


    def trade(seller, buyer, item_id):
        """Trade"""
        seller.dropItem(item_id)
        buyer.addItem(item_id)


    def transaction(seller, buyer, item_id):
        """Transaction"""
        price = seller.calculatePrice(item_id, inventory_items)
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
