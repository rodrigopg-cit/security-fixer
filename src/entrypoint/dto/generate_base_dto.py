from pydantic import BaseModel, Field


class GenerateBaseDto(BaseModel):
    entrypoint_folder: str = Field(examples=["Wings"], default=None)
    security_tool: str = Field(examples=["42crunch"], default=None)
