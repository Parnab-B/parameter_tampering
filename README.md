# parameter_tampering
# URL Parameter Analyzer

## Overview
This script analyzes GET and POST parameters from a given URL. It helps in identifying reflective parameters, validation mechanisms, and possible security vulnerabilities. The script also supports bulk analysis of multiple URLs from a file.

## Features
- Extracts and analyzes GET parameters from URLs
- Extracts POST parameters from HTML forms
- Detects reflective, retrieving, validation, and file-handling parameters
- Saves results to an Excel file (`output.xlsx`)
- Supports bulk processing of URLs
- Uses Selenium for JavaScript-rendered content

## Prerequisites
Ensure you have the following dependencies installed before running the script:
```sh
pip install requests beautifulsoup4 openpyxl selenium
```

## Usage
### Run the Script
Execute the script using:
```sh
python parameter.py
```

### Options
1. **Analyze a Single URL**: The script prompts you to enter a URL for analysis.
2. **Analyze Multiple URLs**: Provide a file containing URLs (one per line) for bulk analysis.

### Output
- The results are stored in `output.xlsx` containing analyzed parameters and their classifications.

## Dependencies
- `requests` - To make HTTP requests
- `beautifulsoup4` - To parse HTML
- `openpyxl` - To save results in an Excel file
- `selenium` - To handle JavaScript-rendered content

## License
This project is licensed under the MIT License. Feel free to use and modify it as needed.

## Author
Parnab Bhattacharya

