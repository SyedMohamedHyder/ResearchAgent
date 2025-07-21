from pydantic import BaseModel, Field
from typing import List, Optional


class Hypothesis(BaseModel):
    """
    Represents a single hypothesis derived from a research question.

    Attributes:
        question (str): The research question that led to the hypothesis.
        hypothesis (str): A testable statement that can be investigated or validated.
        rationale (Optional[str]): Optional explanation supporting why the hypothesis makes sense,
                potentially citing gaps or trends observed in prior work.
    """
    question: str = Field(..., description="The research question that inspired this hypothesis.")
    hypothesis: str = Field(..., description="A testable hypothesis derived from the question.")
    rationale: Optional[str] = Field(None, description="Optional explanation or justification for the hypothesis.")


class Hypotheses(BaseModel):
    """
    A list of structured hypotheses derived from prior research questions,
    each including optional rationale to support their formulation.

    Attributes:
        hypotheses (List[Hypothesis]): A collection of hypotheses paired with their respective
                                       research questions and rationales.
    """
    hypotheses: List[Hypothesis] = Field(
        ...,
        description="A structured list of hypotheses derived from research questions, with optional rationale."
    )
