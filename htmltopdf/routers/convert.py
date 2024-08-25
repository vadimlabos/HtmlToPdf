from enum import Enum

from fastapi import APIRouter, Request, HTTPException

from htmltopdf.controller import converter
from htmltopdf.models.convert import ConvertData

router = APIRouter()


class BodyType(Enum):
    JSON = 1,
    FORM_DATA = 2


async def body_type(request: Request) -> BodyType:
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
            raise HTTPException(status_code=422, detail='Invalid body')


@router.post(
    "/",
    response_description="Returns status weather success convertion"
)
async def convert(request: Request):
    type: BodyType = await body_type(request)
    status: bool = False
    error: str = None

    match (type):
        case BodyType.FORM_DATA:
            body = await request.form()
            files = body.getlist('files')  # returns a list of UploadFile objects
            if files:
                for file in files:
                    status, error = await converter.convert_file(file)
        case BodyType.JSON:
            content = await request.json()
            data: ConvertData = ConvertData(**content)
            status, error = await converter.convert(data)

    if status:
        return {"Message": "Converted"}
    else:
        raise HTTPException(status_code=422, detail=error)
