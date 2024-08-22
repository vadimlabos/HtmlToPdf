from datetime import datetime, timedelta

import pdfkit
from fastapi import UploadFile

from htmltopdf.models.convert import ConvertData
from htmltopdf.utils.utils import Utils


async def convert(data: ConvertData) -> bool:
    status: bool = False
    delta: timedelta = timedelta(0, 0, 0, 0)
    try:
        print("Converting: " + data.htmlPath)
        start: any = datetime.now()
        pdfkit.from_file(data.htmlPath, Utils.generate_temp_file_name(data.outPdf), options=Utils.get_pdf_options())
        end: any = datetime.now()
        delta = end - start

    except Exception as e:
        print(f'Failed to convert file, file name: {0}. \n Exception: {1}', data.htmlPath, e)
        status = False
    finally:
        print(f'Converted, file name: {0}. Duration {1} ms.', data.htmlPath, delta.total_seconds() * 1000)
        return status


async def convert_file(file: UploadFile) -> bool:
    status: bool = False
    delta: timedelta = timedelta(0, 0, 0, 0)
    try:
        print("Converting: " + file.filename)
        start: datetime = datetime.now()
        content: bytes = await file.read()
        status = pdfkit.from_string(content.decode('utf-8'), Utils.generate_temp_file_name(file.filename),
                                    options=Utils.get_pdf_options())
        end: datetime = datetime.now()
        delta = end - start

    except Exception as e:
        print(f'Failed to convert file, file name: {0}. \n Exception: {1}', file.filename, e)
        status = False
    finally:
        print(f'Converted, file name: {0}. Duration {1} ms.', file.filename, delta.total_seconds() * 1000)
        return status
