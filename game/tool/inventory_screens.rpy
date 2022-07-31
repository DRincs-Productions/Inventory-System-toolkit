define INVENTORY_COLUMN_NUMBER = 6

init:
    transform close_zoom:
        size ((105, 35) if renpy.variant("small") else (75, 25))
        xanchor (35 if renpy.variant("small") else 25)

    transform things:
        on selected_idle:
            # matrixcolor SaturationMatrix(0.0)
            zoom 0.9
        on idle:
            # matrixcolor SaturationMatrix(0.0)
            zoom 0.9
        on hover:
            matrixcolor SaturationMatrix(1.0)
            zoom 1.0
        on selected_hover:
            matrixcolor SaturationMatrix(1.0)
            zoom 1.0

style invstyle_frame:
    xalign 0.5
    yalign 0.5
    
style invstyle_label_text:
    size 30
    
style invstyle_label:
    xalign 0.5

screen tooltip(item = False, seller = False):
    if item:
        hbox:
            xalign 0.5 yalign 0.9
            $ val_name = inventory_items[item].name
            $ val_description = inventory_items[item].description
            if seller:
                text ("[val_name]: [val_description] (Sell Value: " + str(seller.calculatePrice(item)) + ")")
            else:
                text "[val_name]: [val_description]"
            $ del val_name
            $ del val_description

screen inventory_screen(first_inventory, second_inventory=None, trade_mode=False, bank_mode=False, sell_and_buy = False):
    # add '/gui/overlay/game_menu.png'
    style_prefix 'inventory'
    tag menu
    frame:
        area (150, 95, 350, 50)
        background None
        text _("THE STUFF") color gui.accent_color size 28 #font 'hermes.ttf'

    # button for closure
    imagebutton:
        pos (1740, 100)
        idle '/interface/button/close_idle.webp'
        hover '/interface/button/close_hover.webp'
        action [Hide('inventory_screen')]
        if renpy.variant("pc"):
            focus_mask True
            at close_zoom
        else:
            at close_zoom_mobile

    # modal False
    frame:
        style_group "invstyle"
        hbox:
            spacing 25
            if (second_inventory and sell_and_buy) or not second_inventory or trade_mode:
                vbox:
                    label first_inventory.name
                    if second_inventory:
                        use money(first_inventory, second_inventory, bank_mode)
                    use inventory_view(first_inventory, second_inventory, trade_mode)
                    use view_nav(first_inventory)
            if second_inventory:
                vbox:
                    label second_inventory.name
                    use money(second_inventory, first_inventory, bank_mode)
                    use inventory_view(second_inventory, first_inventory, trade_mode)
                    use view_nav(second_inventory)

screen inventory_view(inventory, second_inventory=False, trade_mode=False):
    # Necessary otherwise cause: Grid not completely full. (in renpy the grid not is smart)
    $ max_item_number = getItemNumberInInventory(inventory)
    $ grid_column_number = max_item_number
    if (max_item_number % INVENTORY_COLUMN_NUMBER > 0):
        $ grid_column_number = max_item_number + (INVENTORY_COLUMN_NUMBER - (max_item_number % INVENTORY_COLUMN_NUMBER))
    $ list_item_key = list(inventory.getValues().keys())
    side "c r":
        style_group "invstyle"
        area (0, 0, 700, 500)
        vpgrid id ("vp"+inventory.name):
            draggable True   
            mousewheel True
            xsize 700
            ysize 500
            if (grid_column_number == 0):
                cols 1
            elif inventory.grid_view:
                cols INVENTORY_COLUMN_NUMBER
                spacing 10
            else:
                cols 1
                spacing 25
            for index in range(grid_column_number):
                hbox:
                    if (len(list_item_key) > index):
                        $ item = list_item_key[index-1]
                        $ name = inventory_items[item].name
                        $ description = inventory_items[item].description
                        $ value = inventory_items[item].value
                        $ quantity = str(inventory.getQuantity(item))
                        if inventory_items[item].icon:
                            $ icon = inventory_items[item].icon
                            $ hover_icon = im.Sepia(icon)
                            imagebutton:
                                idle LiveComposite((100,100), (0,0), icon, (0,0), Text(quantity))
                                hover LiveComposite((100,100), (0,0), hover_icon, (0,0), Text(quantity))
                                action If(second_inventory, If(trade_mode, Function(trade, inventory, second_inventory, item), Function(transaction, inventory, second_inventory, item)), Show("popup", message=description))
                                hovered Show("tooltip", item = item, seller = inventory)
                                unhovered Hide("tooltip")
                                at things
                            if not inventory.grid_view:
                                vbox:
                                    text name
                                    if not trade_mode:
                                        # text "List Value: [value]"
                                        if second_inventory:
                                            text ("Sell Value: " + str(inventory.calculatePrice(item)))
                        else:                               
                            textbutton "[name] ([quantity])":
                                action If(second_inventory, If(trade_mode and second_inventory, Function(trade, inventory, second_inventory, item), Function(transaction, inventory, second_inventory, item)), Show("popup", message=description))
                                hovered Show("tooltip", item=item, seller=inventory)
                                unhovered Hide("tooltip")
                            if not inventory.grid_view:
                                vbox:                        
                                    text "List Value: [value]"
                                    if not trade_mode and second_inventory:
                                        text "Sell Value: " + str(inventory.calculatePrice(item)) + ")"
            ## maintains spacing in empty inventories.
            if getItemNumberInInventory(inventory) == 0:
                add Null(height = 100, width = 100)

        vbar value YScrollValue("vp"+inventory.name)

screen money(inventory, second_inventory, bank_mode=False):
    hbox:
        style_group "invstyle"
        text "Money: [inventory.money]"
        if bank_mode and inventory.money:
            textbutton "Transfer" action Show("banking", depositor=inventory, withdrawer=second_inventory)

define transfer_amount = 0
screen banking(depositor, withdrawer):
    modal True
    frame:
        style_group "invstyle"
        vbox:
            label "Money Transfer"
            text "Amount: [transfer_amount]"
            bar value VariableValue("transfer_amount", int(depositor.money), max_is_zero=False, style='scrollbar', offset=0, step=0.1) xmaximum 200

            # Examples of the types of controls you can set up
            hbox: 
                for amount in [50,100,250,depositor.money]:
                    if depositor.money>=amount:
                        textbutton str(amount) action SetVariable("transfer_amount", amount)
            hbox:
                textbutton "Transfer" action [Function(moneyTransfer, depositor, withdrawer, transfer_amount), SetVariable("transfer_amount", 0), Hide("banking")]
                textbutton "Cancel" action Hide("banking")

screen view_nav(inventory):
    hbox:
        text "View: "
        textbutton "Grid" action SetField(inventory, "grid_view", True)
        textbutton "List" action SetField(inventory, "grid_view", False)

screen sort_nav(inventory):
    hbox:
        text "Sort: "
        textbutton "Name" action [ToggleField(inventory, "sort_by", inventory.sort_name), inventory.sort_name]
        textbutton "quantity" action [ToggleField(inventory, "sort_by", inventory.sort_qty), inventory.sort_qty]
        textbutton "Val" action [ToggleField(inventory, "sort_by", inventory.sort_value), inventory.sort_value]
        if inventory.sort_order:
            textbutton "asc." action [ToggleField(inventory, "sort_order"), inventory.sort_by]
        else:
            textbutton "des." action [ToggleField(inventory, "sort_order"), inventory.sort_by]
