from pydantic import BaseModel


class Station(BaseModel):
    id: str
    name: str


class StationsResponse(BaseModel):
    stations: list[Station]


class LinesResponse(BaseModel):
    lines: list[str]
