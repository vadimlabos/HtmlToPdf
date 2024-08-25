import argparse
from pathlib import Path
import os

from htmltopdf.config.settings import GeneralSettings, get_general_settings

counter: int = 0


class Utils:

    @staticmethod
    def get_settings() -> GeneralSettings:
        return get_general_settings()

    @staticmethod
    def get_footer_template_path() -> str:
        base: str = Path(__file__).parent.parent.as_posix()
        footer_file_path: str = get_general_settings().footer_path
        return base + footer_file_path

    @staticmethod
    def get_css_path() -> str:
        base: str = Path(__file__).parent.parent.as_posix()
        footer_file_path: str = get_general_settings().css_path
        return base + footer_file_path

    @staticmethod
    def get_temp_dir() -> str:
        base: str = Path(__file__).parent.parent.parent.as_posix()
        temp_dir: str = get_general_settings().temp_dir

        os.makedirs(base + temp_dir, exist_ok=True)

        return base + temp_dir

    @staticmethod
    def get_pdf_options() -> dict:
        options = {
            'page-size': 'A4',
            'margin-top': '10',
            'margin-right': '15',
            'margin-bottom': '40',
            'margin-left': '15',
            'encoding': "UTF-8",
            'orientation': 'Portrait',
            'no-outline': None,
            'footer-right': 'Page: [page]/[topage]',
            'footer-left': 'LabOS',
            'footer-line': True,
            'footer-spacing': '5',
            'header-line': True,
            'header-center': 'Test',
            'header-spacing': '5',
            'enable-local-file-access': True
        }

        return options

    @staticmethod
    def generate_temp_file_name(file_name: str) -> str:
        global counter
        pre, ext = os.path.splitext(file_name)
        counter = counter + 1
        return pre + "_(" + str(counter) + ")_" + ".pdf"

    @staticmethod
    def parse_arguments() -> any:
        parser = argparse.ArgumentParser()
        parser.add_argument('--debug', action='store_true', help="Enable debug mode")
        return parser.parse_args()
