"""
    Flask Web Application for Scraping and Parsing
    This script sets up a Flask web application that allows users to scrape a website and parse its content.
    The application provides two main endpoints:
        1. /get_links: Accepts a POST request with a website URL, scrapes the content, and returns 
                       the links found on the page.
        2. /scrape: Accepts a POST request with a website URL, scrapes the content, and returns 
                    the cleaned and split DOM content.
        3. /parse: Accepts a POST request with the scraped content and a description for parsing, 
                    and returns the parsed content using the Ollama LLM.
"""
import random
from components.crawler import get_all_links
from flask import Flask, request, jsonify, render_template
from components.parse import parse_dom_ollama, parse_links_ollama
from components.scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content


app = Flask(__name__)

@app.route('/')
def home():
    """Home page"""
    return render_template('home.html')

@app.route('/get_links', methods=['POST'])
def get_links():
    data = request.get_json()
    
    if not data or 'website' not in data:
        return jsonify({"error": "Missing website URL"}), 400
    
    try:
        links = get_all_links(data['website'])
        links = [data['website'] + link if not link.startswith('https://') else link for link in links]

        parsed_links = parse_links_ollama(links)

        return jsonify({'links': parsed_links}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/scrape', methods=['POST'])
def handle_scrape():
    """Endpoint for website scraping"""
    data = request.get_json()
    
    if not data or 'website' not in data:
        return jsonify({"error": "Missing website URL"}), 400
    
    try:
        html = scrape_website(data['website'])
        body_content = extract_body_content(html)
        cleaned_content = clean_body_content(body_content)
        chunks = split_dom_content(cleaned_content)
        
        return jsonify({
            "message": "Scraping successful",
            "chunks": chunks,
            "chunk_count": len(chunks)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/parse', methods=['POST'])
def handle_parse():
    """Endpoint for content parsing"""
    data = request.get_json()
    
    required_fields = ['chunks', 'parse_description']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields (chunks or parse_description)"}), 400
    
    try:
        parsed_content = parse_dom_ollama(data['chunks'], data['parse_description'])
        return jsonify({
            "message": "Parsing successful",
            "parsed_content": parsed_content
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run_all', methods=['GET'])
def run_all():
    url = 'https://www.si.com/mlb/giants'
    try:
        all_links = get_all_links(url)
        all_links = [url + link if not link.startswith('http') else link for link in all_links]
        parsed_links = parse_links_ollama(all_links)
        chosen_links = random.sample(parsed_links, 5)
        results = []

        for link in chosen_links:
            html = scrape_website(link)
            body_content = extract_body_content(html)
            cleaned_content = clean_body_content(body_content)
            chunks = split_dom_content(cleaned_content)
            parsed = parse_dom_ollama(chunks, "summarize the article in detail")
            results.append({"link": link, "summary": parsed})

        return jsonify({"summaries": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
