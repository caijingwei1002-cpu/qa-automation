"""Tiny JSONL process used to test the Codex App Server bridge."""

from __future__ import annotations

import json
import sys


def send(value: dict) -> None:
    sys.stdout.write(json.dumps(value, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def main() -> None:
    turns: list[dict] = []
    materialized = False
    for raw_line in sys.stdin:
        message = json.loads(raw_line)
        method = message.get("method")
        request_id = message.get("id")
        params = message.get("params") or {}
        if method == "initialized":
            continue
        if method == "initialize":
            send({"id": request_id, "result": {"serverInfo": {"name": "fake-codex"}}})
        elif method == "account/read":
            send({"id": request_id, "result": {"account": {"type": "chatgpt", "planType": "test"}, "requiresOpenaiAuth": True}})
        elif method == "account/login/start":
            send({"id": request_id, "result": {"type": "chatgpt", "loginId": "login-1", "authUrl": "https://example.invalid/login"}})
        elif method == "thread/start":
            if params.get("approvalPolicy") != "on-request":
                send({"id": request_id, "error": {"message": "invalid approvalPolicy"}})
            elif params.get("sandbox") != "workspace-write":
                send({"id": request_id, "error": {"message": "invalid sandbox"}})
            else:
                send({"id": request_id, "result": {"thread": {"id": "fake-thread", "turns": []}}})
        elif method == "thread/resume":
            if params["threadId"] == "missing-thread":
                send({"id": request_id, "error": {"message": "no rollout found for thread id missing-thread"}})
            else:
                send({"id": request_id, "result": {"thread": {"id": params["threadId"]}}})
        elif method == "thread/read":
            if not materialized and params.get("includeTurns"):
                send({"id": request_id, "error": {"message": "thread is not materialized yet"}})
            else:
                send({"id": request_id, "result": {"thread": {"id": params["threadId"], "turns": turns}}})
        elif method == "turn/start":
            if params.get("approvalPolicy") != "on-request":
                send({"id": request_id, "error": {"message": "invalid approvalPolicy"}})
                continue
            text = params["input"][0]["text"]
            materialized = True
            turn_id = f"turn-{len(turns) + 1}"
            user = {"id": f"user-{turn_id}", "type": "userMessage", "content": [{"type": "text", "text": text}]}
            assistant = {"id": f"agent-{turn_id}", "type": "agentMessage", "text": "这是模拟教练回复。"}
            turns.append({"id": turn_id, "status": "completed", "items": [user, assistant]})
            send({"id": request_id, "result": {"turn": {"id": turn_id, "status": "inProgress", "items": []}}})
            send({"method": "turn/started", "params": {"threadId": params["threadId"], "turn": {"id": turn_id, "status": "inProgress", "items": []}}})
            send({"method": "item/started", "params": {"threadId": params["threadId"], "turnId": turn_id, "item": user}})
            send({"method": "item/completed", "params": {"threadId": params["threadId"], "turnId": turn_id, "item": user}})
            send({"method": "item/started", "params": {"threadId": params["threadId"], "turnId": turn_id, "item": assistant}})
            send({"method": "item/agentMessage/delta", "params": {"threadId": params["threadId"], "turnId": turn_id, "itemId": assistant["id"], "delta": "这是模拟教练回复。"}})
            if "approval" in text:
                send({"id": 900, "method": "item/commandExecution/requestApproval", "params": {"threadId": params["threadId"], "turnId": turn_id, "itemId": "cmd-1", "command": "pytest -q", "reason": "验证学习成果"}})
            send({"method": "item/completed", "params": {"threadId": params["threadId"], "turnId": turn_id, "item": assistant}})
            send({"method": "turn/completed", "params": {"threadId": params["threadId"], "turn": {"id": turn_id, "status": "completed", "items": [assistant]}}})
        elif method == "turn/interrupt":
            send({"id": request_id, "result": {}})
        elif request_id is not None and "result" in message:
            send({"method": "serverRequest/resolved", "params": {"threadId": "fake-thread", "requestId": request_id}})
        else:
            send({"id": request_id, "error": {"message": f"unsupported: {method}"}})


if __name__ == "__main__":
    main()
