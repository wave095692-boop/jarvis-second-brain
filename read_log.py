import json

log_path = "/Users/apple/.gemini/antigravity-ide/brain/8107daaa-f0f2-4535-b751-7c4d1a1f6591/.system_generated/logs/transcript.jsonl"
with open(log_path, "r") as f:
    for line in f:
        data = json.loads(line)
        idx = data.get("step_index", 0)
        if 180 <= idx <= 306:
            print(f"Step {idx} ({data.get('source')}): {data.get('type')}")
            content = data.get("content", "")
            if content:
                print(content[:350] + ("..." if len(content) > 350 else ""))
            tool_calls = data.get("tool_calls", [])
            if tool_calls:
                for tc in tool_calls:
                    print(f"  Tool: {tc.get('name')} with args {tc.get('arguments')}")
            print("-" * 40)
