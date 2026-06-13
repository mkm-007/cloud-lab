from cloudlab.agent import DEFAULT_SYSTEM_PROMPT, WorkflowAgent


def test_agent_lists_project_secrets():
    agent = WorkflowAgent()
    payload = agent.list_project_secrets("web-app")
    assert payload["count"] == 3
    assert payload["secrets"][0]["name"] == "DATABASE_URL"


def test_grounded_response_passes():
    agent = WorkflowAgent()
    run = agent.run("list secrets", "auth")
    assert run.grounded is True
    assert run.hallucination is False


def test_hallucination_detected_in_draft():
    agent = WorkflowAgent()
    draft = "Project auth has secrets: JWT_SIGNING_KEY, OAUTH_CLIENT_SECRET, SK-LIVE-KEY."
    run = agent.run_with_draft("audit secrets", "auth", draft)
    assert run.hallucination is True


def test_missing_secret_fails_grounding():
    agent = WorkflowAgent()
    draft = "Project web-app has 3 secrets: DATABASE_URL, API_KEY."
    run = agent.run_with_draft("summarize", "web-app", draft)
    assert run.grounded is False


def test_system_prompt_requires_tool_use():
    assert "tool outputs" in DEFAULT_SYSTEM_PROMPT.lower()


def test_agent_run_records_tool_name():
    agent = WorkflowAgent()
    run = agent.run("workflow audit", "billing")
    assert run.tool_name == "list_project_secrets"
    assert run.tool_result["count"] == 1
