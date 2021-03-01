import os
import cv2
import PyPDF2 
import textract
import fpdf
import numpy as np
import pytesseract
from PIL import Image
#from nltk.tokenize import word_tokenize
#from nltk.corpus import stopwords
import pandas as pd
import re

#file Path
src_path = "D:\\Documents\\MiniProject\\New folder\\Final\\nonsearchable.pdf"

def get_string_from_image(img_path):
    # Read image with opencv
    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.medianBlur(img, 3)
    img = cv2.bilateralFilter(img,9,75,75)
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)    
    #  Apply threshold to get image with only black and white
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)   
    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(img_path))
    return result

def get_string_from_pdf(pdf_path):
    #open allows you to read the file
    pdfFileObj = open(pdf_path,'rb')
    #The pdfReader variable is a readable object that will be parsed
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #discerning the number of pages will allow us to parse through all #the pages
    num_pages = pdfReader.numPages
    count = 0
    pdftext = ""
    #The while loop will read each page
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        pdftext += pageObj.extractText()

    if pdftext != "":
        pdftext = pdftext
 
    else:#This if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.
        pdftext = textract.process(pdf_path, method='tesseract', language='eng').decode('utf-8')
    # Now we have a text variable which contains all the text derived #from our PDF file. Type print(text) to see what it contains. It #likely contains a lot of spaces, possibly junk such as '\n' etc.
    # Now, we will clean our text variable, and return it as a list of keywords.
    #The word_tokenize() function will break our text phrases into #individual words 
    #tokens = word_tokenize(pdftext)
    #we'll create a new list which contains punctuation we wish to clean
    #punctuations = ['(',')',';',':','[',']',',']
    #We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much value as keywords
    ##stop_words = stopwords.words('english')
    #We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
    #keywords = [word for word in tokens if not word in punctuations]
    #result= (" ".join(keywords))
    return pdftext

#Get extension of file & Call functions accordingly
filename_w_ext = os.path.basename(src_path)
filename, file_extension = os.path.splitext(filename_w_ext)
listofextensions = ['.jpeg', '.png', '.gif', '.bmp', '.tiff','.jpg']

if file_extension in listofextensions:
    print ('\n--- Started recognizing text from image ---\n')
    mst=get_string_from_image(src_path)
else:
    print ('\n--- Started recognizing text from pdf --\n')
    mst=get_string_from_pdf(src_path)

#-----------------------------------------------------------

text = mst.encode('ascii','ignore').lower()
keywords = re.findall(r'[a-zA-Z]\w+',text)
df = pd.DataFrame(list(set(keywords)),columns=['keywords'])



def weightage(word1,text,number_of_documents=1):
    word_list = re.findall(word1,text)
    number_of_times_word_appeared =len(word_list)
    tf = number_of_times_word_appeared/float(len(text))
    idf = np.log((number_of_documents)/float(number_of_times_word_appeared))
    tf_idf = tf*idf
    return number_of_times_word_appeared,tf,idf ,tf_idf 


    
df['number_of_times_word_appeared'] = df['keywords'].apply(lambda x: weightage(x,text)[0])
df['tf'] = df['keywords'].apply(lambda x: weightage(x,text)[1])
df['idf'] = df['keywords'].apply(lambda x: weightage(x,text)[2])
df['tf_idf'] = df['keywords'].apply(lambda x: weightage(x,text)[3])

df = df.sort_values('tf_idf',ascending=True)
df.to_csv('Keywords.csv')
df.head(25)     

#converting String to Searchable pdf
pdf = fpdf.FPDF(format='letter', unit='in')
pdf.alias_nb_pages()
pdf.add_page()
effective_page_width = pdf.w - 2*pdf.l_margin
pdf.set_font('Times','',13.5)
pdf.multi_cell(effective_page_width, 0.25, mst)
pdf.ln(2)
pdf.output("testings.pdf", 'F')
print("\n--- Succesfully Converted._.")

"""filename1 = "D:\\Documents\\MiniProject\\New folder\\Final\\UQP.pdf"

pdfFileObj1 = open(filename1, 'rb')

pdfReader1 = PyPDF2.PdfFileReader(pdfFileObj1)
search_word = input("Enter word: ") 
#search_word = "looks"
search_word_count = 0
pageno=[]
for pageNum in range(0, pdfReader1.numPages):
    pageObj = pdfReader1.getPage(pageNum)
    text = pageObj.extractText()
    search_text = text.lower().split()
    for word in search_text:
        if search_word in word:
            search_word_count += 1
            pageno.append(pageNum+1)
        
print("The word {} was found {} times \n".format(search_word, search_word_count,))
print("In Page Numbers:")
print(pageno)"""

