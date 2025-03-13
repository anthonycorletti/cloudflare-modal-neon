from datetime import datetime

from pydantic import BaseModel


class ReadinessCheck(BaseModel):
    message: str
    version: str
    t: datetime
