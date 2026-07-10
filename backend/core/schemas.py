from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class AgentOutput(BaseModel):
    entities: List[Dict[str, Any]] = []
    relations: List[Dict[str, Any]] = []
    summary: str = ""
    raw: Dict[str, Any] = {}

class AgentSpec(BaseModel):
    id: str
    name: str
    description: str
    system_prompt: str
    tools: List[str] = []
    input_schema: Dict[str, Any] = {}
    output_schema: Dict[str, Any] = {}

class RunInput(BaseModel):
    agent_id: str
    project_id: str
    input: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None

class RunResponse(BaseModel):
    run_id: str
    agent_id: str
    status: str
    created_at: datetime

class SettingsInput(BaseModel):
    provider: str
    api_key: str
    model_name: str

class SettingsOutput(BaseModel):
    provider: str
    api_key_masked: str
    model_name: str

class NodeUpdateInput(BaseModel):
    label: str
    type: str

class NodeMergeInput(BaseModel):
    target_id: str

class EdgeCreateInput(BaseModel):
    project_id: str
    source_id: str
    target_id: str
    relation_type: str
