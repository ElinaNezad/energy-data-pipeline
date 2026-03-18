import logging
import requests
import json


url = "https://electricitymarketservice.energinet.dk/api/v1/PublicData/dataset/mfrrRequest/latest"

def fetch_and_process_data():
    try:
      response = requests.get(url, timeout=15)
      response.raise_for_status()
    except Exception as e:
      logging.error(f"error while reaching the API:{e}")
      return[]
    
    try:
      data = response.json()
    except ValueError as e:
     logging.error(f"Value error: {e}")
     return[]
    
    if not data:
     logging.error("Data is empty")
     return[]
    

    results = []

    for record in data["mfrrRequest"]:

     timestamp = record["timeStamp"]
     mtuStart = record["mtuStart"]
     values = record["values"]

     if timestamp is None and mtuStart is None and values is None:
        logging.warning("Missing required fields in Dataset")
        continue

     for item in record["values"]:
      area = item.get("area")
      value = item.get("value")

      if area is None or value is None:
        logging.warning("Missing area or value inside values array.")
        continue
    
      results.append({
            "timeStamp": timestamp,
            "mtuStart": mtuStart,
            "area": item["area"],
            "value": item["value"]
      })

    # print (json.dumps(results,indent=2))
    print (results)
    return results

    

if __name__ == "__main__":
    fetch_and_process_data()