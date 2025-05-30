#!/usr/bin/env python3
"""
Label Ledger PDF Generator
Creates a 4x6 inch newspaper PDF from JSON data containing headlines and summaries.
"""

import json
from reportlab.lib.pagesizes import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def create_newspaper_pdf(json_file_path, output_pdf_path):
    """
    Create a 4x6 inch newspaper PDF from JSON data.
    
    Args:
        json_file_path (str): Path to JSON file containing news data
        output_pdf_path (str): Path where PDF will be saved
    """
    
    # Define page size (4x6 inches)
    page_width = 4 * inch
    page_height = 6 * inch
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=(page_width, page_height),
        rightMargin=0.3 * inch,
        leftMargin=0.3 * inch,
        topMargin=0.3 * inch,
        bottomMargin=0.3 * inch
    )
    
    # Load JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find file {json_file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=black,
        fontName='Helvetica-Bold'
    )
    
    headline_style = ParagraphStyle(
        'CustomHeadline',
        parent=styles['Heading2'],
        fontSize=10,
        spaceAfter=6,
        spaceBefore=8,
        alignment=TA_LEFT,
        textColor=black,
        fontName='Helvetica-Bold'
    )
    
    summary_style = ParagraphStyle(
        'CustomSummary',
        parent=styles['Normal'],
        fontSize=8,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        textColor=black,
        fontName='Helvetica'
    )
    
    # Build document content
    story = []
    
    # Add main title
    title = Paragraph("Label Ledger", title_style)
    story.append(title)
    story.append(Spacer(1, 0.1 * inch))
    
    # Add news articles
    articles = news_data.get('articles', [])
    
    for i, article in enumerate(articles[:3]):  # Limit to 3 articles
        headline = article.get('headline', f'Article {i+1}')
        summary = article.get('summary', 'No summary available.')
        
        # Add headline
        headline_para = Paragraph(headline, headline_style)
        story.append(headline_para)
        
        # Add summary
        summary_para = Paragraph(summary, summary_style)
        story.append(summary_para)
        
        # Add separator except for last article
        if i < len(articles[:3]) - 1:
            story.append(Spacer(1, 0.05 * inch))
    
    # Build PDF
    try:
        doc.build(story)
        print(f"PDF successfully created: {output_pdf_path}")
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")

def create_sample_json(json_file_path):
    """
    Create a sample JSON file with news data.
    
    Args:
        json_file_path (str): Path where sample JSON will be saved
    """
    sample_data = {
        "articles": [
            {
                "headline": "Local Coffee Shop Opens New Location",
                "summary": "Main Street Coffee celebrated the grand opening of their second location downtown yesterday. The new shop features locally roasted beans and artisanal pastries from neighborhood bakeries."
            },
            {
                "headline": "City Council Approves Park Renovation",
                "summary": "The city council unanimously approved a $2.3 million renovation plan for Riverside Park. The project will include new playground equipment, walking trails, and improved lighting throughout the facility."
            },
            {
                "headline": "High School Drama Club Wins State Competition",
                "summary": "Lincoln High School's drama club took first place at the state theater competition with their production of 'Our Town'. The students will advance to the regional championship next month."
            }
        ]
    }
    
    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
        print(f"Sample JSON created: {json_file_path}")
    except Exception as e:
        print(f"Error creating sample JSON: {str(e)}")

if __name__ == "__main__":
    # File paths
    json_file = "news_data.json"
    pdf_file = "label_ledger.pdf"
    
    # Create sample JSON if it doesn't exist
    try:
        with open(json_file, 'r') as f:
            pass
    except FileNotFoundError:
        print("Creating sample JSON file...")
        create_sample_json(json_file)
    
    # Generate PDF
    print("Generating Label Ledger PDF...")
    create_newspaper_pdf(json_file, pdf_file)
    
    print("\nInstructions:")
    print("1. Edit 'news_data.json' with your headlines and summaries")
    print("2. Run this script to generate 'label_ledger.pdf'")
    print("3. The PDF is sized for 4x6 inch printing")
    
    print("\nJSON format should be:")
    print('''{
  "articles": [
    {
      "headline": "Your Headline Here",
      "summary": "Your summary text here..."
    }
  ]
}''')