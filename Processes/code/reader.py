"""
Author      :Birhan Tesfaye
Last Edit   :May 23
"""

import fitz
import os


def check_validity(pdf_name,filetypes):
    file,ext=os.path.splitext(pdf_name)
    valid=False
    if(ext in filetypes):
        valid=True
    return valid

def converter(doc):
    try:
        newDoc=doc.convertToPDF()
        converted=fitz.open('pdf',newDoc)
        toc=doc.getToC()
        converted.setToC(toc)
        for page in doc:
            links=page.getLinks()
            newpage=converted[page.number]
            for l in links:
                if(l["kind"]==fitz.LINK_NAMED):
                    continue
                newpage.insertLink(l)
    except Exception:
        converted=None
    return converted

def None_to_bool(value):
    if(value):
        value=True
    else:
        value=False
    return value

class Read:
    def __init__(self , pdf_name=None):
        self.status=True
        self.doc=None
        self.pdf_name=pdf_name
        self.filetypes=[".pdf",".xps",".oxps",".cbz",".fb2",".epub"]


    def open(self):
        self.status=check_validity(self.pdf_name,self.filetypes)
        if(self.status):
            try:
                self.doc=fitz.open(self.pdf_name)
                self.encrypted=self.doc.isEncrypted
                self.status=True
            except Exception:
                self.status=False

    def convert(self):
        not_pdf=not self.doc.isPDF
        if(not_pdf):
            try:
                doc=converter(self.doc)
                if(doc is not None):
                    self.doc=doc
                    self.status=True
                else:
                    self.status=False
            except Exception:
                self.status=False

    def isEncrypted(self):
        return self.doc.isEncrypted

    def decrypt(self , password):
        state=self.doc.authenticate(password)
        if(state==2 or state==4):
            self.status=True
        else:
            self.status=False
        return self.status
