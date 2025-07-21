import json
from pathlib import Path
from pydantic import BaseModel
from typing import Union, Any, Callable


def serialize_model(model: Union[BaseModel, list, dict]):
    """
    Recursively serializes a Pydantic BaseModel or list/dict of models into serializable dicts.
    """
    if isinstance(model, list):
        return [serialize_model(item) for item in model]
    elif isinstance(model, dict):
        return {k: serialize_model(v) for k, v in model.items()}
    elif isinstance(model, BaseModel):
        return model.model_dump()
    else:
        return model  # Primitive types, strings, etc.


def input_transformer(**input_sources: str) -> Callable[[dict], str]:
    """
    Returns a transformer function that loads multiple JSON files from the `outputs/` directory
    and returns a single merged dictionary as a JSON string.

    Args:
        **input_sources: Keyword arguments where each key is the desired key in the final dictionary
            and each value is the agent name whose output file will be read (`outputs/{agent_name}.json`).

    Returns:
        A function that takes a context dictionary (ctx) and returns a JSON string containing the combined inputs.

    Example:
        transformer = input_transformer(summaries="summarizer_agent", citations="citation_agent")
        result = transformer(ctx)
        # result => '{"summaries": {...}, "citations": {...}}'
    """
    def transformer(ctx: dict) -> str:
        try:
            combined_inputs = {}

            for input_key, agent_name in input_sources.items():
                file_path = Path("outputs", f"{agent_name}.json")
                if not file_path.exists():
                    raise FileNotFoundError(
                        f"[input_transformer] File not found: {file_path}"
                    )

                with file_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)

                combined_inputs[input_key] = data

            return json.dumps(combined_inputs, ensure_ascii=False)

        except Exception as e:
            print(f"[input_transformer] Failed to load input files: {e}")
            raise

    return transformer


def output_transformer(agent_name: str, output_format="json") -> Callable[[dict, Any], None]:
    """
    Creates a transformer function that writes the output of an agent to a file in the `outputs/` directory.

    Args:
        agent_name (str): The name of the agent. Used to name the output file.
        output_format (str, optional): Format of the output file. Either "json" or plain text. Defaults to "json".

    Returns:
        Callable[[dict, Any], None]: A transformer function that takes the execution context and the agent output,
        and writes the output to `outputs/{agent_name}.{output_format}`.

    Raises:
        Exception: If writing to the file fails, the exception is logged and re-raised.
    """
    def transformer(_: dict, output: Any) -> None:
        try:
            path = Path("outputs", f"{agent_name}.{output_format}")
            path.parent.mkdir(parents=True, exist_ok=True)

            with path.open("w", encoding="utf-8") as f:
                if output_format == "json":
                    json.dump(serialize_model(output), f, indent=2, ensure_ascii=False)
                else:
                    f.write(output)

        except Exception as e:
            print(f"[output_transformer] Failed to write to {agent_name}.{output_format}: {e}")
            raise

    return transformer
