import requests

url = "https://bo-api.drivewealth.io/back-office/managed/portfolios"

payload = {
    "userID": "66304da9-3h6f-2234-935f-ac6b7933d706",
    "name": "Recession Proof",
    "clientPortfolioID": "AAABBB-1222-3344.123456789",
    "description": "Mix of sectors",
    "holdings": [
        {
            "type": "FUND",
            "id": "fund_3d9d00d1-f06e-4f86-9cbf-893c75cf77fe",
            "target": 0.95
        }
    ],
    "triggers": [
        {
            "type": "TOTAL_DRIFT",
            "maxAllowed": 0.05,
            "child": None,
            "lowerBound": 0.01,
            "upperBound": 0.02
        }
    ]
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)