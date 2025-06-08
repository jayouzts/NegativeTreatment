from utils import extract_negative_treatments
import unittest
import os
import re
import json

class TestNegativeTreatment(unittest.TestCase):

    def test_multiple_cases(self):
        case_ids = [
            '8560467914430638671',
            '10195889690540364307',
            '8355294677874943981',
            '4924998297704337602',
            '9445364666925364919'
        ]

        for case_id in case_ids:
            with self.subTest(case_id=case_id):
                result = extract_negative_treatments(case_id)
                self.assertIsNotNone(result, f"Test failed for case ID: {case_id}")

    def test_no_negative_treatment_case(self):
        case_id = '18130159213798259031'  # Peter K. Navarro v. United States
        #This is an in-chambers opion from the Supreme Court with no negative treatments
        result = extract_negative_treatments(case_id)

    # If result is already a dict, continue
        if isinstance(result, dict):
            self.assertIn("negative_treatments", result)
            self.assertEqual(result["negative_treatments"], [])
            return

    # If it's a string, clean and try to parse
        if isinstance(result, str):
           cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", result.strip(), flags=re.MULTILINE)

        # Handle empty or invalid JSON
           if not cleaned.strip():
               self.fail("LLM returned an empty or whitespace-only string")

           try:
               parsed = json.loads(cleaned)
           except json.JSONDecodeError as e:
               print("=== Raw LLM Output ===")
               print(result)
               print("======================")
               self.fail(f"LLM returned invalid JSON: {e}")

               self.assertIn("negative_treatments", parsed)
               self.assertEqual(parsed["negative_treatments"], [])
        else:
          self.fail(f"Unexpected result type: {type(result)}")

if __name__ == '__main__':
    unittest.main()