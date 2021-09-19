from .common import similar
from .common import get_text
from .font import flags_decomposer
class Content:
    def __init__(self, keyword):
        self.keyword = keyword
        self.doc_text=[]

    def get_text(self, doc, init, final):
        for page in doc.pages(init, final):
            page_text = []
            getpage = page.get_text("dict")
            blocks = getpage["blocks"]
            for block in blocks:
                block_text=''
                if ("lines" in block.keys()):
                    lines = block['lines']
                    for line in lines:
                        if ("spans" in line.keys()):
                            spans = line["spans"]
                            for span in spans:
                                text = span['text']
                                block_text+=text
                                block_text+=' '
                block_text=block_text.strip()
                page_text.append(block_text)
            self.doc_text.append(page_text)

    def get_content(self, doc):
        toc=doc.getToC()
        similarity = []
        for i,value in enumerate(toc):
            heading = value[1]
            count = similar(heading, self.keyword)
            pno=value[2]
            try:
                next_pno = toc[i+1][2]
            except Exception:
                next_pno = doc.pageCount
            count = (count, pno, next_pno)
            similarity.append(count)
        if len(toc)>1:
            similarity.sort(key = lambda value:value[0])
            value = similarity[0]
            pno = value[1]
            next_pno = value[2]
            self.get_text(doc, pno, next_pno)




def correct_toc(doc):
    toc = []
    start = 0
    end = doc.pageCount
    doc_text, font_styles = get_text(doc, start, end)
    prev = 0
    prev_o={}
    for i,page_text in enumerate(doc_text):
        for block_text in page_text:
            text = block_text[0]
            size = block_text[1]
            if (size in font_styles[:6]):
                index = font_styles.index(size)
                lvl = index+1
                heading = [lvl, text, i]
                toc.append(heading)

    for i,heading in enumerate(toc.copy()):
        lvl = heading[0]


    return toc






