# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.


# The game starts here.

label start:
    ## If using the crafting feature, add an empty cookbook list after start to keep track of recipes
    $ cookbook = list() 

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
