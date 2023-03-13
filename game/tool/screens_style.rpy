define gui.lateralframescroll_ysize = 850
define gui.little_text_size = 18
define gui.normal_text_size = 24
define gui.big_normal_text_size = 28
define gui.hour_text_size = 60

image gui triangular_button = "/interface/button/triangular_button.webp"

style menu_vscroll is vscrollbar:
    xsize 7
    unscrollable 'hide'

init:
    transform close_zoom:
        xanchor 25
        size (75, 25)
        on idle:
            yanchor 0 matrixcolor BrightnessMatrix(0)
        on hover:
            yanchor 0 matrixcolor BrightnessMatrix(0.9)
    transform close_zoom_mobile:
        xanchor 35
        size (105, 35)
        on idle:
            yanchor 0 matrixcolor BrightnessMatrix(0)
        on hover:
            yanchor 0 matrixcolor BrightnessMatrix(0.9)
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
