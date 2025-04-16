import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os


class SQLInjectionManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        self.results_file = "injection_results.txt" #this can be changed depending on where results go

    #this scans the webpage to look for fillable forms
    def get_forms(self, url):
        soup = BeautifulSoup(self.session.get(url).content, "html.parser")
        return soup.find_all("form")

    #extracts details from forms
    def form_details(self, form):
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

    #this checks for common responses in vulnerable forms
    def is_vulnerable(self, response):
        errors = {
            "quoted string not properly terminated",
            "unclosed quotation mark after the character string",
            "you have an error in your sql syntax"
        }
        for error in errors:
            if error in response.content.decode(errors="ignore").lower():
                return True
        return False

    #this injects the payload
    def scan(self, url, payload):
        results = []
        forms = self.get_forms(url)
        print(f"[+] Detected {len(forms)} forms on {url}.\n")

        for form in forms:
            details = self.form_details(form)
            data = {}

            #this is where the injection command is carried out
            for input_tag in details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    data[input_tag["name"]] = input_tag["value"] + payload
                elif input_tag["type"] != "submit":
                    data[input_tag["name"]] = f"test{payload}"

            full_url = urljoin(url, details["action"])
            print(f"[*] Submitting payload to: {full_url}")
            print(f"[*] Method: {details['method'].upper()}")

            #this sends the payload via protocal
            if details["method"].lower() == "post":
                res = self.session.post(full_url, data=data)
            else:
                res = self.session.get(full_url, params=data)

            vulnerable = self.is_vulnerable(res)
            response_snippet = res.text[:1000]  # reduced for readability at least for now

            #result record that can be used by logger
            result = {
                "url": full_url,
                "method": details["method"].upper(),
                "vulnerable": vulnerable,
                "response_preview": response_snippet,
                "payload": payload
            }

            results.append(result)
            self.save_result(result)
            self.process_response(result)

        return results

    #this summerizes the results 
    def process_response(self, result):
        print("\n--- Response Summary ---")
        print(f"URL: {result['url']}")
        print(f"Method: {result['method']}")
        print(f"Payload: {result['payload']}")
        print(f"Vulnerability Detected: {'YES' if result['vulnerable'] else 'NO'}\n")

    #saves to text file, can be used to save to something else
    def save_result(self, result):
        with open(self.results_file, "a", encoding="utf-8") as f:
            f.write(f"{result['url']} | {result['method']} | Payload: {result['payload']} | Vulnerable: {result['vulnerable']}\n")

    #this resets the result file as outlined in the SRS, specifically SRS 3.2.2.15.10
    def reset_service(self):
        if os.path.exists(self.results_file):
            os.remove(self.results_file)
            print("[*] Results file cleared.")
        else:
            print("[*] No results file to clear.")


if __name__ == "__main__":
    manager = SQLInjectionManager()

    while True:
        print("\n--- SQL Injection Manager ---")
        print("1. Scan a URL")
        print("2. Reset Service (clear results)")
        print("3. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            url = input("Enter target URL: ").strip()
            payload = input("Enter your SQL injection payload: ").strip()
            manager.scan(url, payload)
        elif choice == "2":
            manager.reset_service()
        elif choice == "3":
            print("Exiting.")
            break
        else:
            print("Invalid option. Try again.")
