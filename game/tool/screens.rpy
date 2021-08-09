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


screen tooltip(item=False,seller=false):
    if item:
        hbox:
            xalign 0.5 yalign 0.9
            if seller:
                text ("[item[0].name]: [item[0].description] (Sell Value: " + str(calculate_price(item, seller)) + ")")
            else:
                text "[item[0].name]: [item[0].description]"# (Value: [item[0].value])"

screen inventory_screen(first_inventory, second_inventory=False, trade_mode=False, bank_mode=False):
    add 'interface phon2'
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
            vbox:
                label first_inventory.name
                if second_inventory:
                    use money(first_inventory, second_inventory, bank_mode)
                use inventory_view(first_inventory, second_inventory, trade_mode)
                use view_nav(first_inventory)
                use sort_nav(first_inventory)
            if second_inventory:
                vbox:
                    label second_inventory.name
                    use money(second_inventory, first_inventory, bank_mode)
                    use inventory_view(second_inventory, first_inventory, trade_mode)
                    use view_nav(second_inventory)
                    use sort_nav(second_inventory)

screen inventory_view(inventory, second_inventory=False, trade_mode=False):
    side "c r":
        style_group "invstyle"
        area (0, 0, 700, 500)
        vpgrid id ("vp"+inventory.name):
            draggable True   
            mousewheel True
            xsize 700
            ysize 500
            if inventory.grid_view:
                cols 6
                spacing 10
            else:
                cols 1
                spacing 25
            for item in inventory.inv:
                $ name = item[0].name
                $ description = item[0].description
                $ value = item[0].value
                $ qty = str(item[1])
                hbox:
                    if item[0].icon:
                        $ icon = item[0].icon
                        $ hover_icon = im.Sepia(icon)
                        imagebutton:
                            idle LiveComposite((100,100), (0,0), icon, (0,0), Text(qty))
                            hover LiveComposite((100,100), (0,0), hover_icon, (0,0), Text(qty))
                            action (If(not second_inventory, item[0].act, (If(trade_mode, Function(trade,inventory, second_inventory, item), Function(transaction,inventory, second_inventory, item)))))
                            hovered Show("tooltip", item = item, seller = second_inventory)
                            unhovered Hide("tooltip")
                            at things
                        if not inventory.grid_view:
                            vbox:
                                text name
                                if not trade_mode:
                                    # text "List Value: [value]"
                                    if second_inventory:
                                        text ("Sell Value: " + str(calculate_price(item, second_inventory)))
                    else:                               
                        textbutton "[name] ([qty])":
                            action (If(not second_inventory, item[0].act,(If(trade_mode, Function(trade, inventory, second_inventory, item), Function(transaction,inventory, second_inventory, item)))))
                            hovered Show("tooltip", item=item, seller=second_inventory)
                            unhovered Hide("tooltip")
                        if not inventory.grid_view:
                            vbox:                        
                                text "List Value: [value]"
                                if not trade_mode and second_inventory:
                                    text "Sell Value: " + str(calculate_price(item, second_inventory)) + ")"

            ## maintains spacing in empty inventories.
            if len(inventory.inv) == 0:
                add Null(height=100,width=100)

        vbar value YScrollValue("vp"+inventory.name)

screen money(inventory, second_inventory, bank_mode=False):
    hbox:
        style_group "invstyle"
        text "Money: [inventory.money]"
        if bank_mode and inventory.money:
            textbutton "Transfer" action Show("banking", depositor=inventory, withdrawer=second_inventory)

screen banking(depositor, withdrawer):
    modal True
    frame:
        style_group "invstyle"
        vbox:
            label "Money Transfer"
            text "Amount: [transfer_amount]"
            bar value VariableValue("transfer_amount", depositor.money, max_is_zero=False, style='scrollbar', offset=0, step=0.1) xmaximum 200

            hbox: #examples of the types of controls you can set up
                for amount in [50,100,250,depositor.money]:
                    if depositor.money>=amount:
                        textbutton str(amount) action SetVariable("transfer_amount", amount)
            hbox:
                textbutton "Transfer" action [Function(money_transfer, depositor, withdrawer, transfer_amount), SetVariable("transfer_amount", 0), Hide("banking")]
                textbutton "Cancel" action Hide("banking")

screen crafting(inventory):
    vbox:
        label "Recipes"
        hbox:
            xmaximum 600 xminimum 600 xfill True
            text "Name" xalign 0.5
            text "Ingredients" xalign 0.5
        side "c r":
            area (0,0,600,400)
            viewport id "cookbook":
                draggable True
                mousewheel True
                vbox:
                    for item in cookbook:
                        hbox:
                            first_spacing 25 spacing 10
                            hbox:
                                xmaximum 250 xminimum 250 xfill True box_wrap True
                                if item.icon:
                                    add im.FactorScale(item.icon, 0.33)
                                if inventory.check_recipe(item):
                                    textbutton item.name action Function(inventory.craft,item)
                                else:
                                    text item.name
                            for i in item.recipe: 
                                if i[0].icon:
                                    add im.FactorScale(i[0].icon, 0.33)
                                else:
                                    text i[0].name
                                if inventory.qty(i[0]) >= i[1]:
                                    text "x" + str(i[1]) bold True
                                else:
                                    text "x" + str(i[1])
            vbar value YScrollValue("cookbook") 
        textbutton "Hide" action ToggleScreenVariable("crafting_screen") xalign 0.5

screen view_nav(inventory):
    hbox:
        text "View: "
        textbutton "Grid" action SetField(inventory, "grid_view", True)
        textbutton "List" action SetField(inventory, "grid_view", False)

screen sort_nav(inventory):
    hbox:
        text "Sort: "
        textbutton "Name" action [ToggleField(inventory, "sort_by", inventory.sort_name), inventory.sort_name]
        textbutton "Qty" action [ToggleField(inventory, "sort_by", inventory.sort_qty), inventory.sort_qty]
        textbutton "Val" action [ToggleField(inventory, "sort_by", inventory.sort_value), inventory.sort_value]
        if inventory.sort_order:
            textbutton "asc." action [ToggleField(inventory, "sort_order"), inventory.sort_by]
        else:
            textbutton "des." action [ToggleField(inventory, "sort_order"), inventory.sort_by]

screen inventory_popup(message):
    zorder 100
    frame:
        style_group "invstyle"
        hbox:
            text message
    timer 1.5 action Hide("inventory_popup")
