import requests
import json
import os

def get_phone_number():
    # Keep CLI helper but reuse get_phone_info
    phone = input('Enter phone number: ')
    CC = input('Enter default country code (optional): ')
    result = get_phone_info(phone, CC)
    print(result)
    return result


def get_phone_info(phone: str, CC: str = ''):
    """Query Veriphone API for a phone number and save result to `data.json`.

    Returns the parsed JSON response (or an error dict).
    """
    file_path = 'data.json'
    url = f'https://api.veriphone.io/v2/verify?phone={phone}&country_code={CC}&key=DD0982B23C8641CC97CEF6682591574C'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            posts = response.json()
        else:
            posts = {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        posts = {"error": str(e)}

    # Persist result to data.json
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []
        data.append(posts)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception:
        # If saving fails, don't crash the caller; just continue
        pass

    return posts
        
            
            