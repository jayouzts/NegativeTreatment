import sys
from utils import extract_negative_treatments

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <case_id>")
        sys.exit(1)

    case_id = sys.argv[1]
    print(f"Case ID: {case_id}")  # Debug print
    treatments = extract_negative_treatments(case_id)
    print(treatments)

if __name__ == "__main__":
    main()
