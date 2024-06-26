from pydantic import BaseModel


class IncomeTranscribedText(BaseModel):
    tex_id: str | int
    user_id: str | int


class TranscribedTextId(BaseModel):
    id_text: str | int
