# Llm-showdown

This project allows you to compare the performance of different Large Language Models (LLMs) using various system prompts and user inputs. Results are stored in a CSV file for easy analysis.

## Table of Contents
- [Llm-showdown](#llm-showdown)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Folder Structure](#folder-structure)
  - [Setup Instructions](#setup-instructions)
    - [1. Create and Activate Virtual Environment](#1-create-and-activate-virtual-environment)
    - [2. Install Dependencies](#2-install-dependencies)
    - [3. Add API Keys](#3-add-api-keys)
  - [Usage](#usage)
    - [Run the Script](#run-the-script)
    - [View Results](#view-results)
  - [Configuration](#configuration)
    - [LLM Configuration](#llm-configuration)
    - [User Input CSV](#user-input-csv)
    - [System Prompts](#system-prompts)
  - [Customizations](#customizations)
    - [Adding New LLMs](#adding-new-llms)
    - [Advanced Prompt Formatting](#advanced-prompt-formatting)

---

## Features
- Compare multiple LLMs using system prompts and user inputs.
- Structured results stored in a CSV file for analysis.
- Modular configuration using a JSON file for LLM settings.
- Supports dynamic imports for adding new LLMs.

---

## Folder Structure


my-llm-comparison-project/
├─ .env                 # Stores API keys and environment variables
├─ requirements.txt     # Python dependencies
├─ main.py              # Main script for running the comparisons
├─ data/                # Folder containing user inputs and prompts
│  ├─ user_input.csv    # CSV with user messages
│  └─ prompts/          # Folder containing system prompt .txt files
├─ configs/
│  └─ llm_configs.json  # JSON file specifying LLM configurations
├─ results/
│  └─ combined_results.csv  # CSV file storing LLM responses
└─ .gitignore           # Ignored files and folders


---

## Setup Instructions

### 1. Create and Activate Virtual Environment

1. Navigate to the project folder in your terminal.
2. Create a virtual environment:
   bash
   python3 -m venv venv
   
3. Activate the virtual environment:
   - *Linux/macOS*:
     bash
     source venv/bin/activate
     
   - *Windows*:
     bash
     venv\Scripts\activate
     

### 2. Install Dependencies

Install the required Python packages:
bash
pip install -r requirements.txt


### 3. Add API Keys

Create a .env file in the project root and add your API keys:
env
OPENAI_API_KEY=your_openai_key_here
GROQ_API_KEY=your_groq_key_here


---

## Usage

### Run the Script

Execute the main script to run comparisons:
bash
python main.py


### View Results

Results will be saved in a CSV file located in the results/ folder. By default, the file is named combined_results.csv.

---

## Configuration

### LLM Configuration

Modify the file configs/llm_configs.json to add or adjust LLM settings. Example structure:

json
[
  {
    "name": "OpenAI-GPT-4o-mini",
    "class": "langchain_openai.ChatOpenAI",
    "params": {
      "model": "gpt-4o-mini"
    }
  },
  {
    "name": "Groq-LLama3-8B-8192",
    "class": "langchain_groq.ChatGroq",
    "params": {
      "model": "llama3-8b-8192"
    }
  }
]


- name: A descriptive name for the model.
- class: The fully qualified class name for the model.
- params: Parameters specific to the model (e.g., model name).

### User Input CSV

Update data/user_input.csv to include the user messages. Example:


user_message
hi!
Can you tell me a joke?
Translate this sentence: "Good morning!"
What is the capital of France?


### System Prompts

Add or modify system prompts in the data/prompts/ folder. Each .txt file should contain a system message. Example file system1.txt:


You are a highly skilled translator. Translate the user's input into Italian.


---

## Customizations

### Adding New LLMs

To add a new LLM:
1. Install the required Python package.
2. Add the configuration to configs/llm_configs.json:
   json
   {
     "name": "MyNewLLM",
     "class": "my_library.MyNewLLM",
     "params": {
       "model": "new-model-name"
     }
   }
   
3. Ensure the required API keys or settings are added to .env if needed.

### Advanced Prompt Formatting

If your use case requires structured prompts, you can customize the messages list in main.py:

python
from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Translate this to French: 'Good morning!'")
]