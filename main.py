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

def crop_image(image, margin_width, margin_height, page_num):
    width, height = image.size
    cropped_image = image.crop((margin_width, margin_height, width - margin_width, height - margin_height))

    # Save the cropped image
    if not os.path.exists('cropped'):
        os.makedirs('cropped')
    cropped_image.save(os.path.join('cropped', f'page_{page_num}.png'))

    return cropped_image

def ocr_pdf(pdf_path, margin_width=100, margin_height=100):
    images = convert_from_path(pdf_path)
    text = ""
    for i, img in enumerate(images):
        img = crop_image(img, margin_width, margin_height, i)
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
