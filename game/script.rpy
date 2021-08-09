## inventory 1.5 demo
      
 
      
label start:  
    ## If using the crafting feature, add an empty cookbook list after start to keep track of recipes
    $ cookbook = list() 
   
    ######### DEFINE INVENTORIES ##########    
    $ jane_inv = Inventory("Jane")
    
    ######### DEFINE ITEM OBJECTS ##########
    ### The format is name, description, icon image (if applicable), value (if applicable, selling/buying value), action (screen language action to be performed when icon is clicked on inventory screen), and recipe (if craftable).
    
    ### Items without icons are created like this:      
    #$ quarter = Item("Quarter", "A new quarter)
    
    ### Items with icons are created like this:
    $ eye = Item(name="Eyeball", description="A human eyeball, how creepy!", icon="images/eye.png", value=250)

    # Items that can be used in crafting
    $ but = Item("Button", "A shiny button", "images/button.png", 100, act=Show("inventory_popup", message="This item is only used in crafting"))
    
    $ yarn = Item("Yarn", "Yarny yarny yarn.", "images/yarn.png", 30, act=Show("inventory_popup", message="This item is only used in crafting"))  
    
    $ fabric = Item("Fabric", "You know, cloth.", "images/fabric.png", 100, act=Show("inventory_popup", message="This item is only used in crafting"))
    
    $ coin = Item("Coin", "An old coin", "images/coin.png", 1, act=Show("inventory_popup", message="This item is only used in crafting"))
    
    # An item with a unique action (shows screen with custom message)
    $ sword = Item("Awesome Sword", "An awesome sword.", "images/sword.png", 500, Show("inventory_popup", message="You wave the sword around wildly but nothing happens."))

    # An item that can be crafted has a recipe, which is a nested list of [ingredient, qty]
    $ necklace = Item("Penny Necklace", "Super magic.", "images/necklace.png", 50, recipe=[[coin,6],[yarn,1]])    
    $ doll = Item("Handmade Doll", "Guaranteed to bring luck. (Or not?) Very huggable, mind the needle.", "images/doll.png", 100000, recipe=[[but,2],[fabric,3],[yarn,1]])    
      
    menu:
        "Feature demo":
            pass
        "Skip demo":
            jump skip_demo
    
label demo:    
    # Display an inventory by using the inventory object name as the parameter  
    "For this demo the inventory_screen modal has been set to False (line 150 of inventory.rpy)."
    show screen inventory_screen(jane_inv)         
    
    "Let's add some items to Jane's inventory. The format is item, quantity."
    $ jane_inv.take(coin,4)
    $ jane_inv.take(sword)
    $ jane_inv.take(eye)
    $ jane_inv.take(but,2)
    $ jane_inv.take(fabric,3)
    $ jane_inv.take(yarn,2)        
      
    "You can hover over the items to see a description. If you click on the sword you will perform the action associated with that item (show a screen with a message).  You can sort inventory several ways and can switch between a grid and list view. If you're using text items you'll only want to enable the list view."  
    
    "Now, let's remove a coin."
    $ jane_inv.drop(coin)   
    
    "We can also check to see if Jane has a certain item.  The check function returns the quantity, if any."    
    if jane_inv.qty(coin): 
        $ qty = jane_inv.qty(coin)
        "Jane still has [qty] coins. Good job, Jane."
    else:
        "Jane doesn't have any coins. You must have changed this script!"   

    if jane_inv.qty(but):
        $ qty = jane_inv.qty(but)
        "Jane has [qty] buttons."
    else:
        "Jane doesn't have any buttons."
        
    "You can also change an item and modify the name, description, and icon if you need to."
    $ sword.change("Broken sword", "This sword is old and busted.", "images/broke_sword.png", 50, act=Show("inventory_popup", message="It's broken, be careful!"))
    
    "Now the sword is broken and you can't even wave it around anymore.  Let's sell it and buy something else."
    
    "We'll create a vendor named Mindy and give her money and inventory.  Mindy really likes eyes and buttons. Her barter percentage is 75, so she will only buy items from Jane at 75 percent of their value."
    $ mindy_inv = Inventory("Mindy", 500, 75)
    $ mindy_inv.take(eye,4)
    $ mindy_inv.take(but,3)
    $ mindy_inv.take(coin,2)    
    
    # vendor screen parameters are left-side inventory, right-side inventory
    show screen inventory_screen(jane_inv, mindy_inv)
    
    "Now we'll give Jane some walking-around money."
    $ jane_inv.money = 500    
    
    "The inventory screen can take two inventory parameters and display the inventories side-by-side. You can click an item to buy/sell between the two.  Neither character can buy items if they don't have enough money.  Trade mode allows you to exchange items without money and bank mode allows withdrawing and depositing money."    
    
    $ chest = Inventory("Storage Chest")

    "Using trade and bank modes together, you can create a storage chest."
    show screen inventory_screen(jane_inv, chest, trade_mode=True, bank_mode=True)    
    
    "That's it! Exit to end the demo when you are finished."    
    
    show screen overlay
    
label looping:
    $ renpy.pause()
    jump looping
    
label skip_demo:    
    $ jane_inv.take(coin,4)
    $ jane_inv.take(sword)
    $ jane_inv.take(eye)
    $ jane_inv.take(but,2)
    $ jane_inv.take(fabric,3)
    $ jane_inv.take(yarn,2)   
    
    $ jane_inv.money = 500  
    $ mindy_inv = Inventory("Mindy", 500, 75)
    $ mindy_inv.take(eye,4)
    $ mindy_inv.take(but,3)
    $ mindy_inv.take(coin,2)
    
    $ chest = Inventory("Storage Chest")    
    
    show screen overlay    
    show screen inventory_screen(jane_inv, mindy_inv)

    jump looping
    
screen overlay:
    frame:
        yalign 0.0 xalign 0.0
        hbox:
            textbutton "Inventory" action Show("inventory_screen", first_inventory=jane_inv)
            textbutton "Vendor" action Show("inventory_screen", first_inventory=jane_inv, second_inventory=mindy_inv)
            textbutton "Trade" action Show("inventory_screen", first_inventory=jane_inv, second_inventory=mindy_inv, trade_mode=True)
            textbutton "Storage/Bank" action Show("inventory_screen", first_inventory=jane_inv, second_inventory=chest, trade_mode=True, bank_mode=True) 
            textbutton "Exit" action Quit(confirm=False)