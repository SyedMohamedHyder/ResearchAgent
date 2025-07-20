import asyncio
from dataclasses import dataclass
from typing import Callable,Any, Union


@dataclass
class AgentStep:
    """
    Represents a single agent execution step in the pipeline.
    
    Attributes:
        name: Descriptive name of the step.
        agent: The agent instance to be called.
        input_transform: A function that converts the context into input string for the agent.
        output_key: Key under which the result will be stored in the context.
    """
    name: str
    agent: Any
    input_transform: Callable[[dict], str]
    output_key: str


@dataclass
class ParallelAgentStep:
    """
    Represents a parallelized agent that processes a batch of inputs independently.
    
    Attributes:
        name: Descriptive name of the step.
        agent: The agent instance to be run on each input.
        batch_input_transform: Function that extracts a list of input strings from context.
        output_key: Key under which the list of parsed outputs is stored.
    """
    name: str
    agent: Any
    batch_input_transform: Callable[[dict], list[str]]
    output_key: str


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
    Each step updates the shared context dictionary.
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
        Run the pipeline steps in order, updating context at each step.

        Args:
            agent_runner: Async function to execute an agent with input and return output.

        Returns:
            dict: The updated context after all steps complete.
        """
        for step in self.steps:
            if isinstance(step, ParallelAgentStep):
                await self._run_parallel_agent_step(step, agent_runner)
            elif isinstance(step, ParallelGroup):
                await self._run_parallel_group(step, agent_runner)
            else:
                await self._run_single_agent_step(step, agent_runner)

        return self.context

    async def _run_single_agent_step(self, step: AgentStep, agent_runner: Callable):
        """
        Execute a single AgentStep in the pipeline.

        Args:
            step (AgentStep): The agent step to run.
            agent_runner (Callable): Async function that runs the agent and returns a result.

        Side Effects:
            Updates the pipeline context with the parsed result.
        """
        print(f"Running: {step.name}")
        self.context[step.output_key] = await agent_runner(step.agent, step.input_transform(self.context))

    async def _run_parallel_agent_step(self, step: ParallelAgentStep, agent_runner: Callable):
        """
        Execute a ParallelAgentStep by running the agent concurrently on a batch of inputs.

        Args:
            step (ParallelAgentStep): The step to execute in parallel.
            agent_runner (Callable): Async function that runs the agent and returns a result.

        Side Effects:
            Stores a list of parsed results in the pipeline context.
        """
        print(f"Running ParallelAgentStep: {step.name}")

        results = await asyncio.gather(*[
            agent_runner(step.agent, input_str) for input_str in step.batch_input_transform(self.context)
        ])
        self.context[step.output_key] = results

    async def _run_parallel_group(self, group: ParallelGroup, agent_runner: Callable):
        """
        Execute a group of AgentSteps or ParallelAgentSteps concurrently.

        Args:
            group (ParallelGroup): Group of independent steps to run in parallel.
            agent_runner (Callable): Async function to run each agent.

        Side Effects:
            Updates context with parsed results from each step.
        """
        print(f"Running ParallelGroup: {group.name}")

        async def run_step(s: Union[AgentStep, ParallelAgentStep]):
            if isinstance(s, ParallelAgentStep):
                await self._run_parallel_agent_step(s, agent_runner)
            else:
                await self._run_single_agent_step(s, agent_runner)

        await asyncio.gather(*[run_step(s) for s in group.steps])
