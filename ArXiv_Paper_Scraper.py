import feedparser
import requests
from urllib.parse import quote
from datetime import datetime

# Function to search ArXiv
def search_arxiv(keyword, max_results=100):
    keyword = quote(keyword)
    url = f"http://export.arxiv.org/api/query?search_query=all:{keyword}&start=0&max_results={max_results}"
    feed = feedparser.parse(url)
    papers = []
    
    for entry in feed.entries:
        # Extract the publication year from the published date
        pub_date = entry.published
        pub_year = datetime.strptime(pub_date, '%Y-%m-%dT%H:%M:%SZ').year

        paper_info = {
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary,
            "authors": ', '.join(author.name for author in entry.authors),
            "year": pub_year,
            "pdf_url": entry.link.replace("abs", "pdf") + ".pdf"  # Convert abstract URL to PDF URL
        }
        papers.append(paper_info)
        
    return papers

def get_user_input():
    keyword = input("Enter the keyword(s) for your search: ")
    try:
        max_results = int(input("Enter the maximum number of results: "))
    except ValueError:
        print("Invalid input for maximum results. Using default of 100.")
        max_results = 100
    return keyword, max_results

# Function to write to a file and ask for download
def write_and_download_option(filename, papers, keyword):
    with open(filename, 'w') as f:
        f.write(f"New papers on ArXiv related to {keyword}:\n\n")
        for paper in papers:
            # Write details to file
            f.write(f"Title: {paper['title']}\n")
            f.write(f"Authors: {paper['authors']}\n")
            f.write(f"Year: {paper['year']}\n")
            f.write(f"Link: {paper['link']}\n")
            f.write(f"Summary: {paper['summary']}\n")
            f.write("\n---\n\n")
            
            # Display title, authors, year, and summary to the user in a friendly format
            print(f"\033[94m\033[1mTitle:\033[0m {paper['title']}")  # Blue for title
            print(f"\033[92m\033[1mAuthors:\033[0m {paper['authors']}")  # Green for authors
            print(f"\033[93m\033[1mYear:\033[0m {paper['year']}\n")  # Yellow for year
            print(f"\033[95m\033[1mSummary:\033[0m {paper['summary']}\n")  # Magenta for summary
            
            # Ask the user if they want to download the paper
            choice = input("Do you want to download this paper? (y/n): ")
            if choice.lower() == 'y':
                download_paper(paper['pdf_url'], paper['title'])
            print("----------------------------------------------------\n\n")  # Magenta for summary	    	

# Function to download paper
def download_paper(pdf_url, title):
    response = requests.get(pdf_url)
    with open(f"{title[:50]}.pdf", 'wb') as f:  # Use the first 50 characters of the title as the filename
        f.write(response.content)

# Main part of the script
if __name__ == "__main__":
    print("\033[96m\033[1mCreated by Mohamad Issam Sayyaf \n issamsayyaf97@gmail.com \033[0m")  # Cyan for name
    print("----------------------------\n")
    keyword, max_results = get_user_input()
    filename = "new_papers.txt"
    current_year = datetime.now().year

    papers = search_arxiv(keyword, max_results)
    recent_papers = [paper for paper in papers if paper['year'] >= (current_year - 3)]

    if recent_papers:
        write_and_download_option(filename, recent_papers, keyword)
        print(f"\nSaved new papers to {filename}")
    else:
        print("No new papers found.")

