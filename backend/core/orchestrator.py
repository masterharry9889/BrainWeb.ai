import asyncio
import json
import os
from typing import Dict, Any
from .schemas import AgentSpec, AgentOutput
from ..services.pubsub import publish_event
from ..core.security import decrypt_api_key

# Built-in agents
BUILTIN_AGENTS = {
    "research-agent": AgentSpec(
        id="research-agent",
        name="Research Agent",
        description="Gathers information on a given topic.",
        system_prompt="You are a research agent.",
        input_schema={"topic": "string"},
        output_schema={"summary": "string", "entities": "array", "relations": "array"}
    ),
    "legal-doc-reviewer": AgentSpec(
        id="legal-doc-reviewer",
        name="Legal Doc Reviewer",
        description="Reviews contracts and flags risky clauses",
        system_prompt="You are a legal doc reviewer.",
        input_schema={"document": "string"},
        output_schema={"entities": "array", "relations": "array", "summary": "string"}
    )
}

class Orchestrator:
    def __init__(self):
        self.agents = BUILTIN_AGENTS.copy()

    def get_agents(self) -> Dict[str, AgentSpec]:
        return self.agents

    async def run_agent_async(self, run_id: str, agent_spec: AgentSpec, input_data: Dict[str, Any], context: Dict[str, Any], user_setting: Any = None):
        channel = f"runs:{run_id}"
        
        try:
            await publish_event(channel, "run.started", {"agent_id": agent_spec.id})
            
            if not user_setting:
                raise ValueError("No API key configured.")

            api_key = decrypt_api_key(user_setting.api_key_encrypted)
            provider = user_setting.provider
            model = user_setting.model_name
            
            from litellm import acompletion
            
            if provider == "groq":
                litellm_model = f"groq/{model}"
                os.environ["GROQ_API_KEY"] = api_key
            elif provider == "anthropic":
                # litellm requires anthropic/ prefix for some standard models if not recognized, 
                # but usually handles "claude-3-..." natively. To be safe:
                litellm_model = model if model.startswith("claude") else f"anthropic/{model}"
                os.environ["ANTHROPIC_API_KEY"] = api_key
            else:
                litellm_model = model
                os.environ["OPENAI_API_KEY"] = api_key

            schema_instruction = f"""
First, provide your conversational response to the user. You may use markdown formatting and links.
After your response, you MUST append a RAW JSON block enclosed in ```json ... ``` containing the entities and relations extracted from your response.

The JSON MUST conform exactly to this schema:
{json.dumps(agent_spec.output_schema)}

IMPORTANT:
- 'entities' MUST be an array of objects, each with 'id', 'label', and 'type' (e.g. {{"id": "moe", "label": "Mixture of Experts", "type": "Concept"}}).
- 'relations' MUST be an array of objects, each with 'source', 'target', and 'type' (e.g. {{"source": "moe", "target": "neural_net", "type": "is_a"}}).
"""

            messages = [
                {"role": "system", "content": agent_spec.system_prompt},
                {"role": "user", "content": f"Input: {json.dumps(input_data)}\n\n{schema_instruction}"}
            ]

            response = await acompletion(
                model=litellm_model,
                messages=messages,
                stream=True
            )

            full_response = ""
            async for chunk in response:
                content = chunk.choices[0].delta.content or ""
                if content:
                    full_response += content
                    await publish_event(channel, "run.token", {"token": content})
                    
            try:
                if "```json" in full_response:
                    json_str = full_response.split("```json")[-1].split("```")[0].strip()
                    parsed = json.loads(json_str)
                    summary = full_response.split("```json")[0].strip()
                else:
                    print("WARNING: LLM did not output a ```json block", flush=True)
                    parsed = {"entities": [], "relations": []}
                    summary = full_response
            except Exception as e:
                print(f"ERROR parsing LLM JSON output: {e}", flush=True)
                parsed = {"entities": [], "relations": []}
                summary = full_response
                
            output = AgentOutput(
                summary=summary,
                entities=parsed.get("entities", []),
                relations=parsed.get("relations", []),
                raw={"original_response": full_response}
            )
            
            await publish_event(channel, "run.finished", {
                "output": output.model_dump(),
                "context": context
            })
            
        except Exception as e:
            await publish_event(channel, "run.error", {"error": str(e)})

orchestrator = Orchestrator()
