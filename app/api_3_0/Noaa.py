#coding=utf8
from . import api3


import json

import pytz

tz = pytz.timezone("GMT")







@api3.route("/aurora/color")
def auroraColor():
    list = []
    for i in range(0,101):
        color = hex(aururo_to_rgb(i))
        list.append(color)
    print(list)
    return json.dumps(list)





def aururo_to_rgb(elevation):

    if elevation < 1:
        return 0

    normalized_value = elevation

    breakpoints = [

        (0,(126,161,140)),
        (10,(1,228,0)),
        (30,(58,255,5)),
        (50, (255,251,0)),
        (70, (255,166,2)),
        (90, (250,1,0)),
        (101, (177,32,0))


    ]



    # Find the two neighboring breakpoints for the normalized value
    prev_breakpoint, prev_color = breakpoints[0]
    for next_breakpoint, next_color in breakpoints[1:]:
        if normalized_value < next_breakpoint:
            break
        prev_breakpoint, prev_color = next_breakpoint, next_color

    # Interpolate between the neighboring colors
    prev_normalized, prev_rgb = prev_breakpoint, prev_color
    next_normalized, next_rgb = next_breakpoint, next_color
    t = (normalized_value - prev_normalized) / (next_normalized - prev_normalized)

    r = prev_rgb[0] + int((next_rgb[0] - prev_rgb[0]) * t)
    g = prev_rgb[1] + int((next_rgb[1] - prev_rgb[1]) * t)
    b = prev_rgb[2] + int((next_rgb[2] - prev_rgb[2]) * t)

    # Clamp the RGB values to the valid range (0-255)
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))

    return b + g * 256 + r * 256 * 256 + 255 * 256 * 256 * 256


