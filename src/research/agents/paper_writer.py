from agents import Agent

PAPER_WRITER_PROMPT = """
You are an expert academic writing assistant.

Given all the components of a research paper (abstract, related work, gaps, research questions, hypotheses, methodology, experiments, results, and references), your task is to:

- Generate an appropriate and concise title
- Combine everything into a properly formatted, cohesive, and professional research paper

Return the complete research paper in a structured academic format.
"""

paper_writer_agent = Agent(
    name="Paper Writer Agent",
    instructions=PAPER_WRITER_PROMPT,
)
