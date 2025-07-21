import asyncio
from dataclasses import dataclass
from typing import Callable, Any, Union

import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentStep:
    """
    Represents a single agent execution step in the pipeline.

    Attributes:
        name: Descriptive name of the step.
        agent: The agent instance to be called.
        input_transformer: A function that extracts input string(s) from the shared context.
        output_transformer: A function that takes (context, output) and modifies the context.
    """
    name: str
    agent: Any
    input_transformer: Callable[[dict], str]
    output_transformer: Callable[[dict, Any], None]


@dataclass
class ParallelAgentStep:
    """
    Represents a parallelized agent that processes a batch of inputs independently.

    Attributes:
        name: Descriptive name of the step.
        agent: The agent instance to be run on each input.
        input_transformer: A function that extracts a list of input strings from context.
        output_transformer: A function that takes (context, list of outputs) and modifies the context.
    """
    name: str
    agent: Any
    input_transformer: Callable[[dict], list[str]]
    output_transformer: Callable[[dict, list[Any]], None]


@dataclass
class ParallelGroup:
    """
    Represents a group of agent steps (AgentStep or ParallelAgentStep) that should be executed in parallel.

    Attributes:
        name: Group name for logging/debugging.
        steps: A list of steps to run concurrently, can be AgentStep or ParallelAgentStep.
    """
    name: str
    steps: list[Union[AgentStep, ParallelAgentStep]]


# A step can be a single agent, a batch-parallel agent, or a group of concurrent agents
PipelineStep = Union[AgentStep, ParallelAgentStep, ParallelGroup]


class Pipeline:
    """
    Manages and executes a sequence of agent-based steps.

    Supports sequential, parallel, and batch-parallel execution.
    Each step updates the shared context dictionary through input and output transformers.
    """

    def __init__(self, context: dict = None):
        """
        Initialize the pipeline with an optional context.

        Args:
            context: Dictionary storing shared state between steps.
        """
        self.context = context or {}
        self.steps: list[PipelineStep] = []

    def add_step(self, step: PipelineStep):
        """
        Add a processing step to the pipeline.

        Args:
            step: One of AgentStep, ParallelAgentStep, or ParallelGroup.
        """
        self.steps.append(step)

    async def run(self, agent_runner: Callable) -> dict:
        """
        Runs the pipeline steps in order.

        Args:
            agent_runner: Async function to execute an agent with input and return output.
        """
        logger.info("Pipeline execution started.")
        
        for step in self.steps:
            logger.info(f"Starting step: {step.name} ({type(step).__name__})")

            try:
                if isinstance(step, ParallelAgentStep):
                    await self._run_parallel_agent_step(step, agent_runner)
                elif isinstance(step, ParallelGroup):
                    await self._run_parallel_group(step, agent_runner)
                else:
                    await self._run_single_agent_step(step, agent_runner)
                
                logger.info(f"Completed step: {step.name}")
            
            except Exception as e:
                logger.error(f"Step failed: {step.name} — {e}", exc_info=True)
                raise

        logger.info("Pipeline execution completed successfully.")

    async def _run_single_agent_step(self, step: AgentStep, agent_runner: Callable):
        """
        Execute a single AgentStep in the pipeline.

        Args:
            step: The agent step to run.
            agent_runner: Async function that runs the agent and returns a result.
        """
        agent_input = step.input_transformer(self.context)
        output = await agent_runner(step.agent, agent_input)
        step.output_transformer(self.context, output)

    async def _run_parallel_agent_step(self, step: ParallelAgentStep, agent_runner: Callable):
        """
        Execute a ParallelAgentStep by running the agent concurrently on a batch of inputs.

        Args:
            step: The step to execute in parallel.
            agent_runner: Async function that runs the agent and returns a result.
        """
        input_list = step.input_transformer(self.context)
        results = await asyncio.gather(*[
            agent_runner(step.agent, agent_input) for agent_input in input_list
        ])
        step.output_transformer(self.context, results)

    async def _run_parallel_group(self, group: ParallelGroup, agent_runner: Callable):
        """
        Execute a group of AgentSteps or ParallelAgentSteps concurrently.

        Args:
            group: Group of independent steps to run in parallel.
            agent_runner: Async function to run each agent.

        Side Effects:
            Updates context with parsed results from each step.
        """
        async def run_step(s: Union[AgentStep, ParallelAgentStep]):
            if isinstance(s, ParallelAgentStep):
                await self._run_parallel_agent_step(s, agent_runner)
            else:
                await self._run_single_agent_step(s, agent_runner)

        await asyncio.gather(*[run_step(s) for s in group.steps])
