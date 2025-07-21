from pydantic import BaseModel, Field
from typing import List

class References(BaseModel):
    """
    A structured list of references used or relevant to the research, in a standard citation format.
    """

    references: List[str] = Field(
        ...,
        description="A list of references cited or relevant to the research, formatted in IEEE/APA style."
    )
