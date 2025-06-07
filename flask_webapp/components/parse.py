"""
    This script is used to parse the content of a webpage using the Ollama LLM.
    It extracts specific information from the DOM content based on a provided description.
    The script uses the Langchain library to create a prompt template and chain it with the Ollama model.
    The parsing process is done in batches, and the results are collected and returned as a single string.

    Need to have ollama downloaded and running https://ollama.com/download
    Download a model in command line: 'ollama pull llama3.2' https://github.com/ollama/ollama
    Welcome to use other models or OpenAI but this is free *teehee*
    Possible tutorial https://python.langchain.com/docs/integrations/llms/openai/
"""
import concurrent.futures
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.1:8b")

template_links = (
    "You are an expert in identifying high-quality article links. Your task is to analyze the following HTML or link snippet and determine whether it points to a top news or feature article:\n\n"
    "{link}\n\n"
    "Follow these instructions exactly:\n\n"
    "1. **Strict Output:** Respond only with 'Valid' if the link meets the criteria above, otherwise respond with 'Invalid'.\n"
    "2. **No Extra Output:** Do not include any explanation, reasoning, or formatting—only return 'Valid' or 'Invalid'.\n"
    "3. **Extract Only Top Article URLs:** The link should lead to a prominently featured news or in-depth article, typically found in main headlines, hero sections, or labeled as 'Top Stories', 'Featured', or similar.\n"
    "4. **No Side or Sponsored Content:** Exclude any links to sidebars, sponsored articles, advertisements, newsletter signups, navigation pages, author bios, or category/tag listings.\n"
    "5. **Exclude Social Media Links:** Ignore links to platforms like Facebook, Twitter, Instagram, YouTube, etc. Also exclude pure video, podcast, or PDF links unless they are clearly a feature article.\n"
    "6. **No Multimedia or Download Links:** Exclude links that point to videos, PDFs, podcasts, or other media types unless they clearly represent a feature article.\n"
    "7. **Only Direct URLs:** Return only the extracted URLs—one per line—with no accompanying text, titles, or descriptions.\n"
    "8. **No Match Means Empty String:** If no appropriate article URLs are found, return an empty string ('').\n"
    "9. **Absolute URLs Preferred:** If both relative and absolute URLs are present, prefer absolute URLs. If only relative URLs are available, include them as-is.\n"
    "10. **Avoid Duplicates:** Do not include duplicate links.\n"
)

template_dom = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    "5. **Exclude Social Media Links:** Ignore any links referencing platforms such as Facebook, Twitter, Instagram, TikTok, or similar. Treat them as if they do not exist. "
    "6. **Ignore Non-Article Links:** If the link does not lead to an article, ignore it. "
)

def parse_links_ollama(links):
    print(f"Parsing links...")
    prompt = ChatPromptTemplate.from_template(template_links)
    chain = prompt | model

    def process_link(link):
        response = chain.invoke({"link": link})
        return link if response.strip() == "Valid" else None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_link, links))

    parsed_links = [link for link in results if link is not None]

    return parsed_links

def parse_dom_ollama(dom_chunks, parse_description):
    print("Parsing DOM content...")
    prompt = ChatPromptTemplate.from_template(template_dom)
    chain = prompt | model

    def process_chunk(chunk):
        response = chain.invoke({
            'dom_content': chunk,
            'parse_description': parse_description
        })
        return response

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_chunk, dom_chunks))

    return '\n '.join(results)
