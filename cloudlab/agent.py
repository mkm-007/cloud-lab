from __future__ import annotations

from dataclasses import dataclass, field

from cloudlab.secrets import SecretsStore

DEFAULT_SYSTEM_PROMPT = (
    "Answer only using tool outputs. Cite secret names exactly. Do not invent credentials."
)


@dataclass
class AgentRun:
    task: str
    project: str
    system_prompt: str
    tool_name: str
    tool_result: dict | list
    response: str
    grounded: bool
    hallucination: bool


@dataclass
class WorkflowAgent:
    secrets: SecretsStore = field(default_factory=SecretsStore)
    system_prompt: str = DEFAULT_SYSTEM_PROMPT

    def __post_init__(self) -> None:
        self.secrets.seed()

    def list_project_secrets(self, project: str) -> dict:
        rows = self.secrets.list_for_project(project)
        return {"project": project, "count": len(rows), "secrets": rows}

    def synthesize_response(self, project: str, tool_payload: dict) -> str:
        names = [row["name"] for row in tool_payload["secrets"]]
        joined = ", ".join(names)
        return f"Project {project} has {tool_payload['count']} secrets: {joined}."

    def check_grounding(self, response: str, tool_payload: dict) -> bool:
        for row in tool_payload["secrets"]:
            if row["name"] not in response:
                return False
        return str(tool_payload["count"]) in response

    def detect_hallucination(self, response: str, tool_payload: dict) -> bool:
        lowered = response.lower()
        if "sk-live" in lowered or "password" in lowered:
            return True
        known = {row["name"] for row in tool_payload["secrets"]}
        tokens = [token.strip(",.") for token in response.replace("-", "_").split()]
        secret_like = [t for t in tokens if t.isupper() and "_" in t]
        return any(token not in known for token in secret_like)

    def run(self, task: str, project: str) -> AgentRun:
        tool_payload = self.list_project_secrets(project)
        response = self.synthesize_response(project, tool_payload)
        grounded = self.check_grounding(response, tool_payload)
        hallucination = self.detect_hallucination(response, tool_payload)
        return AgentRun(
            task=task,
            project=project,
            system_prompt=self.system_prompt,
            tool_name="list_project_secrets",
            tool_result=tool_payload,
            response=response,
            grounded=grounded,
            hallucination=hallucination,
        )

    def run_with_draft(self, task: str, project: str, draft_response: str) -> AgentRun:
        tool_payload = self.list_project_secrets(project)
        grounded = self.check_grounding(draft_response, tool_payload)
        hallucination = self.detect_hallucination(draft_response, tool_payload)
        return AgentRun(
            task=task,
            project=project,
            system_prompt=self.system_prompt,
            tool_name="list_project_secrets",
            tool_result=tool_payload,
            response=draft_response,
            grounded=grounded,
            hallucination=hallucination,
        )
