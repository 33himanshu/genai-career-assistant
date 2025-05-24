import requests
import json

# Define the API endpoint
url = "http://localhost:8000/api/job/search"

# Define the query
query = "search job in swe in noida"

# Make the API request
response = requests.post(
    url,
    json={"query": query}
)

# Print the response
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("\nJob Search Results:")
    print(f"Content: {result['content'][:500]}...")  # Show first 500 chars
    print(f"File saved at: {result['file_path']}")
else:
    print(f"Error: {response.text}")