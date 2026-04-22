from pathlib import Path
from config import get_settings
from pysymp_elements import APIClient

settings = get_settings()

# Initialize the client
client = APIClient(
    base_url=settings.base_url,
    username=settings.username,
    password=settings.password,
)

# Get details of a specific user
user = client.get_object('users', 767, detail='full')

# Get all relationships for the user
rel1 = client.get_relationships(object=f'user({user.id})')

# Get all the publications with full details, limiting to 3 pages of results
pubs = client.get_publications(detail = 'full', max_pages=3)

print(user.to_json())
print(rel1) # Note that rel1 is a list of Relationship objects, not a JSON string. You can convert it to JSON if needed.
print(pubs) # Note that pubs is a Python list of Publication objects, not a JSON string. You can convert it to JSON if needed.