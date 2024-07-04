####
# ffunction will return pages modified in the last x days with details like page ID, page name, and content of the modification.
####
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

# Replace these with your actual values
domain = 'your-domain.atlassian.net'
username = 'your-email@example.com'
api_token = 'your-api-token'

def get_last_modified_pages_in_last_x_days(x):
    # Calculate the date x days ago
    x_days_ago = (datetime.now() - timedelta(days=x)).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Construct the URL for the CQL search
    url = f'https://{domain}/wiki/rest/api/content/search'
    cql = f'lastModified > "{x_days_ago}"'
    # title ~ "\"SSA Arret\"" # Find content where the title contains the exact phrase "SSA Arret"
    # text ~ Confluence # find content that contains the word Confluence 
    # Search for content of a particular type (page, blog..)
    # type IN (blogpost, page) # Find blogposts or pages
    # type = attachemnts # Find attachments
    # lastModified >= now("-2w")
    # space = DEV # Find content in DEV space
    # created >= now("-4w")
    # label = "performance" 
    # type = "blogpost"


    params = {
        'cql': cql,
        'expand': 'history,body.storage'
    }
    
    # Make the GET request
    response = requests.get(url, params=params, auth=HTTPBasicAuth(username, api_token))
    
    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        modified_pages = []
        for result in results['results']:
            page_id = result['id']
            title = result['title']
            last_modified = result['history']['lastUpdated']['when']
            content = result['body']['storage']['value']
            modified_pages.append({
                'page_id': page_id,
                'title': title,
                'last_modified': last_modified,
                'content': content
            })
        return modified_pages
    else:
        print(f'Failed to fetch data: {response.status_code}')
        return None

# Example usage
pages = get_last_modified_pages_in_last_x_days(7)
for page in pages:
    print(page)
####



####
# function checks if modifications in the pages occur in sections or subsections containing the string "Arret et Relance" and returns the page, the name of the section, and the content of the modification.
####

from bs4 import BeautifulSoup

def check_modification_in_specific_section(pages):
    modified_sections = []
    for page in pages:
        soup = BeautifulSoup(page['content'], 'html.parser')
        sections = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        for section in sections:
            if "Arret" in section.text and "Relance" in section.text:
                # Assuming the section's content is within the next sibling elements
                content_before = section.find_previous_sibling()
                content_after = section.find_next_sibling()
                modified_sections.append({
                    'page_id': page['page_id'],
                    'page_title': page['title'],
                    'section_title': section.text,
                    'last_modified': page['last_modified'],
                    'content_before': str(content_before),
                    'content_after': str(content_after)
                })
    return modified_sections

# Example usage
modified_sections = check_modification_in_specific_section(pages)
for section in modified_sections:
    print(section)


