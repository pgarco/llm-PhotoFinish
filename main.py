import os
import json
from dotenv import load_dotenv
import pandas as pd
from glob import glob
from importlib import import_module
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# LangChain Core Message Types
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# Define input/output paths
USER_INPUT_CSV = os.path.join("data", "user_input.csv")
PROMPTS_FOLDER = os.path.join("data", "prompts")
LLM_CONFIGS_JSON = os.path.join("configs", "llm_configs.json")
RESULTS_CSV = os.path.join("results", "combined_results.csv")

def load_llm_configs(config_path):
    """Load LLM configurations from a JSON file."""
    print(f"Loading LLM configurations from {config_path}...")
    with open(config_path, "r", encoding="utf-8") as f:
        configs = json.load(f)
    for config in configs:
        # Dynamically import the model class
        module_name, class_name = config["class"].rsplit(".", 1)
        module = import_module(module_name)
        config["class"] = getattr(module, class_name)
    print(f"Loaded {len(configs)} LLM configurations.")
    return configs

def invoke_model(llm, messages):
    """Invoke a model with the given messages."""
    try:
        response = llm.invoke(messages)
        if hasattr(response, "content"):
            return response.content  # Extract content if available
        return str(response)  # Fallback to string representation
    except Exception as e:
        return f"ERROR: {e}"

def process_batch(llm_config, user_messages, prompt_path, system_prompt, batch_size):
    """Process a batch of user messages with a given LLM configuration."""
    llm_class = llm_config["class"]
    llm_name = llm_config["name"]
    llm_params = llm_config["params"]

    # Instantiate the model
    llm = llm_class(**llm_params)

    results = []
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        futures = []
        for user_msg in user_messages:
            # Construct the messages
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_msg),
            ]
            # Submit model invocation to the thread pool
            futures.append(executor.submit(invoke_model, llm, messages))

        # Collect results as they complete
        for future, user_msg in zip(as_completed(futures), user_messages):
            response_content = future.result()
            results.append({
                "user_message": user_msg,
                "system_prompt_file": os.path.basename(prompt_path),
                "model_name": llm_name,
                "llm_response": response_content,
            })
    return results

def main():
    print("Starting LLM Comparison Script...")

    # Load LLM configurations
    llm_configs = load_llm_configs(LLM_CONFIGS_JSON)

    # Read user messages
    print(f"Reading user messages from {USER_INPUT_CSV}...")
    user_messages = pd.read_csv(USER_INPUT_CSV)["user_message"].dropna().tolist()
    print(f"Loaded {len(user_messages)} user messages.")

    # Get all system prompt files
    print(f"Looking for prompt files in {PROMPTS_FOLDER}...")
    prompt_files = glob(os.path.join(PROMPTS_FOLDER, "*.txt"))
    print(f"Found {len(prompt_files)} prompt files: {', '.join([os.path.basename(f) for f in prompt_files])}")

    # Calculate total iterations for progress bar
    total_iterations = len(user_messages) * len(prompt_files) * len(llm_configs)
    print(f"Total iterations to process: {total_iterations}.")

    # Prepare results DataFrame
    results = []

    # Use tqdm for a progress bar
    with tqdm(total=total_iterations, desc="Processing LLM interactions") as pbar:
        for prompt_path in prompt_files:
            with open(prompt_path, "r", encoding="utf-8") as f:
                system_prompt = f.read()

            for llm_config in llm_configs:
                batch_size = llm_config.get("batch_size", 5)  # Default batch size
                print(f"Processing with model {llm_config['name']} using batch size {batch_size}...")

                # Process the batch
                batch_results = process_batch(llm_config, user_messages, prompt_path, system_prompt, batch_size)
                results.extend(batch_results)
                pbar.update(len(user_messages))

    # Save results to CSV
    print(f"Saving results to {RESULTS_CSV}...")
    results_df = pd.DataFrame(results)
    results_df.to_csv(RESULTS_CSV, index=False, encoding="utf-8")
    print(f"Results written to {RESULTS_CSV}. Script complete!")

main()