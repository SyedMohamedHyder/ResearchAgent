from pydantic import BaseModel, Field

class Abstract(BaseModel):
    """
    A concise and informative abstract summarizing the key aspects of the research.
    """

    abstract: str = Field(
        ...,
        description="A clear, self-contained summary of the research motivation, methods, and conclusions."
    )
