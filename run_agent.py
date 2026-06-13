#!/usr/bin/env python3
"""Agentic workflow demo — tool use, prompt grounding, and hallucination checks."""
import json

from cloudlab.agent import WorkflowAgent


def main() -> None:
    agent = WorkflowAgent()
    run = agent.run("summarize secrets", "web-app")
    bad = agent.run_with_draft(
        "summarize secrets",
        "web-app",
        "Project web-app has 3 secrets: DATABASE_URL, API_KEY, REDIS_URL, SK-LIVE-KEY.",
    )
    print(
        json.dumps(
            {
                "system_prompt": run.system_prompt,
                "tool": run.tool_name,
                "tool_result": run.tool_result,
                "response": run.response,
                "grounded": run.grounded,
                "hallucination": run.hallucination,
                "hallucination_example_flagged": bad.hallucination,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
