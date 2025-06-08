import unittest
import os
import sys
from dotenv import load_dotenv
load_dotenv()

def run_tests_from_folder(folder):
    """Discover and run all tests in a given folder."""
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=folder, pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result

def main():
    # Default to mocked (unit) tests unless explicitly set otherwise
    run_mock_tests = os.getenv("MOCK_TEST", "true").lower() != "false"

    SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
    if SRC_DIR not in sys.path:
       sys.path.insert(0, SRC_DIR)

    if run_mock_tests:
        print("Running mocked unit tests...")
        run_tests_from_folder("tests/unit")
    else:
        print("Running full integration tests...")
        run_tests_from_folder("tests/integration")

if __name__ == '__main__':
    main()
