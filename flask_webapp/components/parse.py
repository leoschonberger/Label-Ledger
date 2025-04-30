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
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.1")

template_links = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
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
    count = min(150, len(links))
    parsed_links = []
    print(f"Parsing links...")
    
    prompt = ChatPromptTemplate.from_template(template_links)
    chain = prompt | model

    for i, link in enumerate(links[:count], start=1):
        response = chain.invoke({
            "dom_content": link,
            "parse_description": "Determine if this link is a valid article. Return 'Valid' or 'Invalid' only."
        })
        print(f"Parsed link: {i} of {count}")
        if response.strip() == "Valid":
            parsed_links.append(link)

    parsed_links = list(dict.fromkeys(parsed_links))

    return parsed_links

def parse_dom_ollama(dom_chunks, parse_description):
    parsed_results = []
    print(f"Parsing DOM content: {len(dom_chunks)}...")
    
    prompt = ChatPromptTemplate.from_template(template_dom)
    chain = prompt | model

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({
            'dom_content': chunk,
            'parse_description': parse_description
        })
        
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)
    
    return '\n '.join(parsed_results)
