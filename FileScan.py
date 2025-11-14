import requests
import os
import json

def get_file_scan():
    # Path to VirusTotal file scan API endpoint, then the API key and file path are set with user input
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': '9cf48fa4d97ddba0b7843b56261da3493bdb515f7d94b03d04a1fd04d00b2c8f'}
    file_path = input('Enter the path to the file to be scanned: ')
    
    # Sends the file to VirusTotal for scanning
    # If successful, the scan results are printed; if there is an error, it is printed
    # Finally, the scan results are stored in a JSON file called data.json
    try:
        with open(file_path, 'rb') as file_to_scan:
            files = {'file': (os.path.basename(file_path), file_to_scan)}
            response = requests.post(url, files=files, params=params)
        
        if response.status_code == 200:
            scan_result = response.json()
            print(scan_result)
        else:
            print('Error:', response.status_code)
    except Exception as e:
        print('An error occurred:', str(e))
        
    finally:
        output_file = 'data.json'
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
                    # Attempts to load the file; if there is an error, it initializes an empty list
        else:
            data = []
            # Creates an array if the file does not exist
        
        data.append(scan_result)
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f'Data added to {output_file} successfully.')
        # At the end of the main function, the scan results are stored in a JSON file
    