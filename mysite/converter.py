
import subprocess
from typing import Tuple

from PIL import Image


class BadPdf(Exception):
    pass


class Ghostscript():
    def __init__(self, DLL, args):
        cmd = DLL
        for arg in args:
            cmd += ' '+arg
        self.cmd = cmd

    def run(self):
        code = subprocess.call(self.cmd)
        if code != 0:
            raise BadPdf('pdf file is not valid')


def convert_pdf2tiff(input_file, output_file_name):
    driver = 'tiffg4'
    args = ['-dNOPAUSE',
            '-q',
            f'-sDEVICE={driver}',
            '-dBATCH',
            '-sPAPERSIZE=a4',
            f'-sOutputFile={output_file_name}',
            input_file]
    Ghostscript('gswin64c.exe', args).run()
    return output_file_name


def size_for_fit(size: Tuple[int, 'int']) -> Tuple[int, int]:
    width, height = size
    k = 1
    if width > height and width > 2550:
        k = width/2550
    if height > width and height > 2550:
        k = height/2550
    return int(width/k), int(height/k)


def pdf2tiff(file_name):
    input_file = file_name
    output_file_name = file_name[0:-4] + '.tiff'
    tiff = convert_pdf2tiff(input_file, output_file_name)
    tiff_img = Image.open(tiff)
    new_size: Tuple[int, int] = size_for_fit(tiff_img.size)
    output_img = tiff_img.resize(new_size)
    output_img.save(output_file_name, dpi=(300, 300))
    return output_file_name

if __name__ == "__main__":
    pdf2tiff("C:/Task2.pdf")
    #'gswin64c.exe -dNOPAUSE -q -sDEVICE=tiffg4 -dBATCH -sPAPERSIZE=a4 -sOutputFile=C:/Task2.tiff C:/Task2.pdf'