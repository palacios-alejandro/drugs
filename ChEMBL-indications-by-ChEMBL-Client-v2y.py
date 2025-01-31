from chembl_webresource_client.new_client import new_client
import pandas as pd
import json
import time
from chembl_webresource_client.http_errors import HttpApplicationError

available_resources = [resource for resource in dir(new_client) if not resource.startswith('_')]
print(available_resources)

druglist = 'betamethasone'

# Retry logic
max_retries = 3
retry_delay = 5  # seconds

for attempt in range(max_retries):
    try:
        indications = new_client.drug_indication.filter(pref_name__iexact=druglist).only('id', 'chembl_id', 'drugind_id', 'drugind_type')
        indications_list = list(indications)
        break
    except HttpApplicationError as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
        else:
            raise

print(indications_list)

# Convert indications list to JSON string
indications_json = json.dumps(indications_list, indent=4)

# Save JSON string to a .txt file
with open('indications-v2.txt', 'w') as file:
    file.write(indications_json)

