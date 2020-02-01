# Automate Shelf Life via Software Such as Abbyy via OCR and Indexing
## Project Description
I'm looking for some assistance identifying a software that will automate this process. Presently I've got a scanner that scans incoming vendor purchase orders into searchable pdf format. What I'm looking to do is based on the vendor index information via OCR for items such as shelf life and save it into the name of the file.
###Further explanation
If the word “JABAR” is found you want Capture Pro to look on page 4 for “shipping date” and “expiration date” and then place that information into an index field

Then if the word “BERGQUIS” is found look on page 2 for “Batches & Quantity” and place that info into index field

Then if “NIANTIC” is found look on page 5 for “cure information” and place that info into an index field

## Requirements
- argparse
- PyPDF2
- textract

## Installation
### Linux
Tesseract is available directly from many Linux distributions. The package is generally called 'tesseract' or 'tesseract-ocr' - search your distribution's repositories to find it. Thus you can install Tesseract 4.x and its developer tools on Ubuntu 18.x bionic by simply running:
```
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```
### Windows
Installer for Windows for Tesseract 3.05, Tesseract 4 and development version 5.00 Alpha are available from Tesseract at UB Mannheim (https://github.com/UB-Mannheim/tesseract/wiki). These include the training tools. Both 32-bit and 64-bit installers are available.
The path to installed binaries of Tesseract must be added to the PATH environment variable (typically `C:\Program Files\Tesseract-OCR`).

Poppler is also required for OCR. It could be downloaded here: http://blog.alivate.com.au/poppler-windows/. The archive with Poppler must be extracted. The path to `bin` directory of Poppler must be added to the `PATH` environment variable. 