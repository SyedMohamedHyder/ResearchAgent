from pydantic import BaseModel, Field


class RelatedWorkSummary(BaseModel):
    """
    Represents the synthesized 'Related Work' section of a research paper.
    This section provides a cohesive narrative comparing and contrasting 
    multiple existing research works, grouped by similarity in topics, 
    methods, or goals, and highlights the gaps they leave unaddressed.
    """

    related_work_section: str = Field(
        ...,
        description="A well-structured paragraph summarizing and analyzing existing research works relevant to the new study."
    )
