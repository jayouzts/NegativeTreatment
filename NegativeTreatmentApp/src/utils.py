from fetch_case import fetch_case_html
from prompt_llm import analyze_negative_treatment
from bs4 import BeautifulSoup

def extract_negative_treatments(case_id):
    """
    Fetches the case HTML and uses LLM to extract negative treatment.

    Args:
        case_id (str): Google Scholar case ID.

    Returns:
        list[dict] or str: List of negative treatments, or a string if none found or error occurs.
    """

    result = fetch_case_html(case_id)

    if not result["success"]:
        return f"Error fetching case: {result['error']}"

    soup = BeautifulSoup(result["html"], "html.parser")
    content_div = soup.find("div", {"id": "gs_opinion"})

    if not content_div:
        return "Could not find the case content in HTML."

    text = content_div.get_text(separator="\n", strip=True)

    # Call to LLM
    return analyze_negative_treatment(text)
