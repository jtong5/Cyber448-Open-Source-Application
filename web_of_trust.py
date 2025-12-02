import requests
API_USER_ID = "YOUR_USER_ID_HERE"
API_KEY = 'hjuz2i_4abb80754abb80754abb80754abb8075'
BASE_URL = "https://scorecard.api.mywot.com/v3/targets"
REQUEST_TIMEOUT = 10


def get_wot_project(domain):
    """
    Uses the Web of Trust Map API to:
    1. Search for a project by keyword.
    2. Fetch detailed info about the first matching project.
    3. Print key details and save the full JSON to data.json.
    """

    # ----- Step 1: Search for projects -----
    url = f"{BASE_URL}/{domain}"

    headers = {
        "x-user-id": API_USER_ID,
        "x-api-key": API_KEY,
    }

    try:
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()  # Raise on 404, 401, 403, etc.
        return resp.json()

    except requests.exceptions.HTTPError as e:
        return {
            "error": f"HTTP error: {e}",
            "url": resp.request.url,
            "status_code": resp.status_code,
            "response_text": resp.text
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}

    except ValueError:
        return {"error": "Invalid JSON returned by API"}