# Dark Data Extraction and Analysis

This project is intended to convert images having text, non-searchable and scanned PDFs into searchable PDFs and arranged them according to the relevance to a given search query. And information contained in these documents can be further useful for textual analysis and visualization.

1. Scanned Images to editable text file using ***pytesseract*** - A wrapper for [Google’s Tesseract-OCR Engine](https://github.com/tesseract-ocr/tesseract).
2. Text Extraction from PDFs having scanned images and non-searchable text to list (collection in Python) of Keywords/text using Amazon’s ***textract***.
3. Ranking matching documents according to their relevance to a given *search query* using ***Okapi BM25.***
