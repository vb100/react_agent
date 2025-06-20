# ReactAgent

## 📺 Watch the Tutorial

[▶️ How to Build a React Agent from Scratch with Python](https://youtu.be/GSep4L4vS08?si=HQQn5ToI-0B4YfeA)

**ReactAgent** is a minimalist, Python‑powered AI agent framework that follows the core principles of the ReAct pattern—**Reason + Action**. With ReAct, your agent alternates between thinking (analyzing user input, deciding next steps) and acting (calling functions, generating API requests), resulting in transparent, debuggable decision flows. This repository shows you how to implement a fully‑functional ReactAgent from scratch using **only the OpenAI API**, without any third‑party frameworks like LangChain.  

In this step‑by‑step tutorial, you’ll learn how to:  
1. **Import dependencies** and prepare your Python environment  
2. **Set up the OpenAI client** for secure, authenticated API calls  
3. **Define an `Agent` class**, including `__call__` and `execute` methods  
4. **Write a system prompt** that guides agent behavior  
5. **Create custom functions** your agent can trigger at runtime  
6. **Parse actions with RegEx**, dispatching work to the right handler  
7. **Simulate a conversation loop** and perform live tests with real questions  

Every concept is explained in detail, with code snippets and commentary designed for both beginners taking their first steps into AI‑agent development and advanced users looking for a lightweight, no‑boilerplate solution.

## Requirements

- **Python 3.8+**  
- An **OpenAI API key** (set as `OPENAI_API_KEY` environment variable)  
- `openai` Python package (`pip install openai`)  
- Basic familiarity with Python classes and regular expressions  

## Getting Started

1. **Clone this repo**  
   ```bash
   git clone https://github.com/your‑username/reactagent.git
   cd react_agent

1. **Install dependencies**
   ```bash
   pip install openai==1.59.7
