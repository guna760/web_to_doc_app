import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_website_content(url):
    try:
        # Standard web headers to mimic a normal browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        # Download the webpage data directly over HTTP/HTTPS
        response = requests.get(url, headers=headers, timeout=15)
        
        # Check if the website blocked the request (e.g., 403 Forbidden or 404 Not Found)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Strip out unwanted structural components
        for script in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            script.extract()
            
        title = soup.title.string.strip() if soup.title else "Scraped Website Content"
        structured_elements = []
        
        # Read text headers, paragraphs, and images sequentially
        for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'img']):
            if element.name == 'img':
                img_url = element.get('src')
                if img_url:
                    full_img_url = urljoin(url, img_url)
                    if not any(x in full_img_url.lower() for x in ['logo', 'icon', 'avatar', 'sprite', 'banner']):
                        structured_elements.append({"type": "image", "value": full_img_url})
            else:
                text = element.get_text().strip()
                if text and len(text) > 3:
                    structured_elements.append({"type": "text", "value": text})
        
        # Fallback if the page parsed absolutely nothing
        if not structured_elements:
            return {"error": "The website loaded, but no readable paragraphs or headings were found. It might be protected or completely built on client-side Javascript."}
            
        return {"title": title, "content": structured_elements}
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Network Error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected System Error: {str(e)}"}