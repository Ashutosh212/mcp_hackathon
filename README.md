# 🧠 MCP Hackathon Project: AI Agentic System

Welcome to the repository for our submission to the Agents & MCP Hackathon 2025. This project explores the integration of AI agents with the Model Context Protocol (MCP) to create interactive and intelligent systems.

## 🚀 Project Overview

This project aims to demonstrate the capabilities of AI agents in processing and responding to user inputs by leveraging the MCP framework. The system is designed to:

- Accept user queries or commands
- Process the input using AI models
- Generate appropriate responses or actions
- Provide an interactive interface for user engagement

## 🗂️ Repository Structure

```
mcp_hackathon/
├── agent.ipynb              # Jupyter notebook detailing the development and testing of the AI agent
├── code_client.py           # Client-side script to send requests to the MCP server
├── gradio_mcp.py           # Script to launch the Gradio interface integrated with MCP
├── igdb_api.ipynb          # Notebook demonstrating the integration with the IGDB API for game-related data
├── server.py               # Backend server handling requests and interfacing with the AI agent
├── .gitignore              # Specifies files and directories to be ignored by Git
├── .python-version         # Specifies the Python version used
├── pyproject.toml          # Project metadata and dependencies
├── uv.lock                 # Lock file for dependencies
└── .gradio/flagged/        # Directory for storing flagged examples from the Gradio interface
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.8+ (check `.python-version` for specific version)
- Git

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Ashutosh212/mcp_hackathon.git
   cd mcp_hackathon
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   *Note: If `requirements.txt` is not present, install dependencies as specified in `pyproject.toml`:*
   ```bash
   pip install -e .
   ```

4. **Run the Gradio Interface:**
   ```bash
   python gradio_mcp.py
   ```
   
   This will launch the Gradio interface in your default web browser.

## 🎮 Features

- **Interactive AI Agent**: Powered by MCP framework for intelligent responses
- **Gradio Web Interface**: User-friendly interface for seamless interaction
- **IGDB API Integration**: Access to comprehensive game database for gaming-related queries
- **Jupyter Notebooks**: Detailed development process and API demonstrations
- **Modular Architecture**: Separate client-server architecture for scalability

## 🌐 Live Demo

Experience the live demo of the project here: [Live Demo Link](https://your-demo-link.com) *(Replace with actual link if available)*

## 🔧 Usage

### Running the Server
```bash
python server.py
```

### Using the Client
```bash
python code_client.py
```

### Exploring the Notebooks
Open the Jupyter notebooks to understand the development process:
- `agent.ipynb` - AI agent development and testing
- `igdb_api.ipynb` - IGDB API integration examples

## 🤖 Technical Stack

- **AI Framework**: Model Context Protocol (MCP)
- **Interface**: Gradio
- **Backend**: Python
- **APIs**: IGDB API for gaming data
- **Development**: Jupyter Notebooks

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- **Hugging Face** for organizing the Agents & MCP Hackathon
- **Gradio** for providing an easy-to-use interface framework
- **IGDB API** for game-related data integration
- **MCP Community** for the excellent framework and documentation

## 📧 Contact

For questions or suggestions, please reach out:
- GitHub: [@Ashutosh212](https://github.com/Ashutosh212)
- Project Link: [https://github.com/Ashutosh212/mcp_hackathon](https://github.com/Ashutosh212/mcp_hackathon)

---

*Built with ❤️ for the Agents & MCP Hackathon 2025*
