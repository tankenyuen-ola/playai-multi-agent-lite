# Multi-Agent Project

A powerful framework for building and managing multi-agent systems using Google's Generative AI (Gemini) API. This project provides utilities for token management, agent communication, and system orchestration.

## New Feature
Local Deployment of LLMs (currently supports Qwen2.5-7b-instruct, more models incoming)

Method 1: Using FastAPI

Switch between models via the following endpoints:
	•	/multi-agent/gemini
	•	/multi-agent/qwen

Make sure your local models are stored in the models directory.

## Features

- 🤖 Multi-agent system architecture
- 🔢 Token counting and management
- 💬 Agent communication protocols
- ⚙️ Configuration management
- 📝 Prompt templating and management
- 🔄 System orchestration

## Example Outputs

The system demonstrates different agent personalities and emotional responses. Here are some example interactions:

### Agent Personalities

#### Agent 1 (Humorous)
```
用户问: 说个笑话我听
emotion guide index: 4
agent code: agent_1

哈哈，没问题！
话说，我发现最近我的钱包越来越瘦了， 感觉它在减肥... 哎呀，成年人的生活啊！
```

#### Agent 2 (Empathetic)
```
用户问: 我心情不好
emotion guide index: 1
agent code: agent_2

(´･ω･`) 怎么啦？ 发生什么事了？

用户问: 你喜欢吃什么
emotion guide index: 1
agent code: agent_2

哇，吃的呀！(≧∇≦)/
我喜欢吃的东西可多了，不过要说最喜欢的，大概是甜品吧，比如蛋糕、冰淇淋什么的，心情不好的时候吃一口，真的超治愈！😋 你呢，喜欢吃什么呀？
```

#### Agent 3 (Playful)
```
用户问: 你真漂亮
emotion guide index: 4
agent code: agent_3

哎哟，谢谢啊，不过你是不是想说点啥？ 哈哈

用户问: 你是傻傻的
emotion guide index: 4
agent code: agent_3

哇！你才傻傻的，你全家都傻傻的！哼！
```

#### Agent 4 (Relatable)
```
用户问: 不想上班
emotion guide index: 1
agent code: agent_4

不想上班+1 😭 真的不想上班不想上学不想动...
```

### Emotional Response System

The system uses an emotion guide index to modulate responses:
- Index 1: Empathetic and caring responses
- Index 4: Playful and humorous responses

Each agent maintains its unique personality while adapting to the emotional context of the conversation.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Poetry (Python package manager)
- Google Generative AI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multi-agent.git
cd multi-agent
```

2. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies using Poetry:
```bash
poetry install
```

4. Activate the virtual environment:
```bash
poetry shell
```

5. Set up your environment variables:
```bash
export GEMINI_API_KEY=your_api_key_here
```

## Usage Examples

### Token Counting Example

The project includes a token counting utility that helps you calculate and track token usage with the Gemini API.

#### Running the Example

There are two ways to run the token counting example:

1. From the project root:
```bash
poetry run python run_token_example.py
```

2. Directly from the examples directory:
```bash
poetry run python examples/token_counting_example.py
```

The example demonstrates:
- Input token counting
- Output token estimation
- Text generation with Gemini API
- Actual token usage calculation

## Project Structure

```
multi-agent/
├── core/                  # Core functionality
│   ├── api/              # API clients and utilities
│   ├── config/           # Configuration management
│   └── prompt/           # Prompt templates and classes
├── examples/             # Example scripts and demos
├── docs/                 # Documentation
├── tests/               # Test suite
├── pyproject.toml       # Poetry project configuration
├── poetry.lock          # Poetry lock file
└── README.md           # This file
```

## Development

### Setting Up Development Environment

1. Install development dependencies:
```bash
poetry install --with dev
```

2. Run tests:
```bash
poetry run pytest
```

3. Add new dependencies:
```bash
poetry add package-name
poetry add --group dev package-name  # For development dependencies
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Documentation

Detailed documentation is available in the `docs/` directory:
- API Reference
- Architecture Guide
- Best Practices
- Tutorials

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:
1. Check the [documentation](docs/)
2. Open an issue
3. Contact the maintainers

## Acknowledgments

- Google Generative AI Team
- Contributors and maintainers
- Open source community 
