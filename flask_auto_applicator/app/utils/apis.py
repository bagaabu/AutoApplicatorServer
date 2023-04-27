from .const import urls
import requests
import json


def send_request(target, data):
    headers = {'Content-Type': 'application/json'}
    request_data = data
    response = requests.post(urls[target], headers=headers, data=json.dumps(request_data), timeout=1000)
    res_data = json.loads(response.text)
    return res_data
