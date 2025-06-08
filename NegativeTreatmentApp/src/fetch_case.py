import os
import requests
import chardet
from config import SCHOLAR_BASE_URL

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def fetch_case_html(case_id: str) -> dict:
    """
    Fetch the HTML of a case from Google Scholar or cache.

    Returns:
        dict with:
        - success (bool)
        - html (str or None)
        - error (str or None)
    """
    cache_path = os.path.join(CACHE_DIR, f"{case_id}.html")

    # Check cache first to limit repeated calls to scholar
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "rb") as raw_file:
                raw_data = raw_file.read()
                detected = chardet.detect(raw_data)
                encoding = detected.get("encoding", "utf-8")

                html = raw_data.decode(encoding)
                return {"success": True, "html": html, "error": None}
        except Exception as e:
            return {"success": False, "html": None, "error": str(e)}

    url = f"{SCHOLAR_BASE_URL}?case={case_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text

        if "enable JavaScript" in html or "Sorry, we can't process your request" in html:
            return {
                "success": False,
                "html": None,
                "error": "Google Scholar blocked the request. Try again later or reduce frequency."
            }

        # Save to cache
        with open(cache_path, "w", encoding="utf-8") as file:
            file.write(html)

        return {"success": True, "html": html, "error": None}

    except requests.RequestException as e:
        return {
            "success": False,
            "html": None,
            "error": f"Error fetching case from Google Scholar: {e}"
        }
