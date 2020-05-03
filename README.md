# Dark Data Extraction and Analysis

Converted images having text, non-searchable and scanned PDFs into searchable PDFs and arranged them according to the relevance to a given search query.  can be further useful for textual analysis and visualization.

1. Scanned Images to editable text file using ***pytesseract*** wrapper for [Google’s Tesseract-OCR Engine](https://github.com/tesseract-ocr/tesseract).
2.  Text Extraction from PDFs having scanned images to list (collection in Python) of Keywords/text using Amazon’s ***textract***.
