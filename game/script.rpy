# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

######### DEFINE INVENTORIES ##########    
define mc_inventory_name = __("MC Inventory")
default mc_inventory = Inventory(mc_inventory_name)


# The game starts here.

label start:
    ## If using the crafting feature, add an empty cookbook list after start to keep track of recipes
    $ cookbook = list() 
      
    menu:
        "Feature demo":
            pass
        "Skip demo":
            jump skip_demo
    
label demo:    
    # Display an inventory by using the inventory object name as the parameter  
    "For this demo the inventory_screen modal has been set to False (line 150 of inventory.rpy)."
    show screen inventory_screen(mc_inventory)         
    
    "Let's add some items to Jane's inventory. The format is item, quantity."
    $ mc_inventory.take("coin",4)
    $ mc_inventory.take("sword")
    $ mc_inventory.take("eye")
    $ mc_inventory.take("but",2)
    $ mc_inventory.take("fabric",3)
    $ mc_inventory.take("yarn",2)        
      
    "You can hover over the items to see a description. If you click on the sword you will perform the action associated with that item (show a screen with a message).  You can sort inventory several ways and can switch between a grid and list view. If you're using text items you'll only want to enable the list view."  
    
    "Now, let's remove a coin."
    $ mc_inventory.drop("coin")   
    
    "We can also check to see if Jane has a certain item.  The check function returns the quantity, if any."    
    if mc_inventory.qty("coin"): 
        $ qty = mc_inventory.qty("coin")
        "Jane still has [qty] coins. Good job, Jane."
    else:
        "Jane doesn't have any coins. You must have changed this script!"   

    if mc_inventory.qty("but"):
        $ qty = mc_inventory.qty("but")
        "Jane has [qty] buttons."
    else:
        "Jane doesn't have any buttons."
        
    "You can also change an item and modify the name, description, and icon if you need to."
    $ sword.change("Broken sword", "This sword is old and busted.", "images/broke_sword.png", 50, act=Show("inventory_popup", message="It's broken, be careful!"))
    
    "Now the sword is broken and you can't even wave it around anymore.  Let's sell it and buy something else."
    
    "We'll create a vendor named Mindy and give her money and inventory.  Mindy really likes eyes and buttons. Her barter percentage is 75, so she will only buy items from Jane at 75 percent of their value."
    $ mindy_inv = Inventory("Mindy", 500, 75)
    $ mindy_inv.take("eye",4)
    $ mindy_inv.take("but",3)
    $ mindy_inv.take("coin",2)    
    
    # vendor screen parameters are left-side inventory, right-side inventory
    show screen inventory_screen(mc_inventory, mindy_inv)
    
    "Now we'll give Jane some walking-around money."
    $ mc_inventory.money = 500    
    
    "The inventory screen can take two inventory parameters and display the inventories side-by-side. You can click an item to buy/sell between the two.  Neither character can buy items if they don't have enough money.  Trade mode allows you to exchange items without money and bank mode allows withdrawing and depositing money."    
    
    $ chest = Inventory("Storage Chest")

    "Using trade and bank modes together, you can create a storage chest."
    show screen inventory_screen(mc_inventory, chest, trade_mode=True, bank_mode=True)    
    
    "That's it! Exit to end the demo when you are finished."    
    
    show screen overlay
    
label skip_demo:    
    $ mc_inventory.take("coin",4)
    $ mc_inventory.take("sword")
    $ mc_inventory.take("eye")
    $ mc_inventory.take("but",2)
    $ mc_inventory.take("fabric",3)
    $ mc_inventory.take("yarn",2)   
    
    $ mc_inventory.money = 500  
    $ mindy_inv = Inventory("Mindy", 500, 75)
    $ mindy_inv.take("eye",4)
    $ mindy_inv.take("but",3)
    $ mindy_inv.take("coin",2)
    
    $ chest = Inventory("Storage Chest")    
    
    call screen room_navigation

screen room_navigation():
    modal True
    # Tools
    frame:
        yalign 0.0 xalign 0.0
        hbox:
            textbutton "Inventory" action Show("inventory_screen", first_inventory=mc_inventory)
            textbutton "Vendor" action Show("inventory_screen", first_inventory=mc_inventory, second_inventory=mindy_inv)
            textbutton "Trade" action Show("inventory_screen", first_inventory=mc_inventory, second_inventory=mindy_inv, trade_mode=True)
            textbutton "Storage/Bank" action Show("inventory_screen", first_inventory=mc_inventory, second_inventory=chest, trade_mode=True, bank_mode=True) 
            textbutton "Exit" action Quit(confirm=False)
    hbox:
        align (0.99, 0.01)
        spacing 2

        # Money
        text __("$[mc_inventory.money]"):
            align(1.0, 0.5)
            font 'DejaVuSans.ttf'
            size 30
            drop_shadow [(2, 2)]
