from datetime import datetime, timedelta
from typing import Any

import pdfkit
from fastapi import UploadFile

from htmltopdf.models.convert import ConvertData
from htmltopdf.utils.utils import Utils


async def convert(data: ConvertData) -> Any:
    status: bool = False
    error: str = None
    delta: timedelta = timedelta(0, 0, 0, 0)
    try:
        print("Converting: " + data.htmlPath)
        start: any = datetime.now()
        pdfkit.from_file(data.htmlPath, Utils.generate_temp_file_name(data.outPdf), options=Utils.get_pdf_options())
        end: any = datetime.now()
        delta = end - start

    except Exception as e:
        error = f'Failed to convert file, file name: {data.htmlPath}. \n Exception: {e}'
        status = False
        print(error)
    finally:
        if status:
            print(f'Converted, file name: {data.htmlPath}. Duration {delta.total_seconds() * 1000} ms.')

        return status, error


async def convert_file(file: UploadFile) -> Any:
    status: bool = False
    error: str = None
    delta: timedelta = timedelta(0, 0, 0, 0)
    try:
        print("Converting: " + file.filename)
        start: datetime = datetime.now()
        content: bytes = await file.read()
        pdf: str = Utils.get_temp_dir() + Utils.generate_temp_file_name(file.filename)
        status = pdfkit.from_string(content.decode('utf-8'),
                                    pdf,
                                    options=Utils.get_pdf_options())
        end: datetime = datetime.now()
        delta = end - start

    except Exception as e:
        error = f'Failed to convert file, file name: {file.filename}. \n Exception: {e}'
        status = False
        print(error)
    finally:
        if status:
            print(f'Converted, file name: {file.filename}. Duration {delta.total_seconds() * 1000} ms.')

        return status, error
