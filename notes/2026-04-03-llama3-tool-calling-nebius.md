# Llama 3.3 70B Tool Calling Failure on Nebius Token Factory

## Problem

When using `meta-llama/Llama-3.3-70B-Instruct` via Nebius Token Factory's OpenAI-compatible endpoint with LangChain's `ChatOpenAI` + `create_agent`, tool calls are **not extracted** into LangChain's structured `tool_calls` field. Instead, the raw JSON appears in the message `content`:

```
'["{\"type\": \"function\", \"name\": \"check_pub_availability\", \"parameters\": {\"pub_name\": \"The Albanach\", \"required_capacity\": \"160\", ...'
```

Using `Qwen/Qwen3-32B` on the same endpoint with the same code works correctly.

## Root Cause: Server-Side Tool Call Parsing

This is **not a LangChain/LangGraph prompt template issue**. The problem sits at the **Nebius inference server** level (vLLM-based).

### How OpenAI-compatible tool calling works

When `tools=` is passed to an OpenAI-compatible API, two things need to happen:

1. **Request side**: The server injects tool definitions into the model's prompt using the correct **chat template** for that specific model (Llama 3 uses a different format than Qwen).
2. **Response side**: The server must **parse** the model's raw text output and extract tool calls into the structured `tool_calls` field of the API response.

### Why Qwen3-32B works and Llama 3.3 70B doesn't

- **Qwen3-32B** has robust tool calling support in vLLM. Its chat template natively handles `tools` in the OpenAI format, and the server correctly parses output into structured `tool_calls` objects.
- **Llama 3.3 70B** uses a different native tool calling format (with `<|python_tag|>` markers and its own JSON structure). The Nebius server does not correctly parse Llama 3.3's raw tool call output into the OpenAI-compatible `tool_calls` response format. The model's raw text gets dumped into the `content` field instead.

LangChain's `ChatOpenAI` then sees `content=<raw JSON string>` with `tool_calls=[]`, so `m.tool_calls` is empty.

### Supporting Evidence

- Nebius's own function calling docs use `meta-llama/Meta-Llama-3.1-8B-Instruct-fast` in examples -- a different variant with likely different server-side support.
- Known class of issue with vLLM-based providers:
  - [vllm-project/vllm#14951](https://github.com/vllm-project/vllm/issues/14951) -- "vLLM response on tool_calls does not align with OpenAI standard"
  - [vllm-project/vllm#14269](https://github.com/vllm-project/vllm/pull/14269) -- added a specific `tool_chat_template_llama3.3_json.jinja` template, indicating special handling was needed
- The model name on Nebius (`meta-llama/Llama-3.3-70B-Instruct`) may not have the correct tool-call chat template enabled server-side.

## Workarounds

1. **Use Qwen3-32B** for tool-calling tasks on Nebius -- it works because the server has proper support for it.
2. **Check for a `-fast` or tool-specific variant** of Llama 3.3 on Nebius (like the `Meta-Llama-3.1-8B-Instruct-fast` in their docs) that might have better tool call parsing.
3. **Manual parsing** (not recommended): Write a custom output parser that catches raw JSON in `content` when `tool_calls` is empty, but this defeats the purpose of LangGraph's built-in agent loop.
