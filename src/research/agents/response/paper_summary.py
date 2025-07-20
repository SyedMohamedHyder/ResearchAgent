from typing import List, Optional
from pydantic import BaseModel, Field

class PaperSummary(BaseModel):
    """
    A structured representation of a research paper's key information.

    This model captures important aspects of a paper such as its title, abstract,
    keywords, contributions, methodology, results, limitations, and notable references.
    It provides a concise summary useful for documentation, analysis, or review.
    """

    title: Optional[str] = Field(
        default=None,
        description="The full title of the paper."
    )

    abstract: Optional[str] = Field(
        default=None,
        description="The abstract or a generated summary of the paper."
    )

    keywords: List[str] = Field(
        default_factory=list,
        description="Key topics or terms (5–10) representing the paper's scope."
    )

    key_contributions: List[str] = Field(
        default_factory=list,
        description="The main contributions, findings, or novelties introduced by the paper."
    )

    methodology: Optional[str] = Field(
        default=None,
        description="Summary of the method, framework, algorithm, or experimental setup used."
    )

    results_summary: Optional[str] = Field(
        default=None,
        description="Concise summary of the paper's results or outcomes."
    )

    limitations: List[str] = Field(
        default_factory=list,
        description="Any stated or inferred limitations of the paper's approach or findings."
    )

    referenced_works: List[str] = Field(
        default_factory=list,
        description="Significant citations, tools, or datasets the paper builds upon."
    )

    domain_track: Optional[str] = Field(
        default=None,
        description="The inferred domain or track this paper belongs to (e.g., Cloud Computing, AI, IoT)."
    )
