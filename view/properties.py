from PySide6.QtGui import QBrush, QColor, QPen

class CColor:
    @staticmethod
    def rgb_to_hex(r, g, b):
        return '#%02x%02x%02x' % (r, g, b)

    @staticmethod
    def rgb_to_QColor(r, g, b):
        return QColor(r, g, b)

    @staticmethod
    def hex_to_QColor(hex_code):
        return QColor(hex_code)

    @staticmethod
    def hex_to_rgb(hex_code):
        hex_code = hex_code.lstrip('#') # removes hash if present
        return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))# 16 due to hex



class CColorTheme:
    class DarkMode:
        SHEET_COLOR = "#113311"
        TABLE_TEXT_COLOR = "#BBBBBB"

        BACKGROUND_COLOR = "#181818"
        ACCENT_COLOR = "#4C6663" #C2185B"
        SECONDARY_COLOR = "#424242"
        ON_HOVER_COLOR = "#FFFFFF"


        CANVAS_BACKGROUND_COLOR = "#FFFFFF"
        CANVAS_POINT_COLOR = "#000000"
        CANVAS_PATH_COLOR = "d4c5e2"

        LIGHT_TEXT_COLOR = "#FFFFFF"
        DARK_TEXT_COLOR = "#000000"

        __ACCENT_COLOR_BRIGHTNESS = CColor.hex_to_QColor(ACCENT_COLOR).lightness()
        ACCENT_TEXT_COLOR = DARK_TEXT_COLOR if __ACCENT_COLOR_BRIGHTNESS > 128 else LIGHT_TEXT_COLOR


    class LightMode:
        BACKGROUND_COLOR = "#FFFFFF"
        ACCENT_COLOR = "#FF00FF"#C2185B"
        SECONDARY_COLOR = "#F5F5F5"

        CANVAS_BACKGROUND_COLOR = "#000000"
        POINT_COLOR = "#FFFFFF"
        PATH_COLOR = "#00FF00"

        LIGHT_TEXT_COLOR = "#FFFFFF"
        DARK_TEXT_COLOR = "#000000"

        __ACCENT_COLOR_BRIGHTNESS = CColor.hex_to_QColor(ACCENT_COLOR).lightness()
        ACCENT_TEXT_COLOR = DARK_TEXT_COLOR if __ACCENT_COLOR_BRIGHTNESS > 128 else LIGHT_TEXT_COLOR



class Settings:
    def __init__(self):
        self.color_theme = CColorTheme.DarkMode
        self.font_size_large = 14
        self.font_size_medium = 12
        self.font_size_small = 10
