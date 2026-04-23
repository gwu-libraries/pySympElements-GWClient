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
pubs = client.get_publications(detail = 'full', limit = 55)

print(user.to_json())
print(rel1) # Note that rel1 is a list of Relationship objects, not a JSON string. You can convert it to JSON if needed.
print(pubs) # Note that pubs is a Python list of Publication objects, not a JSON string. You can convert it to JSON if needed.
#for pub in pubs:
#    print(pub.type_display_name, ": ", pub.open_access_status)

pub_rels_list = client.get_related_objects(category_from = 'users', category_to = 'publications', id = 767, limit = 25, detail = 'full')

for pub_rel in pub_rels_list:
    pub = pub_rel.related[0].object
    print(pub.fields_dict.get('open-access-status'))