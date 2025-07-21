from pydantic import BaseModel, Field
from typing import List, Optional

class Component(BaseModel):
    name: str = Field(..., description="Name of the system component.")
    description: str = Field(..., description="Purpose and functionality of the component.")
    technologies: Optional[List[str]] = Field(None, description="Technologies or tools used in this component.")

class SystemDesign(BaseModel):
    """
    A high-level system design representing the architecture that implements the proposed methodology.
    It includes major components, their responsibilities, and potential technologies.
    """
    overview: str = Field(..., description="A high-level description of the overall system design and its purpose.")
    components: List[Component] = Field(..., description="Key components of the system and their roles.")
    rationale: Optional[str] = Field(None, description="Optional justification for the chosen architecture or design decisions.")
