import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL for the website
BASE_URL = "https://www.accesstoinsight.org"
INDEX_URL = f"{BASE_URL}/index-sutta.html"

# Maximum number of sutras to scrape
MAX_SUTRAS = 500

# Function to fetch sutra links from the index page
def fetch_sutra_links():
    response = requests.get(INDEX_URL)
    if response.status_code != 200:
        print("Failed to fetch the index page")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all sutra links (those starting with "tipitaka/")
    sutra_links = []
    for link in soup.select("a[href^='tipitaka/']"):  # Match href starting with 'tipitaka/'
        href = link['href']
        full_url = BASE_URL + "/" + href  # Build full URL
        sutra_links.append(full_url)
    
    print(f"Found {len(sutra_links)} sutra links.")
    return sutra_links

# Function to fetch sutra content
def fetch_sutra_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch sutra: {url}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract title and content
    title = soup.find('h1').text.strip() if soup.find('h1') else "Unknown Title"
    content = []
    for paragraph in soup.select("p"):
        content.append(paragraph.text.strip())
    
    return {"title": title, "url": url, "content": "\n".join(content)}

# Main function to orchestrate the scraping process
def main():
    # Step 1: Fetch sutra links
    sutra_links = fetch_sutra_links()
    if not sutra_links:
        print("No sutra links found. Exiting.")
        return
    
    # Step 2: Scrape content for each sutra, limited to MAX_SUTRAS
    all_sutras = []
    for index, link in enumerate(sutra_links):
        if index >= MAX_SUTRAS:  # Stop once we've reached the limit
            break
        print(f"Fetching content from: {link}")
        sutra = fetch_sutra_content(link)
        if sutra:
            all_sutras.append(sutra)
        time.sleep(1)  # Pause to avoid overwhelming the server
    
    # Step 3: Save to CSV
    if all_sutras:
        df = pd.DataFrame(all_sutras)
        df.to_csv("sutras.csv", index=False)
        print(f"Sutras saved to 'sutras.csv' ({len(all_sutras)} sutras scraped).")
    else:
        print("No sutra content scraped.")

# Run the main function
if __name__ == "__main__":
    main()
