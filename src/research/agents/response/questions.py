from pydantic import BaseModel, Field
from typing import List

class ResearchQuestions(BaseModel):
    """
    A list of research questions generated based on the identified gaps 
    and related works in the field of study. These questions aim to guide 
    and define the objectives of a potential new research paper.
    """

    questions: List[str] = Field(
        ...,
        description="A list of well-formed, focused research questions derived from prior work and identified gaps."
    )
