# from langchain_community.retrievers import WikipediaRetriever

# retriever = WikipediaRetriever()

# docs = retriever.invoke("vitamin D")
# print(docs)

from langchain_community.retrievers import WikipediaRetriever

def get_wiki_content(topic: str) -> str:
    """
    Extract and combine Wikipedia content for a given topic into a single paragraph.
    
    Args:
        topic (str): The topic to search for on Wikipedia
    
    Returns:
        str: Combined content from all retrieved documents
    """
    try:
        # Initialize retriever and get documents
        retriever = WikipediaRetriever()
        docs = retriever.invoke(topic)
        
        # Combine all document content into one string
        combined_content = ' '.join(doc.page_content for doc in docs)
        
        # Clean up any double spaces and extra whitespace
        cleaned_content = ' '.join(combined_content.split())
        
        return cleaned_content
        
    except Exception as e:
        return f"Error retrieving content: {str(e)}"

# Example usage
if __name__ == "__main__":
    content = get_wiki_content("vitamin D")
    print(content)