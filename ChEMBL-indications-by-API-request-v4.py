import requests
import json
import time

def txtfile_to_list(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
    return [line.strip() for line in data]

def fetch_page(url, max_retries, retry_delay):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise

def list_to_jsonfile(drugs_list, filename):
    # Convert drugs list to JSON string
    drugs_json = json.dumps(drugs_list, indent=4)

    # Save JSON string to a .txt file
    with open(filename, 'w') as file:
        file.write(drugs_json)

def main():
    # Terms to search for    
    list_of_study_drugs = txtfile_to_list('drug_list-v2.txt')  # Load the list of drugs from the file
    print(list_of_study_drugs)
    drug = 'aprepitant'  # Drug name to search for

    # Retry logic
    max_retries = 3
    retry_delay = 5  # seconds

    # Base URL from ChEMBL API Drug resource
    base_url = f'https://www.ebi.ac.uk/chembl/api/data/drug.json?molecule_synonyms__molecule_synonym__iexact={drug}'
    drugs_list = []

    next_url = base_url
    page_counter = 0

    while next_url:
        page_counter += 1
        print(f"Fetching page {page_counter}")
        data = fetch_page(next_url, max_retries, retry_delay)
        drugs_list.extend(data['drugs'])
        # drugs_list.extend(data['drug_indications'])
        partial_url = data['page_meta']['next']
        counts = data['page_meta']['total_count']
        print(f'Partial URL: {partial_url}, Total count: {counts}')
        next_url = f'https://www.ebi.ac.uk{partial_url}' if partial_url else None

    print(drugs_list)

    # Call the function to save the drugs list to a file
    list_to_jsonfile(drugs_list, 'ChEMBL_Drugs-v1.txt')

if __name__ == "__main__":
    main()
