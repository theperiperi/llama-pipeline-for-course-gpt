import time
import requests
import asyncio
import aiohttp

MAX_RETRIES = 3
LLAMA2_ENDPOINT = 'https://www.llama2.ai/api'  # Enter llama2 endpoint here

class LlamaInteraction:
    @staticmethod
    async def async_make_retried_generator(input_text):
        payload = {
            "input": input_text
        }
        async with aiohttp.ClientSession() as session:
            for i in range(MAX_RETRIES):
                try:
                    async with session.post(LLAMA2_ENDPOINT, json=payload) as response:
                        response.raise_for_status()  # Raise an error for bad responses
                        output_text = await response.json()
                        yield output_text.get('output', '')
                        break
                except aiohttp.ClientError as e:
                    LlamaInteraction._handle_request_exception(e, i)

    @staticmethod
    def _handle_request_exception(e, retries):
        if retries == MAX_RETRIES - 1:
            raise e
        time.sleep(1)

# Function to search with generated queries using a search API wrapper
def search_with_queries(queries):
    # Replace 'YOUR_SEARCH_API_KEY' and 'YOUR_CX' with actual values for the Google Custom Search API
    search_api_key = 'AIzaSyC4ZeKKTb3Dc-XB3nlrVwm0mpMRDvvWSDE'
    cx = 'b46414dca715a4927'
    search_results = []
    for query in queries:
        params = {
            'key': search_api_key,
            'cx': cx,
            'q': query
        }
        try:
            response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
            response.raise_for_status()  # Raise an error for bad responses
            search_results.extend(response.json().get('items', []))
        except requests.exceptions.RequestException as e:
            print(f"Error in search request: {e}")

    return search_results

# Function to scrape relevant content from a webpage
def scrape_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        # Assume the relevant content is wrapped inside the main tag
        content = response.text
        return content
    except requests.exceptions.RequestException as e:
        print(f"Error in content scraping: {e}")
        return None

if __name__ == '__main__':
    # Example usage
    topic = "programming"
    
    # Step 1: Generate search queries using Llama 2
    input_text = f"Generate search queries to find articles about {topic}"
    llama_queries = list(LlamaInteraction.async_make_retried_generator(input_text))

    # Step 2: Search with generated queries
    search_results = search_with_queries(llama_queries)

    # Step 3: Scrape relevant content
    if search_results:
        first_result_url = search_results[0].get('link')
        relevant_content = scrape_content(first_result_url)

        # Step 4: Convert relevant content into knowledge points using Llama 2
        if relevant_content:
            # Pass relevant content through Llama 2 for condensation
            input_text = f"Condense the following content: {relevant_content}"
            llama_knowledge_points = list(LlamaInteraction.async_make_retried_generator(input_text))
            print("Generated Llama Knowledge Points:")
            for point in llama_knowledge_points:
                print(point)
        else:
            print("No relevant content found")
    else:
        print("No search results found")
