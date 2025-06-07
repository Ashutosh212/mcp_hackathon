title: "🧠 MCP Hackathon Project: AI Agentic System"
description: >
  This project explores the integration of AI agents with the Model Context Protocol (MCP) to create interactive and intelligent systems.
hackathon:
  name: "Agents & MCP Hackathon 2025"
  url: "https://huggingface.co/Agents-MCP-Hackathon"
project_overview:
  - Accept user queries or commands.
  - Process the input using AI models.
  - Generate appropriate responses or actions.
  - Provide an interactive interface for user engagement.
repository_structure:
  - file: "agent.ipynb"
    description: "Jupyter notebook detailing the development and testing of the AI agent."
  - file: "code_client.py"
    description: "Client-side script to send requests to the MCP server."
  - file: "gradio_mcp.py"
    description: "Script to launch the Gradio interface integrated with MCP."
  - file: "igdb_api.ipynb"
    description: "Notebook demonstrating the integration with the IGDB API for game-related data."
  - file: "server.py"
    description: "Backend server handling requests and interfacing with the AI agent."
  - file: ".gitignore"
    description: "Specifies files and directories to be ignored by Git."
  - file: ".python-version"
    description: "Specifies the Python version used."
  - file: "pyproject.toml"
    description: "Project metadata and dependencies."
  - file: "uv.lock"
    description: "Lock file for dependencies."
  - file: ".gradio/flagged/"
    description: "Directory for storing flagged examples from the Gradio interface."
setup_instructions:
  - step: "Clone the Repository"
    commands:
      - git clone https://github.com/Ashutosh212/mcp_hackathon.git
      - cd mcp_hackathon
  - step: "Create a Virtual Environment"
    commands:
      - python3 -m venv venv
      - source venv/bin/activate
  - step: "Install Dependencies"
    commands:
      - pip install -r requirements.txt
    note: "If `requirements.txt` is not present, install dependencies as specified in `pyproject.toml`."
  - step: "Run the Gradio Interface"
    commands:
      - python gradio_mcp.py
    note: "This will launch the Gradio interface in your default web browser."
live_demo:
  description: "Experience the live demo of the project here"
  link: "#"
license:
  type: "MIT"
  file: "LICENSE"
acknowledgments:
  - name: "Hugging Face"
    url: "https://huggingface.co/"
    reason: "Organizing the Agents & MCP Hackathon"
  - name: "Gradio"
    url: "https://gradio.app/"
    reason: "Providing an easy-to-use interface framework"
  - name: "IGDB API"
    url: "https://api.igdb.com/"
    reason: "Game-related data integration"
