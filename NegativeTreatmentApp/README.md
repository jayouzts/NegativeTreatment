# Negative Treatment Analyzer

This project analyzes judicial opinions from Google Scholar to identify **negative treatment** of cited cases (e.g., reversed, distinguished, criticized). It uses OpenAI's GPT models to process and interpret legal texts, returning results in structured JSON.

---

## 🔍 Prompting Strategy

Several iterations were tested to ensure reliable LLM outputs:

- **Initial Prompting**: Requested identification of negative treatments with supporting explanations and quotes.
- **Refinement**: Added a constraint to limit consideration to cases explicitly cited in the opinion, reducing hallucination.
- **Output Format**: Modified to return structured JSON with `treated_case`, `type`, `explanation`, and `quote`.
- **Deduplication**: Ensured multiple pieces of evidence for the same case were grouped into a single object with an array of supporting passages.
- **False Positive Mitigation**: Improved instructions to prevent misclassifying supporting cases as negatively treated.

The final prompt is stored in `src/prompts/negative_treatment.txt`._

---

## ⚙️ Environment Setup

This project uses a `.env` file for API keys and configuration. You must create one before running the app:

```bash
cp .env.example .env
```

Then update the following variables:

```
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo
SCHOLAR_BASE_URL=https://scholar.google.com/scholar_case
MOCK_TEST=false
```

---

## 📦 Dependencies

Included in `requirements.txt`. To install:

```bash
pip install -r requirements.txt
```

### Package Breakdown

- **`requests`**: Used to fetch case HTML from Google Scholar.
- **`beautifulsoup4`**: Parses HTML to extract the opinion text.
- **`openai`**: Sends prompts and receives results from the LLM.
- **`python-dotenv`**: Loads API keys and config from `.env` securely.
- **`chardet`**: Helps detect and decode various encodings from Google Scholar HTML files.

---

## 🧪 Running the Application

To analyze a case by Google Scholar ID:

```bash
python src/main.py <case_id>
```

Example:

```bash
python src/main.py 8560467914430638671
```

The output will be JSON with any negative treatments found.

---

## 🧪 Testing

### Mocked Unit Tests

Mock LLM and fetch calls for fast local testing:

```bash
python run_tests.py
```

### Full Integration Tests

Set MOCK_TEST environment variable to false to disable mocking.  Then execute run_tests.py._

---

## 🚧 Known Limitations


For very large opinions (e.g., lengthy Supreme Court decisions such as Dobbs, case id 15560296770592570126 ),
the full text may exceed the token limit of the current OpenAI model and API tier.
In production, this should be handled by splitting the input into smaller sections
(e.g., paragraphs or logical blocks), analyzing each separately, and then aggregating results.
Due to time for this demonstration, long texts are not currently segmented.

Google Scholar Access Restrictions:
This application scrapes case text directly from Google Scholar using HTTP requests. 
Google Scholar actively employs bot-detection mechanisms and may temporarily block or throttle requests, 
especially if JavaScript is not enabled (as is the case with this script). 
During development, I encountered issues where access was denied due to perceived automated behavior.

To work around this:

The application includes a caching mechanism to reduce the number of requests.

Friendly error messages are returned when scraping fails.

As a fallback, users can manually download and save HTML case files into
the src/cache/ directory using the appropriate case ID as the filename.
