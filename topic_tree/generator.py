from pluto import EngineArguments, DataEngine, Dataset, TopicTree, TopicTreeArguments
import os
from dotenv import load_dotenv
from pathlib import Path
import json


# Set up OpenAI API Key from environment variable
base_dir = Path(__file__).resolve().parent.parent
print(base_dir)

# Construct the path to the .env file
dotenv_path = base_dir / '.env'

# Load the .env file
load_dotenv(dotenv_path)


os.getenv("OPENAI_API_KEY")



def generate_topic_trees(root_prompts):
    system_prompt = "You are a helpful AI coding assistant. You do not just give high level coding advice, but instead, you respond to coding questions with specific code examples."
    all_trees = []

    for root_prompt in root_prompts:
        tree = TopicTree(
            args=TopicTreeArguments(
                root_prompt=root_prompt,
                model_system_prompt=system_prompt,
                tree_degree=1,
                tree_depth=1
            )
        )

        tree.build_tree(model_name="gpt-4o-mini")

        temp_filename = f"temp_{root_prompt.replace(' ', '_')}.jsonl"
        tree.save(temp_filename)

        with open(temp_filename, "r", encoding="utf-8") as temp_file:
            for line in temp_file:
                all_trees.append(json.loads(line))

        os.remove(temp_filename)

    return all_trees


if __name__ == "__main__":
    # Test root prompts
    test_prompts = [
        "nutrients",
        "vitamin D"
    ]
    
    # Generate topic trees
    trees = generate_topic_trees(test_prompts)
    
    # Print the results
    print(f"Generated {len(trees)} topic trees:")
    for tree in trees:
        print(json.dumps(tree, indent=2))