from onshape_client.client import Client
import valispace
import json
import yaml


# Sample of configuration from Onshape Developer Portal:
# my_configuration = {
#                     "base_url": "https://cad.onshape.com",
#                     "access_key": "access_key",
#                     "secret_key": "secret_key"
#                     }


with open('config.yaml') as f:
    # for Onshape
    data = yaml.load(f, Loader=yaml.FullLoader)
    my_configuration = data["my_configuration"]

    # for Valispace
    url = data["url"]
    project_name = data["project_name"]
    username = data["username"]
    password = data["password"]


# Get parts from Onshape project
onshape_client = Client(configuration=my_configuration)

# /api/parts/d/cf9ae4af8d5dd69e0be8390a/w/d6cf21a6b4d1850415a83496?withThumbnails=false&includeFlatParts=false&includePropertyDefaults=false
data = onshape_client.parts_api

did = "cf9ae4af8d5dd69e0be8390a"
wvm = "w"
wvmid = "d6cf21a6b4d1850415a83496"

parts_data = data.get_parts_wmv(did=did,
                                wvm=wvm,
                                wvmid=wvmid)

name_list = []
for element in parts_data:
    name_list.append(element["name"])

print(name_list)


# Put to Valispace
valispace_api = valispace.API(url=url, username=username, password=password)
project_comps = valispace_api.get_component_list(
    project_name=project_name)

for v in project_comps:
    if v["name"] == "Motorcycle":
        print(v)
    motorcycle = v

    if v["name"] == "Light":
        print(v)


# -- put component
valispace_api.post_data(type='component', data="""{
                                                    "name": "Light",
                                                    "description": "Test python API",
                                                    "parent": null,
                                                    "project": 56,
                                                    "tags": []
                                                    }"""
                        )

light = valispace_api.get_component_by_name(unique_name='Light', project_name=project_name)
light_id = light["id"]

for name in name_list:
    name = name.replace(" ", '_')
    data_post = {
            "name": str(name),
            "description": "Test python API",
            "parent": light_id,
            "project": v["project"],
            "tags": []
            }

    data_post_json = json.dumps(data_post)

    valispace_api.post_data(type='component', data=data_post_json)
