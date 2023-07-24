from pydantic import BaseModel


class Image(BaseModel):
    def __init__(self, data: str):
        self.data = data
