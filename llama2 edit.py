import time
import requests
import asyncio
import aiohttp

# TODO: Handle exceptions

MAX_RETRIES = 3 

class LlamaChat():
    def __init__(self):
        pass

    def create(self, messages: list[dict], stream: bool = False, async_mode: bool = False, temprature: float = 0.75, topP: float = 0.9, max_tokens: int = 4096):
        if async_mode and stream:
            return self.async_make_retried_generator(messages, temprature, topP, max_tokens)
        elif async_mode:
            return self.async_get_full_response(messages, temprature, topP, max_tokens)
        if stream:
            return self.sync_make_retried_generator(messages, temprature, topP, max_tokens)
        return self.sync_get_full_response(messages, temprature, topP, max_tokens)

    @staticmethod
    def sync_make_retried_generator(messages, temprature: float, topP: float, max_tokens: int):
        payload = {
            "prompt": messages[-1]['content'] if messages[-1]['role'] == 'user' else "",
            "systemPrompt": messages[0]['content'] if messages[0]['role'] == 'system' else "", 
            "version": "f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
            "temperature": temprature,
            "topP": topP,
            "maxTokens": max_tokens,
            "image": None,
            "audio": None
        }
        for i in range(MAX_RETRIES):
            try:
                res = requests.post("https://www.llama2.ai/api", json=payload, stream=True)
                for chunk in res.iter_content(chunk_size=1024):
                    yield chunk.decode('utf-8')
                break
            except Exception as e:
                if i == MAX_RETRIES - 1:
                    raise e
                time.sleep(1)

    @staticmethod
    async def async_make_retried_generator(messages, temprature: float, topP: float, max_tokens: int):
        payload = {
            "prompt": messages[-1]['content'] if messages[-1]['role'] == 'user' else "",
            "systemPrompt": messages[0]['content'] if messages[0]['role'] == 'system' else "", 
            "version": "f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
            "temperature": temprature,
            "topP": topP,
            "maxTokens": max_tokens,
            "image": None,
            "audio": None
        }
        async with aiohttp.ClientSession() as session:
            for i in range(MAX_RETRIES):
                try:
                    async with session.post("https://www.llama2.ai/api", json=payload) as res:
                        async for chunk in res.content.iter_chunked(1024):
                            yield chunk.decode('utf-8')
                        break
                except Exception as e:
                    if i == MAX_RETRIES - 1:
                        raise e
                    await asyncio.sleep(1)

    @staticmethod
    def sync_get_full_response(messages, temprature: float, topP: float, max_tokens: int):
        response_data = ''
        for chunk in LlamaChat.sync_make_retried_generator(messages, temprature, topP, max_tokens):
            response_data += chunk
        return response_data

    @staticmethod
    async def async_get_full_response(messages, temprature: float, topP: float, max_tokens: int):
        response_data = ''
        async for chunk in LlamaChat.async_make_retried_generator(messages, temprature, topP, max_tokens):
            response_data += chunk
        return response_data
    

    
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
