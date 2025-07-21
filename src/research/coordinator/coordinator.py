import os
import asyncio
from agents import Runner, RunConfig, Agent
from foundation import pdf

from .pipeline import *
from research.agents.response import *
from research.agents import *
from .transformers import *


class ResearchCoordinator:
    """
    Coordinates the end-to-end research analysis process by:
    - Loading PDF files from a specified folder.
    - Extracting text from the PDFs.
    - Executing a multi-step AI pipeline that processes the papers to
      summarize them, identify related work and research gaps, and
      generate relevant research questions.
    """

    def __init__(self, papers_folder: str = "papers"):
        """
        Initializes the ResearchCoordinator.

        Args:
            papers_folder (str): Path to the folder containing research papers in PDF format.
        """
        self.papers_folder = papers_folder

    async def run_agent(self, agent, agent_input: str):
        """
        Runs a given agent asynchronously using a predefined model configuration.

        Args:
            agent (Agent): The agent instance to be executed.
            agent_input (str): Input data to feed into the agent.

        Returns:
            Any: The final output from the agent.
        """
        config = RunConfig(model="gpt-4o-mini")
        result = await Runner.run(agent, agent_input, run_config=config)
        return result.final_output

    async def load_paper_texts(self) -> list[str]:
        """
        Loads and reads all PDF files from the `papers_folder`, extracting text from each.

        Returns:
            list[str]: A list of paper texts extracted from the PDFs.
        """
        paths = [
            os.path.join(self.papers_folder, f)
            for f in os.listdir(self.papers_folder)
            if f.endswith(".pdf")
        ]
        return await asyncio.gather(
            *[asyncio.to_thread(pdf.read_pdf, path) for path in paths]
        )

    async def research(self) -> dict:
        """
        Executes the full research analysis pipeline:
        - Loads papers
        - Builds the processing pipeline
        - Runs the pipeline with agent execution

        Returns:
            dict: The final output from the pipeline containing results of all processing steps.
        """
        paper_texts = await self.load_paper_texts()
        pipeline = self._build_pipeline(paper_texts)
        return await pipeline.run(self.run_agent)

    def _build_pipeline(self, paper_texts: list[str]) -> Pipeline:
        """
        Constructs the processing pipeline for analyzing multiple research papers.
        Internally used by the coordinator.

        Args:
            paper_texts (list[str]): A list of raw paper texts.

        Returns:
            Pipeline: A configured Pipeline instance ready to run.
        """
        pipeline = Pipeline()

        pipeline.add_step(
            ParallelAgentStep(
                name="Paper Summary",
                agent=paper_summarizer_agent,
                input_transformer=lambda ctx: paper_texts,
                output_transformer=output_transformer(paper_summarizer_agent.name),
            )
        )

        pipeline.add_step(
            ParallelGroup(
                name="Parallel Analysis",
                steps=[
                    self._make_agent_step(
                        "Related Work",
                        related_work_agent,
                        summaries=paper_summarizer_agent.name,
                    ),
                    self._make_agent_step(
                        "Gap Identification",
                        gap_identifier_agent,
                        summaries=paper_summarizer_agent.name,
                    ),
                ],
            )
        )

        pipeline.add_step(
            self._make_agent_step(
                "Research Questions",
                research_question_agent,
                related_work=related_work_agent.name,
                gaps=gap_identifier_agent.name,
            )
        )

        pipeline.add_step(
            self._make_agent_step(
                "Hypotheses",
                hypothesis_generator_agent,
                questions=research_question_agent.name,
                related_work=related_work_agent.name,
                gaps=gap_identifier_agent.name
            )
        )

        pipeline.add_step(
            self._make_agent_step(
                "Methodology",
                methodology_planner_agent,
                hypotheses=hypothesis_generator_agent.name
            )
        )

        pipeline.add_step(
            self._make_agent_step(
                "SystemDesign",
                system_design_agent,
                methodology=methodology_planner_agent.name,
                hypotheses=hypothesis_generator_agent.name
            )
        )

        pipeline.add_step(
            self._make_agent_step(
                "Experiments",
                experiment_conductor_agent,
                system_design=system_design_agent.name,
                hypotheses=hypothesis_generator_agent.name,
                related_work=related_work_agent.name,
                gaps=gap_identifier_agent.name,
            )
        )

        pipeline.add_step(
            self._make_agent_step(
                "ResultsAnalysis",
                results_analyzer_agent,
                hypotheses=hypothesis_generator_agent.name,
                system_design=system_design_agent.name,
                experiment_results=experiment_conductor_agent.name
            )
        )

        pipeline.add_step(
            self._make_agent_step(
                "Abstract",
                abstract_generator_agent,
                questions=research_question_agent.name,
                system_design=system_design_agent.name,
                results=experiment_conductor_agent.name
            )
        )

        pipeline.add_step(
        self._make_agent_step(
                "References",
                reference_generator_agent,
                summary=paper_summarizer_agent.name,
                related_work=related_work_agent.name,
                gaps=gap_identifier_agent.name,
                questions=research_question_agent.name
            )
        )

        pipeline.add_step(
            self._make_agent_step(
                "Write Paper",
                paper_writer_agent,
                output_format="md",
                abstract=abstract_generator_agent.name,
                related_work=related_work_agent.name,
                research_gaps=gap_identifier_agent.name,
                research_questions=research_question_agent.name,
                hypotheses=hypothesis_generator_agent.name,
                methodology=methodology_planner_agent.name,
                experiments=experiment_conductor_agent.name,
                results_analysis=results_analyzer_agent.name,
                references=reference_generator_agent.name,
            )
        )

        return pipeline

    def _make_agent_step(self, name: str, agent: Agent, output_format="json", **input_sources) -> AgentStep:
        """
        Creates a configured AgentStep for a given agent with transformed input and output.

        Args:
            name (str): The name of the step in the pipeline.
            agent (Agent): The agent instance to execute for this step.
            output_format (str, optional): Format to parse the agent's output (e.g., "json", "text"). Defaults to "json".
            **input_sources: Keyword arguments mapping input field names to the names of previous steps
                            whose outputs will be passed as inputs to this agent.

        Returns:
            AgentStep: A fully initialized step with input and output transformers ready for pipeline execution.
        """
        return AgentStep(
            name=name,
            agent=agent,
            input_transformer=input_transformer(**input_sources),
            output_transformer=output_transformer(agent.name, output_format=output_format),
        )
