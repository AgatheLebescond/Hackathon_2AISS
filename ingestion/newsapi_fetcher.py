import requests
from newspaper import Article, Config
from urllib.parse import urlparse
import nltk

def fetch_article_from_url(url: str, api_token: str = None, header_name: str = 'Authorization') -> dict:
    """
    Fetches an article from the given URL and returns its text and metadata.
    Optionally includes an API token in the request headers.

    Args:
        url (str): The article URL.
        api_token (str, optional): API token for authenticated requests.
        header_name (str): Header field name for the token (default 'Authorization').

    Returns:
        dict: {
            "text": str,           # Full text of the article
            "metadata": {
                "title": str,
                "authors": list,
                "publish_date": datetime or None,
                "top_image": str,
                "movies": list,
                "keywords": list,
                "summary": str,
                "source": str        # Domain of the article
            }
        }
    """
    nltk.download('punkt')
    nltk.download('punkt_tab')
    # Configure request headers
    config = Config()
    if api_token:
        config.request_headers = {
            header_name: f"Bearer {api_token}"
        }

    # Use newspaper3k with optional headers to extract content
    article = Article(url, config=config)
    article.download()
    article.parse()
    article.nlp()  # extract keywords and summary

    # Extract domain for metadata
    parsed = urlparse(url)
    source = parsed.netloc

    article_data = {
        "text": article.text,
        "metadata": {
            "title": article.title,
            "authors": article.authors,
            "publish_date": article.publish_date,
            "top_image": article.top_image,
            "movies": article.movies,
            "keywords": article.keywords,
            "summary": article.summary,
            "source": source
        }
    }
    return article_data

# Example usage:
# data = fetch_article_from_url(
#     "https://example.com/news/story", 
#     api_token="YOUR_API_TOKEN",
#     header_name="X-API-Key"
# )
# print(data['metadata']['title'])
# print(data['text'][:500])