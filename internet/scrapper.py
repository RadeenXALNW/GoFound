from scrapegraphai.graphs import SearchGraph
from langchain_community.document_loaders import WebBaseLoader
import re
import json
from datetime import datetime

def extract_webpage_content(url):
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        
        if docs:
            content = docs[0].page_content
            # Remove excess whitespace
            content = re.sub(r'\s+', ' ', content).strip()
            # Split content into sentences
            sentences = re.split(r'(?<=[.!?])\s+', content)
            # Filter out incomplete sentences
            complete_sentences = [s for s in sentences if len(s.split()) >= 3]
            # Join the complete sentences
            filtered_content = ' '.join(complete_sentences)
            return filtered_content
        return None
    except Exception as e:
        print(f"Error extracting content from {url}: {str(e)}")
        return None

def save_results_to_file(search_results, url_contents, timestamp):
    output = {
        "timestamp": timestamp,
        "search_results": search_results,
        "extracted_contents": url_contents
    }
    
    # Save as JSON
    with open(f"search_results_{timestamp}.json", "w", encoding='utf-8') as json_file:
        json.dump(output, json_file, indent=4, ensure_ascii=False)
    
    # Save as TXT
    with open(f"search_results_{timestamp}.txt", "w", encoding='utf-8') as txt_file:
        txt_file.write(f"Search Results - {timestamp}\n")
        txt_file.write("=" * 50 + "\n\n")
        
        txt_file.write("Key Nutrients:\n")
        for nutrient in search_results['key_nutrients']:
            txt_file.write(f"- {nutrient}\n")
        
        txt_file.write("\nExtracted Content from Sources:\n")
        txt_file.write("=" * 50 + "\n")
        
        for url, content in url_contents.items():
            txt_file.write(f"\nSource: {url}\n")
            txt_file.write("-" * 30 + "\n")
            txt_file.write(content + "\n")

def main():
    config = {
        "llm": {
            "api_key": "sk****",
            "model": "openai/gpt-4o-mini",
        },
        "max_results": 3,
        "headless": True,
        "verbose": True,
        "playwright": {
            "chromium": {
                "launch_options": {
                    "headless": True
                }
            }
        }
    }

    search_prompt = "What are the key nutrients needed for a healthy diet?"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        # Initialize and run search
        search_graph = SearchGraph(
            prompt=search_prompt,
            config=config
        )
        result = search_graph.run()
        urls = search_graph.get_considered_urls()

        # Print initial results
        print("\nSearch Results:")
        print(result)
        print("\nConsidered URLs:")
        for url in urls:
            print(f"- {url}")

        # Extract content from each URL
        url_contents = {}
        print("\nExtracting content from URLs...")
        for url in urls:
            print(f"Processing: {url}")
            content = extract_webpage_content(url)
            if content:
                url_contents[url] = content
                print(f"Successfully extracted content from: {url}")
            else:
                print(f"Failed to extract content from: {url}")

        # Save all results
        save_results_to_file(result, url_contents, timestamp)
        print(f"\nResults saved to search_results_{timestamp}.json and search_results_{timestamp}.txt")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()