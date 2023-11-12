#' AIzaSyC4ZeKKTb3Dc-XB3nlrVwm0mpMRDvvWSDE '  #google custom search api key
# 'b46414dca715a4927'       # google custom search cx
#'LL-YbBwy6qtvi1E9TejD5aGHBm9O3IULERjK4ijXiBNffokVLMBMAAz7mzruClbcZTW' #api key goes here
import requests

llama_endpoint = 'LL-YbBwy6qtvi1E9TejD5aGHBm9O3IULERjK4ijXiBNffokVLMBMAAz7mzruClbcZTW'  #enter llama endpoint here

# Function to generate search queries using Llama 2
def generate_search_queries_llama(topic):
    response = requests.post(
        llama_endpoint,
        json={"input": f"Generate search queries to find articles about {topic}"}
    )
    queries = response.json().get('output', '').split('\n')
    return queries

# Function to search with generated queries using a search API wrapper
def search_with_queries(queries):
    # Use a search API wrapper (e.g., Google Custom Search API) to get search results
    # Replace 'YOUR_SEARCH_API_KEY' and 'YOUR_CX' with actual values
    search_api_key = 'AIzaSyC4ZeKKTb3Dc-XB3nlrVwm0mpMRDvvWSDE'
    cx = 'b46414dca715a4927'
    search_results = []
    for query in queries:
        params = {
            'key': search_api_key,
            'cx': cx,
            'q': query
        }
        response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
        search_results.extend(response.json().get('items', []))
    return search_results

# Function to scrape relevant content from a webpage
def scrape_content(url):
    response = requests.get(url)
    # Replace 'main' with the appropriate tag where the relevant content is wrapped
    content = response.text  # Use entire text for simplicity
    return content

# Function to convert content into knowledge points using Llama 2
def convert_to_knowledge_points_llama(content):
    response = requests.post(
        llama2_endpoint,
        json={"input": f"Condense the following content: {content}"}
    )
    knowledge_points = response.json().get('output', '')
    return knowledge_points

if __name__ == '__main__':
    # Example usage
    topic = "programming"
    
    # Step 1: Generate search queries
    queries = generate_search_queries_llama(topic)

    # Step 2: Search with generated queries
    search_results = search_with_queries(queries)

    # Step 3: Scrape relevant content
    if search_results:
        first_result_url = search_results[0].get('link')
        relevant_content = scrape_content(first_result_url)

        # Step 4: Convert relevant content into knowledge points
        knowledge_points = convert_to_knowledge_points_llama(relevant_content)

        print("Generated Search Queries:", queries)
        print("Search Results:", search_results)
        print("Relevant Content:", relevant_content)
        print("Knowledge Points:", knowledge_points)
    else:
        print("No search results found")
