"""
Author      :Birhan Tesfaye
Last Edit   :May 23
"""
from django.contrib import messages
from .common import get_text

"""
USE:
extract = Extract("request",read.doc)
error, doc_text=extract.main(2,4)
"""

class Extract:
    def __init__(self, request, doc):
        self.doc = doc
        self.request=request
        self.toc = self.doc.getToC(simple=False)
        #self.update_toc()
        self.get_heading_toc()
        self.headings=[]

    def check_toc(self):
        status=True
        if(len(self.toc)==0):
            status=False
        return status


    def font_size(self, font_styles):
        return font_styles

    def strip(self, List):
        values = [[],'',(),{},('')]
        for i,item in enumerate(List.copy()):
            for value in values:
                if(value==item or value==item[0]):
                    List.remove(item)
                    break


    def update_toc(self):
        if(self.toc[0][3]['page']==1):
            for index,toc in enumerate(self.toc.copy()):
                toc[2] -= 1
                self.toc[index]=toc

    def check_heading(self, toc, lvls):
        heading=toc[0]
        status=False
        for lvl in lvls:
            if(heading==lvl):
                status=True
                break
        return status

    def get_heading_toc(self,lvl=[1]):
        self.heading_toc=[]
        for i,toc in enumerate(self.toc):
            if(self.check_heading(toc, lvl)):
                value=(toc[1],i)
                self.heading_toc.append(value)

    def extract(self, start, end):
        doc_text, font_styles = get_text(self.doc, start, end)
        self.error = False
        try:
            self.doc_text=doc_text
            self.font_styles=font_styles
            if(self.doc_text==[]):
                messages.warning(self.request,"You don't have text extracted please try another text file")
                self.error=True
        except Exception:
            messages.warning(self.request,"Problem while extracting")
            self.error=True
            self.doc_text = []
            self.font_styles = []
        return self.error

    def main(self, start, end=None):
        start_index=int(start)
        if(end == -1):
            end_index=len(self.toc)-1
        else:
            end_index=int(end)
        self.working_toc=self.toc[start_index:end_index+1]
        start_pno=self.working_toc[0][3]['page']
        end_pno=self.working_toc[-1][3]['page']
        self.page_diff=start_pno
        self.extract(start_pno, end_pno)
        return self.error, self.doc_text





