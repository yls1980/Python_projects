import os
import glob
#import pdftotree
import PyPDF2
import random
import string

def read_files(spath, sformat, b_arch=False):
    files = []
    for file in glob.glob(spath+'\\*', recursive=True):
        if os.path.isfile(file) and os.path.splitext(os.path.basename(file))[1].upper() in sformat:
            files.append(file)
    return files

def pdf_to_html(path_pdf,path_html,sname):
    if not os.path.exists(path_html):
        os.mkdir(path_html)
    if os.path.exists(path_pdf):
        #pdftotree.parse(path_pdf, html_path=path_html, model_type=None, model_path=None, visualize=False)
        pdfFileObj = open(path_pdf, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        print(pdfReader.numPages)
        n = pdfReader.numPages-1
        #digits = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        docInfo = pdfReader.getDocumentInfo()
        try:
            print(docInfo.author, docInfo.creator, docInfo.producer, docInfo.title, docInfo.subject)
        except AttributeError as e:
            pass
        f = open (os.path.join(path_html,sname+'.txt'),'w',encoding='utf-8')
        for i in range(n):
            pageObj = pdfReader.getPage(i)
            f.write(pageObj.extractText())
        f.close()
        pdfFileObj.close()



#files = read_files('y:\\BOOKS\\Telegram\\', sformat=('.PDF'))
files = read_files('e:\\0\\', sformat=('.PDF'))
for file in files:
    pdf_to_html(file, 'o:\\pdf', os.path.basename(file))