import os
import json
import argparse
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


ABUSE_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "44e062c43d0bf2c2c982ecdbe2426b8a0189c584f4b06d6962116389fcebc5df5dabd7d3bdae9f25")
BASE_URL = "https://api.abuseipdb.com/api/v2/check"
REQUEST_TIMEOUT = 10


def _make_session(retries: int = 2, backoff_factor: float = 0.5) -> requests.Session:
    s = requests.Session()
    retry = Retry(total=retries, backoff_factor=backoff_factor, status_forcelist=(429, 500, 502, 503, 504))
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


def check_ip(ip: Optional[str] = None, api_key: Optional[str] = None, save_path: str = "data.json"):
    """
    Query AbuseIPDB for threat information about an IP address.

    - `ip`: the IP to check (user prompted if not provided)
    - `api_key`: override API key
    - `save_path`: file path to save results
    """

    key = api_key or ABUSE_API_KEY
    if not key or key == "YOUR_ABUSEIPDB_KEY_HERE":
        print("[Error] AbuseIPDB API key not set. Set ABUSEIPDB_API_KEY or pass --api-key.")
        return

    if not ip:
        ip = input("Enter the IP address to check: ").strip()

    if not ip:
        print("No IP entered, aborting.")
        return

    headers = {
        "Key": key,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90  # last 90 days of reports
    }

    print(f"\nQuerying AbuseIPDB for IP: {ip}")
    session = _make_session()

    try:
        resp = session.get(BASE_URL, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        data = resp.json()

        if "data" not in data:
            print("[Error] Unexpected AbuseIPDB response format:")
            print(json.dumps(data, indent=4))
            return

        print("\n=== AbuseIPDB Result ===")
        print(json.dumps(data, indent=4))

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"\nResult saved to {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"[Error] AbuseIPDB request failed: {e}")


def _cli():
    p = argparse.ArgumentParser(description="Check an IP address using AbuseIPDB.")
    p.add_argument("--ip", help="IP address to check")
    p.add_argument("--api-key", help="Override AbuseIPDB API key")
    p.add_argument("--out", "-o", default="data.json", help="Output JSON file path")
    args = p.parse_args()

    check_ip(ip=args.ip, api_key=args.api_key, save_path=args.out)


if __name__ == "__main__":
    _cli()