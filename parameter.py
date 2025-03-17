import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from openpyxl import Workbook
import html
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor

def find_get_params(url):
    """Extract GET parameters from the URL."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return [f"{param}: {', '.join(values)}" for param, values in query_params.items()]

def find_post_params(url):
    """Extract POST parameters by analyzing forms in the HTML content."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        params = []
        for form in soup.find_all('form'):
            inputs = form.find_all('input')
            for input_field in inputs:
                input_name = input_field.get('name')
                input_type = input_field.get('type', 'text')
                if input_name:
                    params.append(f"{input_name} ({input_type})")
        return params
    except requests.RequestException as e:
        print(f"[!] Error fetching the URL: {e}")
        return []

def analyze_url_parameters(url):
    """Analyze URL parameters for reflective, retrieving, validation, and file handling behavior."""
    try:
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        if not params:
            return "No GET parameters found in the URL."

        results = {}
        original_response = requests.get(url, timeout=10)
        original_response.raise_for_status()
        original_text = original_response.text

        for param, values in params.items():
            param_value = values[0]
            modified_value = "test_reflective"

            # Reflective Parameter Test
            reflective_url = url.replace(f"{param}={param_value}", f"{param}={modified_value}")
            reflective_response = requests.get(reflective_url, timeout=10)
            reflective_response.raise_for_status()

            if modified_value in reflective_response.text or html.escape(modified_value) in reflective_response.text:
                results[param] = "Reflective Parameter: The value is echoed back in the response."
                continue

            # Retrieving Parameter Test
            if param_value in original_text:
                results[param] = "Retrieving Parameter: Fetches data from the backend."
                continue

            # Validation Test
            invalid_value = "invalid"
            validation_url = url.replace(f"{param}={param_value}", f"{param}={invalid_value}")
            validation_response = requests.get(validation_url, timeout=10)
            validation_response.raise_for_status()

            if validation_response.status_code != original_response.status_code:
                results[param] = "Validation Parameter: Controls access or validation logic."
                continue

            # File Handling Test
            if ".php" in original_text or "file" in original_text.lower():
                results[param] = "File Handling Parameter: Handles or interacts with files."
                continue

            # Undefined Parameter Behavior
            results[param] = "Undefined: Requires deeper manual testing or special cases."

        return results
    except requests.RequestException as e:
        return f"Error analyzing URL: {e}"

def save_to_excel(data, filename="output.xlsx"):
    """Save the extracted data to an Excel file."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Parameters"

    # Write headers
    sheet.append(["URL", "Method", "Parameters", "Analysis"])

    # Write data rows
    for row in data:
        sheet.append(row)

    workbook.save(filename)
    print(f"[+] Data saved to {filename}")

def process_url(url):
    """Process and analyze a single URL."""
    print(f"\nAnalyzing URL: {url}")

    data = []

    # Process GET parameters
    get_params = find_get_params(url)
    if get_params:
        analysis_results = analyze_url_parameters(url)
        if isinstance(analysis_results, dict):
            for param, result in analysis_results.items():
                data.append([url, "GET", param, result])
        else:
            data.append([url, "GET", ", ".join(get_params), analysis_results])
    else:
        print("[!] No GET parameters found. Checking for forms...")

    # Process POST parameters (from forms)
    post_params = find_post_params(url)
    if post_params:
        for param in post_params:
            data.append([url, "POST", param, "Manual Analysis Required"])
    else:
        print("[!] No POST parameters (forms) detected.")

    # Handle case where no data is found
    if not data:
        print("[!] No parameters (GET or POST) were identified. The page might not require analysis.")
        data.append([url, "-", "-", "No parameters detected"])

    return data

def run_selenium(url):
    """Use Selenium to handle JavaScript-rendered content."""
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(3)  # Allow time for JavaScript to load content
        page_source = driver.page_source
    finally:
        driver.quit()

    return page_source

def main():
    print("Please ensure that you have the following dependencies installed before running the script:")
    print("requests, beautifulsoup4, openpyxl, selenium")
    print("You can install them using the following command in the terminal:")
    print("pip install requests beautifulsoup4 openpyxl selenium")

    print("\nChoose an option:")
    print("1. Enter a URL directly")
    print("2. Provide a file containing URLs")

    choice = input("Enter your choice (1 or 2): ").strip()

    all_data = []

    if choice == "1":
        url = input("Enter the URL: ").strip()
        if not url.startswith("http"):
            url = "http://" + url
        all_data.extend(process_url(url))
    elif choice == "2":
        file_path = input("Enter the file path: ").strip()
        try:
            with open(file_path, 'r') as file:
                urls = [url.strip() for url in file if url.strip()]
                with ThreadPoolExecutor(max_workers=5) as executor:
                    results = executor.map(process_url, urls)
                    for result in results:
                        all_data.extend(result)
        except FileNotFoundError:
            print("Error: The specified file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Invalid choice. Please restart the program and choose a valid option.")
        return

    # Save results to Excel
    if all_data:
        save_to_excel(all_data)

if __name__ == "__main__":
    main()




