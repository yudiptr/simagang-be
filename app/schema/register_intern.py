from pydantic import BaseModel, Field
from enum import Enum
from typing import List
from fastapi import File, UploadFile, Form

class FileTypes(Enum):
    PDF = "application/pdf"
    PNG = "image/png"

class InternFiles(BaseModel):
    cv: UploadFile = File(..., media_type=FileTypes.PDF.value)
    cover_letter: UploadFile = File(..., media_type=FileTypes.PDF.value)
    student_card: UploadFile = File(..., media_type=FileTypes.PDF.value)
    photo: UploadFile = File(..., media_type=FileTypes.PNG.value)
    proposal: UploadFile = File(..., media_type=FileTypes.PDF.value)