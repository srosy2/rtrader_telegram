import PyPDF2
import cv2
import pytesseract
from pdf2image import convert_from_path


# file_name = 'trader.jpg'

class PrepareMessage:
    type_file = 'JPEG'
    custom_config = r'-l eng --oem 1 --psm 6'

    def __init__(self, file: str, img: str):
        self.pdf_file = file
        self.image_file = img
        self._prepare_answer()

    @staticmethod
    def _prepare_text(text):
        return text.split('\n')[-2]

    @staticmethod
    def _read_image(file):
        img = cv2.imread(file)
        return img

    def _prepare_answer(self):
        self._convert_pdf_to_image(self.pdf_file, self.image_file)

    def _get_image_text(self, image_file):
        img = self._read_image(image_file)
        text = pytesseract.image_to_string(
            img, config=self.custom_config
        )
        return self._prepare_text(text)

    def _convert_pdf_to_image(self, file, file_name):
        images = convert_from_path(file)
        images[0].save(file_name, self.type_file)

    def return_image(self):
        with open(self.image_file, 'rb') as file:
            img = file.read()
        return img

    def return_text(self):
        return self._get_image_text(self.image_file)


if __name__ == '__main__':
    message = PrepareMessage('download_2_file', 'trader.jpg')
