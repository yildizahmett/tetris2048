from lib.color import Color

TILE_COLORS = {
        2: {
        "background_color": Color(238, 228, 218),
        "foreground_color": Color(138, 129, 120)
        },
        4:{
        "background_color": Color(236, 224, 200),
        "foreground_color": Color(138, 129, 120)
        },
        8:{
        "background_color": Color(243, 177, 121),
        "foreground_color": Color(255, 255, 255)
        },
        16:{
        "background_color": Color(245, 150, 98),
        "foreground_color": Color(255, 255, 255)
        },
        32:{
        "background_color": Color(249, 123, 97),
        "foreground_color": Color(255, 255, 255)
        },
        64:{
        "background_color": Color(245, 100, 60),
        "foreground_color": Color(255, 255, 255)
        },
        128:{
        "background_color": Color(238, 228, 218),
        "foreground_color": Color(255, 255, 255)
        },
        256:{
        "background_color": Color(237, 203, 99),
        "foreground_color": Color(255, 255, 255)
        },
        512:{
        "background_color": Color(238, 201, 84),
        "foreground_color": Color(255, 255, 255)
        },
        1024:{
        "background_color": Color(239, 196, 64),
        "foreground_color": Color(255, 255, 255)
        },
        2048:{
        "background_color": Color(238, 194, 45),
        "foreground_color": Color(255, 255, 255)
        }
}

def get_next_display_dict(grid_width):
    TILE_NEXT_DISPLAY = {
        "I":{
            'x': grid_width + 1,
            'y': 1
        },
        "J":{
            'x': grid_width + 1.5,
            'y': 2
        },
        "L":{
            'x': grid_width + 0.5,
            'y': 2
        },
        "O":{
            'x': grid_width + 1.5,
            'y': 3
        },
        "T":{
            'x': grid_width + 1,
            'y': 3
        },
        "S":{
            'x': grid_width + 1,
            'y': 2
        },
        "Z":{
            'x': grid_width + 1,
            'y': 2
        }
    }
    return TILE_NEXT_DISPLAY