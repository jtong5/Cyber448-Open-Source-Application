import requests
import json

API_KEY = 'hjuz2i_4abb80754abb80754abb80754abb8075'

BASE_URL = "https://www.weboftrust.org/api/v1"
REQUEST_TIMEOUT = 10


def get_wot_project():
    """
    Uses the Web of Trust Map API to:
    1. Search for a project by keyword.
    2. Fetch detailed info about the first matching project.
    3. Print key details and save the full JSON to data.json.
    """

    # Ask user what to search for (like 'ethereum', 'TradeTrust', etc.)
    # ******* Currently, this can pull information from companies. Not URLS. *********
    search_term = input("Enter a search term for a DID project (e.g. 'ethereum'): ")

    headers = {
        "X-API-Key": API_KEY
    }

    # ----- Step 1: Search for projects -----
    search_url = f"{BASE_URL}/search"
    search_params = {"query": search_term}

    try:
        print(f"Searching: {search_url}?query={search_term}")
        search_resp = requests.get(search_url, headers=headers, params=search_params, timeout=REQUEST_TIMEOUT)
        search_resp.raise_for_status()
        search_data = search_resp.json()
    except requests.exceptions.RequestException as e:
        print(f"[Error] Search request failed: {e}")
        return
    except ValueError as e:
        print(f"[Error] Failed to decode search JSON: {e}")
        return

    # The API can return either a dict with a "data" key or a raw list of results.
    if isinstance(search_data, dict):
        # prefer 'data', fall back to 'results' if present
        results = search_data.get("data") or search_data.get("results") or []
    elif isinstance(search_data, list):
        results = search_data
    else:
        results = []

    if not results:
        print("No projects found for that search term.")
        return

    # For simplicity, just pick the first result
    project_result = results[0]
    raw_id = project_result.get("id", "")

    # In the docs, IDs look like 'project-118', and they strip 'project-'
    if raw_id.startswith("project-"):
        project_id = raw_id.replace("project-", "")
    else:
        project_id = raw_id

    print("\n=== Search Result Chosen ===")
    print(f"Title: {project_result.get('title')}")
    print(f"Type:  {project_result.get('type')}")
    print(f"Raw ID: {raw_id}  -> Using ID: {project_id}")

    # ----- Step 2: Get detailed project info -----
    project_url = f"{BASE_URL}/projects/{project_id}"

    try:
        print(f"Fetching project details: {project_url}")
        project_resp = requests.get(project_url, headers=headers, timeout=REQUEST_TIMEOUT)
        project_resp.raise_for_status()
        project = project_resp.json()
    except Exception as e:
        print(f"[Error] Project details request failed: {e}")
        return

    # ----- Step 3: Print some nice details -----
    print("\n=== Web of Trust Project Details ===")
    print(f"Title:   {project.get('title')}")
    print(f"Type:    {project.get('type')}")
    print(f"Status:  {project.get('status')}")
    print(f"Country: {project.get('country_code')}")
    print(f"Website: {project.get('website')}")

    stats = project.get("stats", {})
    if stats:
        print("\n--- Stats ---")
        print(f"Total links / relationships: {stats.get('total_links')}")
        print(f"Network score: {stats.get('score')}")

    # ----- Step 4: Save full JSON response -----
    result_to_save = {
        "search_term": search_term,
        "chosen_project_id": project_id,
        "project": project,
    }

    with open("data.json", "w") as f:
        try:
            json.dump(result_to_save, f, indent=4)
        except TypeError:
            # Some objects may not be JSON serializable; attempt to stringify
            json.dump({'project': str(project)}, f, indent=4)

    print("\nFull project data saved to data.json\n")


# Optional: quick manual test
if __name__ == "__main__":
    get_wot_project()

def get_wot_for_query(search_term):

    headers = {"X-API-Key": API_KEY}

    search_url = f"{BASE_URL}/search"
    search_params = {"query": search_term}

    try:
        search_resp = requests.get(search_url, headers=headers, params=search_params, timeout=REQUEST_TIMEOUT)
        search_resp.raise_for_status()
        search_data = search_resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Search request failed: {e}"}
    except ValueError as e:
        return {"error": f"Failed to decode search JSON: {e}"}

    if isinstance(search_data, dict):
        results = search_data.get("data") or search_data.get("results") or []
    elif isinstance(search_data, list):
        results = search_data
    else:
        results = []

    if not results:
        return {"error": "No projects found for that search term."}

    project_result = results[0]
    raw_id = project_result.get("id", "")

    if raw_id.startswith("project-"):
        project_id = raw_id.replace("project-", "")
    else:
        project_id = raw_id

    project_url = f"{BASE_URL}/projects/{project_id}"
    try:
        project_resp = requests.get(project_url, headers=headers, timeout=REQUEST_TIMEOUT)
        project_resp.raise_for_status()
        project = project_resp.json()
    except Exception as e:
        return {"error": f"Project details request failed: {e}"}

    result_to_return = {
        "search_term": search_term,
        "chosen_project_id": project_id,
        "project": project,
    }

    return result_to_return
