MCP Hackathon Project: AI Agentic System
Welcome to the repository for our submission to the Agents & MCP Hackathon 2025. This project explores the integration of AI agents with the Model Context Protocol (MCP) to create interactive and intelligent systems.

🚀 Project Overview
This project aims to demonstrate the capabilities of AI agents in processing and responding to user inputs by leveraging the MCP framework. The system is designed to:

Accept user queries or commands.

Process the input using AI models.

Generate appropriate responses or actions.

Provide an interactive interface for user engagement.

🗂️ Repository Structure
agent.ipynb: Jupyter notebook detailing the development and testing of the AI agent.

code_client.py: Client-side script to send requests to the MCP server.

gradio_mcp.py: Script to launch the Gradio interface integrated with MCP.

igdb_api.ipynb: Notebook demonstrating the integration with the IGDB API for game-related data.

server.py: Backend server handling requests and interfacing with the AI agent.

.gitignore: Specifies files and directories to be ignored by Git.

.python-version: Specifies the Python version used.

pyproject.toml: Project metadata and dependencies.

uv.lock: Lock file for dependencies.

.gradio/flagged: Directory for storing flagged examples from the Gradio interface.

🛠️ Setup Instructions
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/Ashutosh212/mcp_hackathon.git
cd mcp_hackathon
Create a Virtual Environment:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
Install Dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Note: If requirements.txt is not present, install dependencies as specified in pyproject.toml.

Run the Gradio Interface:

bash
Copy
Edit
python gradio_mcp.py
This will launch the Gradio interface in your default web browser.

🌐 Live Demo
Experience the live demo of the project here: Live Demo Link (Replace with actual link if available)

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

🤝 Acknowledgments
Hugging Face for organizing the Agents & MCP Hackathon.

Gradio for providing an easy-to-use interface framework.

IGDB API for game-related data integration.

