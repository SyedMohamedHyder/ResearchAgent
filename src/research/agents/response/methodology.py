from pydantic import BaseModel, Field
from typing import List, Optional

class Methodology(BaseModel):
    hypothesis: str = Field(..., description="The hypothesis this methodology is designed to test.")
    approach: str = Field(..., description="The overall research approach or strategy (e.g., experiment, survey, simulation).")
    tools: Optional[str] = Field(None, description="Tools, software, or frameworks proposed for the methodology.")
    data: Optional[str] = Field(None, description="The type of data required or to be collected.")
    procedure: Optional[str] = Field(None, description="Step-by-step plan or procedure to carry out the methodology.")

class MethodologyPlan(BaseModel):
    """
    A structured plan detailing how to test each hypothesis using appropriate methodology, tools, and data.
    """
    methodologies: List[Methodology] = Field(
        ...,
        description="A list of methodological plans corresponding to each hypothesis."
    )
