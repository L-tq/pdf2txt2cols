import io
import os
import re
from pdf2image import convert_from_path
import pytesseract
import fitz

# sudo apt-get install tesseract-ocr


def flatten_pdf(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    for page in doc:
        page.clean_contents()
        for annot in page.annots():
            annot.update()
    doc.save(output_path)
    doc.close()


def ocr_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang="eng")
    return text

def process_text(text):
    lines = text.split('\n')
    processed_lines = []

    for i, line in enumerate(lines):
        if i > 0 and line and not lines[i-1]:
            processed_lines.append("\n")

        if line.endswith("-"):
            line = line.rstrip("-")
        else:
            line += " "

        processed_lines.append(line)

    return ''.join(processed_lines)

def save_to_txt(text, output_path):
    with io.open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def main(input_pdf, output_txt):
    flattened_pdf = 'flattened.pdf'
    flatten_pdf(input_pdf, flattened_pdf)
    raw_text = ocr_pdf(flattened_pdf)
    processed_text = process_text(raw_text)
    save_to_txt(processed_text, output_txt)
    os.remove(flattened_pdf)



if __name__ == "__main__":
    input_pdf = 'input.pdf'
    output_txt = 'output.txt'
    main(input_pdf, output_txt)
