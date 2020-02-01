import argparse
import glob
import os
import PyPDF2
import re
from shutil import copyfile
import textract
from typing import Dict, List


def extract_text(file_name) -> str:
    """
    The function extracts text from the searchable pdf file
    :param file_name: Path to the pdf file
    :return: String with text extracted from the pdf file using PyPDF2
    """
    # get the number of pages of the pdf file
    reader = PyPDF2.PdfFileReader(file_name)
    pages_number = reader.getNumPages()
    doc = ''
    for i in range(pages_number):
        page = reader.getPage(i)
        text = page.extractText()
        doc = doc + text
    return doc


def scan(input_path: str, extension_mask='*.pdf', is_searchable=True, method='tesseract') -> List[Dict[str, str]]:
    """
    The function returns the list of dictionaries. The initial filenames are saved with the 'src' key in the dictionary.
    The new filenames are saved with  the 'dst' key in the dictionary.
    :param input_path: Path to the directory with pdf files
    :param extension_mask: Mask of pdf files in the directory
    :param is_searchable: If true then the text is extracted from the file via PyPDF2 else textract is employed
    :param method: One of {'tesseract', 'pdftotext'}. If method is tesseract then text is recognised by tesseract-ocr else text is extracted by pdftotext
    :return: Lis of dictionaries
    """
    pdfs = []
    for file_name in glob.glob(os.path.join(input_path, extension_mask)):
        if is_searchable:
            text = extract_text(file_name)

        else:
            text = str(textract.process(file_name, method=method, language='eng'), encoding='UTF-8')
            # print(text)

        new_file_name = ''

        if re.search('JABAR', text, re.IGNORECASE):
            print('JABAR is found in {}'.format(file_name))
            shipping_date = re.search('shipping\s*date\s*[:;,|.!]\s*\d+/\d+/\d+', text, re.IGNORECASE)
            if shipping_date:
                split = shipping_date.group(0).split()
                print('Expiration Date: {}'.format(split[-1]))
                new_file_name += ' - {}'.format(split[-1])
            else:
                print('Shipping Date is not found in {}'.format(file_name))

            expiration_date = re.search('expiration\s*date\s*[:;,|.!]\s*\d+\s*years', text, re.IGNORECASE)
            if expiration_date:
                split = expiration_date.group(0).split()
                print('Expiration Date: {}'.format(split[-2]))
                new_file_name += ' - {} YEARS'.format(split[-2])
            else:
                print('Expiration Date is not found in {}'.format(file_name))

        elif re.search('BERGQUIS', text, re.IGNORECASE):
            id_re = re.search('\w+\s*\(\s*\w+[.,]\w+\s*\w+\)', text, re.IGNORECASE)
            if id_re:
                split = id_re.group(0).split()
                print('ID: {}'.format(split[0]))
                new_file_name += ' - {}'.format(split[0])
            else:
                print('ID is not found in {}'.format(file_name))

            shelf_date = re.search('\s*she[lfti][lfti]\s*Life\s*[:;,.]\s*\d*/\d*/\d*', text, re.IGNORECASE)
            if shelf_date:
                split = shelf_date.group(0).split()
                print('Shelf Date: {}'.format(split[-1]))
                new_file_name += ' - {}'.format(split[-1])
            else:
                print('Shelf Date is not found in {}'.format(file_name))

        elif re.search('NIANTIC', text, re.IGNORECASE):
            cure = re.search('\d(qo0)\d\d?', text, re.IGNORECASE)
            if cure:
                print('Cure: {}'.format(cure.group(0)))
                new_file_name += ' - {}'.format(cure.group(0))
            else:
                print('Cure is not found in {}'.format(file_name))

        else:
            print('Keywords are not found in {}'.format(file_name))

        base = os.path.basename(file_name)
        split_base = os.path.splitext(base)
        new_file_name = split_base[0] + new_file_name + split_base[1]

        pdfs.append({'src': file_name, 'dst': new_file_name})

    return pdfs


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Automate Shelf Life via Software Such as Abbyy via OCR and Indexing')
    parser.add_argument(
        '--input_path',
        type=str,
        default='scans',
        help='Path to the directory with searchable scans of incoming vendor purchases.'
    )
    parser.add_argument(
        '--output_path',
        type=str,
        default='output',
        help='Path to the directory. Processed files will be copied in this directory.'
    )
    parser.add_argument(
        '--searchable',
        action="store_true",
        help='Documents are well scanned and recognized using the OCR software. '
             'If this argument is not set then tesseract is employed for OCR.'
    )
    args = parser.parse_args()
    pdfs = scan(args.input_path, is_searchable=args.searchable)
    for d in pdfs:
        copyfile(d['src'], os.path.join(args.output_path, d['dst'].replace('/', '.')))
