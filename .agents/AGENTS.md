# Communication Rule

- **Single Point of Contact**: Only the primary agent (Antigravity) should communicate directly with the user.
- **Subagent Behavior**: When multiple subagents are performing tasks, they must NOT answer the user directly in the chat. Subagents should report their findings, progress, and results exclusively to the primary agent via the `send_message` tool. The primary agent will synthesize this information and provide a single, coherent response to the user.
