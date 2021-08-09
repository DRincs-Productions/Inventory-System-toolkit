init python: 
    import renpy.store as store
    
    class Item(store.object):
        """Inventory item"""
        def __init__(self,
            name,
            description,
            icon,
            value = None,
            act = Show("inventory_popup", message="Nothing happened!"), type="item", recipe=False):

            global cookbook
            self.name = name
            self.description = description
            self.icon = icon
            self.value = value
            # screen action
            self.act = act
            # type of item
            self.type = type
            # nested list of [ingredient, qty]
            self.recipe = recipe

            if recipe:
                cookbook.append(self)
                # alpha order
                cookbook.sort(key=lambda i: i.name)

        def change(self, name, description=False, icon=False, value=False, act=False, recipe=False):
            self.name = name
            if description:
                self.description = description
            if icon:
                self.icon = icon
            if value:
                self.value = value
            if act:
                self.act = act
            if recipe:
                self.recipe = recipe

    class Inventory(store.object):
        """Inventory of a character"""
        def __init__(self,
            name,
            money = 0,
            barter = 100):

            self.name = name
            self.money = money
            # percentage of value paid for items
            self.barter = barter
            # items stored in nested list [item object, qty]
            self.inv = [] 
            self.sort_by = self.sort_name
            # ascending, descriptionending
            self.sort_order = True
            self.grid_view = True

        def buy(self, item, price):
            self.deposit(price)
            self.take(item[0])

        def check(self, item):
            """Returns item index (location)"""
            if self.qty(item):
                for i in self.inv:
                    if i[0] == item:
                        return self.inv.index(i)

        def check_recipe(self, item):
            """Verify all ingredients are in inv"""
            checklist = list()
            for i in item.recipe:
                if self.qty(i[0]) >= i[1]:
                    checklist.append(True)
            if len(checklist) == len(item.recipe):
                return True
            else:
                return False
   
        def craft(self, item):
            for line in item.recipe:
                self.drop(line[0], line[1])
            self.take(item)  
            message = _("Crafted a %s!") % (item.name)
            renpy.show_screen("inventory_popup", message=message)

        def deposit(self, amount):
            self.money -= amount   

        def drop(self, item, qty=1):
            if self.qty(item):
                item_location = self.check(item)
                if self.inv[item_location][1] > qty:
                    self.inv[item_location][1] -= qty
                else:
                    del self.inv[item_location]

        def qty(self, item):
            """Returns quantity"""
            for i in self.inv:
                if i[0] == item:
                    return i[1]

        def sell(self, item, price):
            self.withdraw(price)
            self.drop(item[0])

        def sort_name(self):
            self.inv.sort(key=lambda i: i[0].name, reverse=self.sort_order)

        def sort_qty(self):
            self.inv.sort(key=lambda i: i[1], reverse=self.sort_order)

        def sort_value(self):
            self.inv.sort(key=lambda i: i[0].value, reverse=self.sort_order)

        def take(self, item, qty=1):
            if self.qty(item):
                item_location = self.check(item)
                self.inv[item_location][1] += qty
            else:
                self.inv.append([item,qty])

        def withdraw(self, amount):
            self.money += amount
            
    def calculate_price(item, buyer):
        """Calculate price"""
        if buyer:
            price = item[0].value * (buyer.barter * 0.01)
            return int(price)
        
    def money_transfer(depositor, withdrawer, amount):
        """Money transfer"""
        if depositor.money >= amount:
            depositor.deposit(amount)
            withdrawer.withdraw(amount) 
        else:
            message = _("Sorry, %s doesn't have %d!") % (buyer.name, amount)
            renpy.show_screen("inventory_popup", message=message) 

    def trade(seller, buyer, item):
        """Trade"""
        seller.drop(item[0])
        buyer.take(item[0])
        
    def transaction(seller, buyer, item):
        """Transaction"""
        price = calculate_price(item, buyer)
        if buyer.money >= price:
            seller.sell(item, price)
            buyer.buy(item, price)
        else:
            message = _("Sorry, %s doesn't have enough money!") % (buyer.name)
            renpy.show_screen("inventory_popup", message = message)

    transfer_amount = 0
