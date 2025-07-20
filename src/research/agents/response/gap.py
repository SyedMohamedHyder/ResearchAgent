from pydantic import BaseModel, Field

class GapIdentifierResult(BaseModel):
    """
    Represents the output of the gap identification process in research literature.
    It highlights the limitations, missing pieces, or open challenges found across the reviewed papers.
    """

    research_gaps: str = Field(
        ...,
        description="A cohesive paragraph describing the key gaps or limitations in the existing research literature."
    )
