"""
    Flask Web Application for Scraping and Parsing
    This script sets up a Flask web application that allows users to scrape a website and parse its content.
    The application provides two main endpoints:
        1. /scrape: Accepts a POST request with a website URL, scrapes the content, and returns 
                    the cleaned and split DOM content.
        2. /parse: Accepts a POST request with the scraped content and a description for parsing, 
                    and returns the parsed content using the Ollama LLM.
"""
from components.crawler import get_all_links
from components.parse import parse_with_ollama
from flask import Flask, request, jsonify, render_template
from components.scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content

app = Flask(__name__)

@app.route('/')
def home():
    """Home page"""
    return render_template('home.html')

@app.route('/get_links', methods=['POST'])
def get_links():
    try:
        data = request.get_json()
        website = data.get('website')

        if not website:
            return jsonify({'error': 'Website URL is required'}), 400

        # Call the get_all_links function to fetch links
        links = get_all_links(website)  # Ensure this function is implemented and imported correctly

        return jsonify({'links': links}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/scrape', methods=['POST'])
def handle_scrape():
    """Endpoint for website scraping"""
    data = request.get_json()
    
    if not data or 'website' not in data:
        return jsonify({"error": "Missing website URL"}), 400
    
    try:
        # Scrape website and process content
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
        parsed_content = parse_with_ollama(data['chunks'], data['parse_description'])
        return jsonify({
            "message": "Parsing successful",
            "parsed_content": parsed_content
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
