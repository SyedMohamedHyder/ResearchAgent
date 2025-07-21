from pydantic import BaseModel, Field
from typing import List, Optional

class AnalyzedResult(BaseModel):
    hypothesis: str = Field(..., description="The hypothesis being evaluated.")
    outcome: str = Field(..., description="The observed or simulated outcome of the experiment.")
    analysis: str = Field(..., description="Interpretation of the outcome and whether it supports or refutes the hypothesis.")
    confidence: Optional[str] = Field(None, description="Optional estimate of confidence or reliability in the result.")

class ResultsAnalysis(BaseModel):
    """
    Structured analysis of experiment outcomes aligned with the hypotheses.
    """

    results: List[AnalyzedResult] = Field(
        ...,
        description="List of analyzed outcomes mapped to each hypothesis, including interpretation and optional confidence."
    )
