import json
import os
from pathlib import Path

from azure.identity import DefaultAzureCredential
import requests

from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["AZURE_SEARCH_ENDPOINT"].rstrip("/")
credential = DefaultAzureCredential()
token = credential.get_token("https://search.azure.com/.default")

headers = {"Authorization": f"Bearer {token.token}"}
params = {"api-version": os.getenv("AZURE_SEARCH_API_VERSION", "2025-09-01")}
base = Path("config/azure_search")

for resource in ["datasources", "indexes", "indexers", "skillsets"]:
    response = requests.get(
        f"{endpoint}/{resource}",
        headers=headers,
        params=params,
        timeout=30,
    )
    response.raise_for_status()

    for item in response.json()["value"]:
        name = item["name"]

        response = requests.get(
            f"{endpoint}/{resource}/{name}",
            headers=headers,
            params=params,
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()
        data.pop("@odata.etag", None)

        path = base / resource / f"{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n")

        print(f"✓ {path}")