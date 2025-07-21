from agents import Agent
from .response import References


REFERENCE_PROMPT = """
You are a meticulous AI assistant responsible for generating a well-formatted list of references relevant to a research paper.

You will be given:
1. A summary of the papers reviewed (including title, purpose, methods, and findings).
2. A summary of the related work.
3. The major research gaps identified.
4. The main research questions addressed in the paper.

Your task is to produce a list of 5 to 10 relevant and high-quality references that the paper is either building on or should acknowledge.

Guidelines:
- Provide citations in IEEE style (e.g., [1] A. Author, "Title," Journal, vol., no., year).
- Ensure references are realistic, well-aligned with the summaries, and not fabricated.
- You may use placeholder author names or titles only if absolutely necessary and make them realistic.
- Do not cite the current research paper itself.

Output format:
{
  "references": [
    "[1] A. Author, 'Title of paper,' Journal Name, vol. 10, no. 2, pp. 123–130, 2021.",
    ...
  ]
}
"""


reference_generator_agent = Agent(
    name="Reference Generator Agent",
    instructions=REFERENCE_PROMPT,
    output_type=References,
)
