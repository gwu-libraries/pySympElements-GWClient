from typing import cast
from pathlib import Path
from config import get_settings
from pysymp_elements import APIClient
from pysymp_elements.models import APIObject, Relationship, Publication, User
import csv

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
pubs = client.get_publications(detail = 'full', limit = 555)

print(user.to_json())
print(rel1) # Note that rel1 is a list of Relationship objects, not a JSON string. You can convert it to JSON if needed.
print(pubs) # Note that pubs is a Python list of Publication objects, not a JSON string. You can convert it to JSON if needed.
#for pub in pubs:
#    print(pub.type_display_name, ": ", pub.open_access_status)

pub_rels_list = client.get_related_objects(category_from = 'users', category_to = 'publications', id = 767, limit = 25, detail = 'full')

for pub_rel in pub_rels_list:
    pub = pub_rel.related[0].object
    print(pub.type, ",", pub.fields_dict.get('doi'),",", pub.fields_dict.get('open-access-status'))


for pub_rel in pub_rels_list:
    pub = pub_rel.related[0].object
    for author in pub.authors:
        print(author.last_name)
        for link in author.links:
            print("    ", link.href)

for pub in pubs:
    print(str(pub.id), ",", pub.type, ",", pub.fields_dict.get('doi'),",", pub.fields_dict.get('open-access-status'))
    
all_current_users = client.get_users(detail = 'full', limit = 2500, **{'is-current-staff': True})

user_pubs = []
for user in all_current_users:
    print("Getting publications for user: ", user.id)
    pub_rels_list = client.get_related_objects(category_from = 'users', category_to = 'publications', id = user.id, detail = 'full', **{'created-since': '2025-01-01T00:00:00Z'})
    for pub_rel in pub_rels_list:
        pub = pub_rel.related[0].object
        print(user.id, ",", pub.type, ",", pub.fields_dict.get('doi'),",", pub.fields_dict.get('open-access-status'))
        user_pub = {
            'user': user.id,
            'pub_type': pub.type,
            'doi': pub.fields_dict.get('doi'),
            'open_access_status': pub.fields_dict.get('open-access-status'),
            'online_publication_date': pub.online_publication_date.to_ymd_string() if pub.online_publication_date else None,
            'publication_date': pub.publication_date.to_ymd_string() if pub.publication_date else None}
        user_pubs.append(user_pub)

with open("user_pubs.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=user_pubs[0].keys())
    writer.writeheader()
    writer.writerows(user_pubs)
