######### DEFINE ITEM OBJECTS ##########
### The format is name, description, icon image (if applicable), value (if applicable, selling/buying value), action (screen language action to be performed when icon is clicked on inventory screen), and recipe (if craftable).

### Items without icons are created like this:      
#$ quarter = Item("Quarter", "A new quarter)

define inventory_items = {
    ### Items with icons are created like this:
    "eye"       :   Item(name=__("Eyeball"), description=__("A human eyeball, how creepy!"), icon="images/eye.webp", value=250),
    # Items that can be used in crafting
    "but"       :   Item(__("Button"), __("A shiny button"), "images/button.webp", 100, act = Show("inventory_popup", message = __("This item is only used in crafting"))),
    "yarn"      :   Item(__("Yarn"), __("Yarny yarny yarn."), "images/yarn.webp", 30, act = Show("inventory_popup", message = __("This item is only used in crafting"))),
    "fabric"    :   Item(__("Fabric"), __("You know, cloth."), "images/fabric.webp", 100, act = Show("inventory_popup", message = __("This item is only used in crafting"))),
    "coin"      :   Item(__("Coin"), __("An old coin"), "images/coin.webp", 1, act = Show("inventory_popup", message = __("This item is only used in crafting"))),
    # An item with a unique action (shows screen with custom message)
    "sword"     :   Item(__("Awesome Sword"), __("An awesome sword."), "images/sword.webp", 500, Show("inventory_popup", message = __("You wave the sword around wildly but nothing happens."))),
    # An item that can be crafted has a recipe, which is a nested list of [ingredient, qty]
    # "necklace"  :   Item("Penny Necklace", "Super magic.", "images/necklace.webp", 50, recipe = [[coin,6],[yarn,1]]),
    # "doll"      :   Item("Handmade Doll", "Guaranteed to bring luck. (Or not?) Very huggable, mind the needle.", "images/doll.webp", 100000, recipe = [[but,2],[fabric,3],[yarn,1]]),
}

######### DEFINE INVENTORIES ##########    
define mc_inventory_name = __("MC Inventory")
default mc_inventory = Inventory(name="[mc_inventory_name]", money=500, barter=100,
    inv = {
        "coin":     4,
        "sword":    1,
        "eye":      1,
        "but":      2,
        "fabric":   3,
        "yarn":     2,
    }
)

define mindy_inventory_name = __("Mindy")
default mindy_inv = Inventory(name="[mindy_inventory_name]", money=500, barter=75,
    inv = {
        "eye":      4,
        "but":      3,
        "coin":     2,
    }
)

define chest_inventory_name = __("Storage Chest")
default chest = Inventory(name="[chest_inventory_name]")
    
