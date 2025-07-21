from .hypothesis_generator import hypothesis_generator_agent
from .related_work import related_work_agent
from .gap_identifier import gap_identifier_agent
from .questionnaire import research_question_agent
from .paper_summarizer import paper_summarizer_agent
from .methodology_planner import methodology_planner_agent
from .system_designer import system_design_agent
from .expermient_conductor import experiment_conductor_agent
from .results_analyzer import results_analyzer_agent
from .abstract_generator import abstract_generator_agent
from .reference_geneartor import reference_generator_agent
from .paper_writer import paper_writer_agent


__all__ = [
    "paper_summarizer_agent",
    "gap_identifier_agent",
    "related_work_agent",
    "research_question_agent",
    "hypothesis_generator_agent",
    "methodology_planner_agent",
    "system_design_agent",
    "experiment_conductor_agent",
    "results_analyzer_agent",
    "abstract_generator_agent",
    "reference_generator_agent",
    "paper_writer_agent",
]
