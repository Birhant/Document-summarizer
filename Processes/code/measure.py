import fitz
from nltk import word_tokenize

class PPT_page:
    def __init__(self):
        self.size=300
    def write(self,text):
        output=['']
        index=0
        total=0
        tokens=word_tokenize(text)
        for token in tokens:
            total+=len(token)+1
            if(total>self.size):
                token+=' '
                output.append(token)
                total=len(token)+1
                index+=1
            else:
                token+=' '
                output[index]+=token
        return output
ppt=PPT_page()