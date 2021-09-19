"""
Author      :Birhan Tesfaye
Last Edit   :May 23
"""

ENCODING = "UTF-8"

def flags_decomposer(flags):
    """Make font flags human readable."""
    l = []
    if flags & 2 ** 0:
        l. append("superscript")
    if flags & 2 ** 1:
        l. append("italic")
    if flags & 2 ** 2:
        l. append("serifed")
    else:
        l. append("sans")
    if flags & 2 ** 3:
        l. append("monospaced")
    else:
        l. append("proportional")
    if flags & 2 ** 4:
        l. append("bold")
    style=l
    return style




