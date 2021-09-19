import fitz
from nltk import word_tokenize

"""USE:
write=Write()
write.main(doc_text)
write.save(path)
"""
class Write:
    def __init__(self):
        self.fonts = [12, 14, 16, 18, 20, 22, 24, 26]
        self.totals = [102, 104, 106, 108, 110, 112, 114, 116]
        self.unit_heights = [13, 14, 15, 16, 17, 18, 19, 20]
        self.default_height=50
        self.gap=24
        self.prev_height=self.default_height
        self.doc=None

    def newPage(self):
        page = self.doc.newPage()
        shape = page.newShape()
        self.shape = shape


    def font_style(self, style):
        if(style=='para'):
            font=self.fonts[0]
        elif(style=='heading_5'):
            font=self.fonts[1]
        elif (style == 'heading_4'):
            font=self.fonts[2]
        elif(style=='heading_3'):
            font=self.fonts[3]
        elif (style == 'heading_2'):
            font=self.fonts[4]
        elif (style == 'heading_1'):
            font=self.fonts[5]
        elif (style == 'heading_0'):
            font=self.fonts[6]
        else:
            font=self.fonts[0]
        return font


    def insertText(self, rect, block_text, font_size, align):
        diff = self.shape.insertTextbox(rect, block_text, fontname="helv", fontsize=font_size, encoding=fitz.TEXT_ENCODING_LATIN, align=align)
        if(diff>=0):
            self.shape.commit()
        return diff

    def write(self, block):
        text= block[0]
        if(block[1].startswith('heading')):
            align=fitz.TEXT_ALIGN_CENTER
            self.prev_height+=12
        else:
            align=fitz.TEXT_ALIGN_LEFT
        font_size=self.font_style(block[1])
        total_height =self.write_style(text, font_size, align)
        return total_height

    def write_style(self, text, font_size, align):
        total_height=self.prev_height+1
        rect = fitz.Rect(25,self.prev_height,570,total_height)
        diff=self.insertText(rect, text, font_size, align)
        total_height-=diff
        if(total_height>750):
            self.newPage()
            diff=self.prev_height-self.default_height
            total_height-=diff
            self.prev_height=self.default_height
        rect = fitz.Rect(25,self.prev_height,570,total_height)
        diff = self.insertText(rect, text, font_size, align)
        return total_height

    def main(self, doc_text):
        self.doc=fitz.open()
        self.newPage()
        for i,text in enumerate(doc_text):
            last_point = self.write(text)
            self.prev_height=last_point +self.gap

    def save(self, path):
        self.doc.save(path)

