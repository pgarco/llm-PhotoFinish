# Llm-PhotoFinish

This project allows you to compare the performance of different Large Language Models (LLMs) and save results with the call and paramenters to ease reproducibility, replication and transparency in analysis.

## Table of Contents
- [Llm-PhotoFinish](#llm-showdown)
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
---

## Features
- Compare multiple LLMs using system prompts and user inputs.
- Structured results stored in a CSV file for analysis.
- Modular configuration using a JSON file for LLM settings.
- Supports dynamic imports for adding new LLMs.

---

## Folder Structure


llm-PhotoFinish
├── .env                 
├── requirements.txt     
├── main.py              
├── data                 
│   ├── user_input.csv    
│   └──prompts           
├──  configs
│   └──llm_configs.json
├── results
│   └── combined_results.csv
└── .gitignore


---

## Setup Instructions

### 1. Create and Activate Virtual Environment
     
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

Results will be saved in a CSV file located in the results/ folder.

---

## Configuration

### LLM Configuration

Modify the file configs/llm_configs.json to add or adjust LLM settings.

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

Update data/user_input.csv to include the user messages.


### System Prompts

Add or modify system prompts in the data/prompts/ folder. Each .txt file should contain a system message.

