from typing import List, Tuple
import re
from pathlib import Path
import PyPDF2
from PyPDF2.utils import PdfReadError
from PIL import Image
import pytesseract


# todo Приведение структуры файлов к единообразию

# todo извлечение изображения из pdf
def pdf_image_extract(pdf_path: Path) -> List[Path]:
    file_decode = {
        '/DCTDecode': 'jpg',
        '/FlateDecode': 'png',
        '/JPXDecode': 'jp2'
    }
    result = []
    with open(pdf_path, 'rb') as file:
        try:
            pdf_file = PyPDF2.PdfFileReader(file)
        except PdfReadError:
            # сделать запись в лог ошибки
            pass
        for page_num, page in enumerate(pdf_file.pages, 1):
            file_name = f"{pdf_path.name}.{page_num}.{file_decode[page['/Resources']['/XObject']['/Im0']['/Filter']]}"
            image_data = page['/Resources']['/XObject']['/Im0']._data
            img_path = pdf_path.parent.joinpath(file_name)
            img_path.write_bytes(image_data)
            result.append(img_path)
    return result


# todo распознать текст на изображении
def get_serial_number(img_path: Path) -> Tuple[Path, List[str]]:
    numbers = []
    text_ru = pytesseract.image_to_string(Image.open(img_path), 'rus')
    for idx, line in enumerate(text_ru.split('\n')):
        pattern = re.compile(r'заводской.*номер')
        if re.match(pattern, line):
            text_en = pytesseract.image_to_string(Image.open(img_path), 'eng')
            numbers.append(text_en.split('\n')[idx].split()[-1])
    return img_path, numbers


if __name__ == '__main__':
    pdf_file_path = Path('/Users/gefest/projects/geekbrains/data_mining_23_11_2020/8416_4.pdf')
    
    images = pdf_image_extract(pdf_file_path)
    numbers = list(map(get_serial_number, images))
    print(1)