from pydantic import BaseModel


class ConvertData(BaseModel):
    htmlPath: str
    outPdf: str
    orientation: str | None = None
    cssPath: str | None = None
    pageTimeout: int | None = None
