from pydantic import BaseModel
from enum import Enum
from typing import Optional

class InputType(str, Enum):
    LOCAL_FOLDER = "local_folder"
    GOOGLE_DRIVE = "google_drive"

class ProcessRequest(BaseModel):
    input_type: InputType
    path: str
    api_key: str

class ProcessResponse(BaseModel):
    excel_path: str
    pdf_path: str
    message: str