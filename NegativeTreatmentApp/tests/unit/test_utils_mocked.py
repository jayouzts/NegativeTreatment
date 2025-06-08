import unittest
from unittest.mock import patch
from src.utils import extract_negative_treatments

class TestNegativeTreatmentMocked(unittest.TestCase):

    @patch('src.utils.analyze_negative_treatment')
    @patch('src.utils.fetch_case_html')
    def test_mocked_response(self, mock_fetch, mock_analyze):
        mock_fetch.return_value = {
            "success": True,
            "html": "<div id='gs_opinion'>We hereby overrule MockCase due to changed legal standards.</div>",
            "error": None
        }

        mock_analyze.return_value = [
            {
                "treated_case": "MockCase v. State, 123 A.2d 456 (2020)",
                "evidence": [
                    {
                        "type": "overruled",
                        "explanation": "Court explicitly stated the precedent no longer applies.",
                        "quote": "We hereby overrule MockCase due to changed legal standards."
                    }
                ]
            }
        ]

        case_id = "mock_case_id"
        result = extract_negative_treatments(case_id)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["treated_case"], "MockCase v. State, 123 A.2d 456 (2020)")

    @patch('src.utils.analyze_negative_treatment')
    @patch('src.utils.fetch_case_html')
    def test_mocked_no_treatment_response(self, mock_fetch, mock_analyze):
        mock_fetch.return_value = {
            "success": True,
            "html": "<div id='gs_opinion'>This case contains no negative treatment of prior rulings.</div>",
            "error": None
        }

        mock_analyze.return_value = "I found no negative treatments"

        case_id = "mock_case_id_no_negatives"
        result = extract_negative_treatments(case_id)

        self.assertEqual(result, "I found no negative treatments")
