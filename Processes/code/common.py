from . import font
from .natural_order import SortBlocks
from .natural_order import SortLines
from .natural_order import SortSpans

def strip(List):
    values = [[],'',(),{},('')]
    for i,item in enumerate(List.copy()):
        for value in values:
            if(value==item or value==item[0]):
                List.remove(item)
                break


def get_block_text(block):
    ln_text = ''
    min_size=1000
    if ("lines" in block.keys()):
        lines = SortLines(block["lines"])
        for line in lines:
            if ("spans" in line.keys()):
                spans = SortSpans(line["spans"])
                for span in spans:
                    text = span['text']
                    size = span["size"]
                    min_size=min(size, min_size)
                    flag = font.flags_decomposer(span["flags"])
                    ln_text += text
            ln_text+=r" "
    ln_text.strip()
    block_text=(ln_text, min_size)
    return block_text

def get_text(doc, start, end):
    doc_text = []
    font_styles=[]

    for page in doc.pages(start, end):
        page_text = []
        getpage = page.get_text("dict")
        blocks = getpage["blocks"]
        blocks = SortBlocks(blocks)
        for block in blocks:
            block_text = get_block_text(block)
            page_text.append(block_text)
            size=block_text[1]
            font_styles.append(size)
        strip(page_text)
        doc_text.append(page_text)
    font_styles = set(font_styles)
    font_styles = list(font_styles)
    font_styles.sort(reverse = True)
    return doc_text, font_styles


def similar (t1, t2):
    titles = t1.split(' ')
    texts  = t2.split(' ')
    count=0
    for text in texts.copy():
        if(text in titles):
            titles.remove(text)
            texts.remove(text)
            count+=1
        else:
            count-=1
            texts.remove(text)
    return count
