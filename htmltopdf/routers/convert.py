import fileinput
from enum import Enum
from typing import Annotated
import json

from pydantic.v1.json import pydantic_encoder
from starlette.datastructures import FormData

from htmltopdf.controller import converter
from htmltopdf.models.convert import ConvertData
from fastapi import APIRouter, File, UploadFile, Depends, Request, HTTPException

import threading

router = APIRouter()


class BodyType(Enum):
    JSON = 1,
    FORM_DATA = 2


async def body_type(request: Request):
    content_type = request.headers.get('Content-Type')
    if content_type is None:
        raise HTTPException(status_code=400, detail='No Content-Type provided!')
    elif (content_type == 'application/x-www-form-urlencoded' or
          content_type.startswith('multipart/form-data')):
        try:
            return BodyType.FORM_DATA
        except Exception:
            raise HTTPException(status_code=400, detail='Invalid Form data')
    elif content_type == 'application/json':
        try:
            return BodyType.JSON
        except Exception:
            raise HTTPException(status_code=400, detail='Invalid body')


@router.post(
    "/",
    response_description="Returns status weather success convertion"
)
async def convert(request: Request):
    type = await body_type(request)
    match (type):
        case BodyType.FORM_DATA:
            body = await request.form()
            files = body.getlist('files')  # returns a list of UploadFile objects
            if files:
                for file in files:
                    print(f'Filename: {file.filename}')
                    await converter.convert_file(file)
        case BodyType.JSON:
            content = await request.json()
            print(content)
            data: ConvertData = ConvertData(**content)
            await converter.convert(data)
