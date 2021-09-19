def SortBlocks(blocks):
    sblocks = []
    for b in blocks:
        x0 = str(int(b["bbox"][0]+0.99999)).rjust(4,"0") # x coord in pixels
        y0 = str(int(b["bbox"][1]+0.99999)).rjust(4,"0") # y coord in pixels
        sortkey = y0 + x0                                # = "yx"
        sblocks.append([sortkey, b])
    sblocks.sort(key=lambda line:line[0])
    return [b[1] for b in sblocks] # return sorted list of blocks

def SortLines(lines):
    ''' Sort the lines of a block in ascending vertical direction. See comment
    in SortBlocks function.
    '''
    slines = []
    for l in lines:
        y0 = str(int(l["bbox"][1] + 0.99999)).rjust(4,"0")
        slines.append([y0, l])
    slines.sort(key=lambda line:line[0])
    return [l[1] for l in slines]

def SortSpans(spans):
    ''' Sort the spans of a line in ascending horizontal direction. See comment
    in SortBlocks function.
    '''
    sspans = []
    for s in spans:
        x0 = str(int(s["bbox"][0] + 0.99999)).rjust(4,"0")
        sspans.append([x0, s])
    sspans.sort(key=lambda line:line[0])
    return [s[1] for s in sspans]

