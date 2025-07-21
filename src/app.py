import asyncio
from dotenv import load_dotenv

from agents import trace, gen_trace_id
from research.coordinator import ResearchCoordinator

load_dotenv()


async def main():
    researcher = ResearchCoordinator(papers_folder="papers")

    trace_id = gen_trace_id()
    print(f"Trace URL: https://platform.openai.com/traces/trace?trace_id={trace_id}")

    with trace("Deep Research", trace_id=trace_id):
        await researcher.research()


if __name__ == "__main__":
    asyncio.run(main())
