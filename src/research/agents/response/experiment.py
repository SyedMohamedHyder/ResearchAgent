from pydantic import BaseModel, Field
from typing import List, Optional


class Experiment(BaseModel):
    """
    A detailed description of an experiment designed to test a specific hypothesis.
    """
    hypothesis: str = Field(..., description="The hypothesis that this experiment is designed to test.")
    objective: str = Field(..., description="The main goal or question the experiment seeks to answer.")
    variables: List[str] = Field(..., description="Key variables involved in the experiment.")
    method: str = Field(..., description="The method or procedure used to carry out the experiment.")
    expected_outcome: Optional[str] = Field(None, description="The anticipated results or implications if the hypothesis holds.")

class Experiments(BaseModel):
    """
    A list of experiments, each targeting a hypothesis with a defined method, variables, and expected outcome.
    """
    experiments: List[Experiment] = Field(
        ..., 
        description="List of structured experiments to test corresponding hypotheses."
    )
