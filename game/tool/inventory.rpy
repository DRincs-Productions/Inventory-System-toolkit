##Ren'Py Inventory System v. 1.5 provided under public domain by saguaro

init python: 
    import renpy.store as store    
    
    class Item(store.object):
        def __init__(self, name, desc, icon=False, value=0, act=Show("inventory_popup", message="Nothing happened!"), type="item", recipe=False):
            global cookbook
            self.name = name
            self.desc = desc
            self.icon = icon
            self.value = value               
            self.act = act # screen action
            self.type = type # type of item
            self.recipe = recipe # nested list of [ingredient, qty]   
            
            if recipe:
                cookbook.append(self)
                cookbook.sort(key=lambda i: i.name) #alpha order

        def change(self, name, desc=False, icon=False, value=False, act=False, recipe=False): 
            self.name = name
            if desc:
                self.desc = desc
            if icon:
                self.icon = icon
            if value:
                self.value = value   
            if act:
                self.act = act
            if recipe:
                self.recipe = recipe                
            
    class Inventory(store.object):
        def __init__(self, name, money=0, barter=100):
            self.name = name
            self.money = money
            self.barter = barter #percentage of value paid for items            
            self.inv = []  # items stored in nested list [item object, qty]
            self.sort_by = self.sort_name
            self.sort_order = True #ascending, descending
            self.grid_view = True
            
        def buy(self, item, price):            
            self.deposit(price)            
            self.take(item[0])                

        def check(self, item):
            if self.qty(item):
                for i in self.inv:
                    if i[0] == item:        
                        return self.inv.index(i) # returns item index (location)            
            
        def check_recipe(self, item): # verify all ingredients are in inv
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
            message = "Crafted a %s!" % (item.name)
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
            for i in self.inv:
                if i[0] == item:   
                    return i[1] # returns quantity   
                    
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
        if buyer:
            price = item[0].value * (buyer.barter * 0.01)
            return int(price)
        
    def money_transfer(depositor, withdrawer, amount):
        if depositor.money >= amount:
            depositor.deposit(amount)
            withdrawer.withdraw(amount) 
        else:
            message = "Sorry, %s doesn't have %d!" % (buyer.name, amount) 
            renpy.show_screen("inventory_popup", message=message) 

    def trade(seller, buyer, item):
        seller.drop(item[0])
        buyer.take(item[0])              
        
    def transaction(seller, buyer, item):
        price = calculate_price(item, buyer)
        if buyer.money >= price:   
            seller.sell(item, price)
            buyer.buy(item, price)
        else:
            message = "Sorry, %s doesn't have enough money!" % (buyer.name)
            renpy.show_screen("inventory_popup", message=message)

    transfer_amount = 0
