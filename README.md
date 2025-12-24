# MCP Customer Support Chatbot (Prototype)

This project is a **local prototype** of a Customer Support chatbot for a company that sells computer products (monitors, printers, and accessories).

The chatbot uses:
- **Model Context Protocol (MCP)** to access company-provided tools and context via an HTTP server
- A **lightweight LLM** accessed through **OpenRouter** for cost-efficient reasoning
- **Streamlit** to provide a simple interactive demo UI that runs locally

The goal of this prototype is to demonstrate correct MCP integration, tool-aware LLM orchestration, and a working end-to-end user experience.

---

## Project Structure

```
mcp_chatbot/
├── app.py            # Streamlit UI and chat loop
├── chatbot.py        # Chat orchestration logic (LLM + MCP)
├── llm_client.py     # LLM client wrapper
├── mcp_client.py     # MCP HTTP client
├── requirements.txt  # Python dependencies
├── .env.example      # template of `.env` file with environment variables
├── LICENSE           # MIT license
└── README.md         # This file
```

### File Overview

- **app.py**
  - Streamlit-based UI
  - Handles user input, session state, and rendering messages
  - Ensures exactly-once message processing (prevents duplicate requests)

- **chatbot.py**
  - Central orchestration layer
  - Builds prompts, calls the LLM, and invokes MCP tools when needed

- **llm_client.py**
  - Wraps the LLM API using an OpenAI-compatible client
  - Configurable model, base URL, and API key via environment variables

- **mcp_client.py**
  - Simple HTTP client for communicating with the MCP server
  - Sends tool payloads and returns structured responses

---

## High-Level Workflow

1. **User enters a question** in the Streamlit UI  
   (e.g., “Prices of the monitors and printers”)

2. **Chatbot builds context**
   - System prompt
   - Conversation history
   - User message

3. **LLM is called via OpenRouter**
   - Uses a lightweight, cost-efficient model
   - Decides whether an MCP tool is required

4. **MCP tool call (if needed)**
   - The chatbot sends a request to the MCP server
   - MCP returns structured product or troubleshooting data

5. **Final LLM response**
   - MCP results are injected back into the conversation
   - The LLM generates a user-facing answer

6. **Response is displayed**
   - Chat history is updated
   - Input is cleared safely to prevent duplicate submissions

---

## Requirements

- Tested with Python **3.9.7**
- Internet access (for OpenRouter and MCP server)

---

## Environment Variables

Create a `.env` file in the project root folder, following the `.env.example` file

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Running the Application Locally

```bash
streamlit run app.py
```

Then open the browser at:

```
http://localhost:8501
```

---

## MCP Server

This prototype connects to a company-provided MCP server via HTTP:

```
https://vipfapwm3x.us-east-1.awsapprunner.com/mcp
```

The MCP server exposes tools and contextual information used by the chatbot to provide accurate, company-specific support responses.

---

## Design Notes

- The application is intentionally **kept simple** to focus on MCP usage rather than UI complexity.
- The LLM provider is abstracted so models or vendors can be swapped easily.
- The system is fully runnable **locally**, and not deployed on cloud.

---

## Future Improvements (Out of Scope)

- Streaming responses (LLM + MCP)
- LangChain + LangFuse observability
- Persistent chat history
- Retry and fallback logic for MCP failures
- Deployment to a hosted environment

---
