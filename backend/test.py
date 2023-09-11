URL_GEOSERVER: str = 'https://mapservice.gishub.vn/geoserver'
username_geoserver = 'admin'
password_geoserver = 'gishub@@505'

service_url = URL_GEOSERVER
username = username_geoserver
password = password_geoserver

url = f"{service_url}/rest/layergroups"
headers = {"content-type": "text/xml"}
import requests
r = requests.get(url, auth=(username, password), headers=headers)

if r.status_code == 200:
    print(r.text)
