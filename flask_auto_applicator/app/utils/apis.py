from .const import urls
import requests
import json


def send_request(target, data, request_id):
    headers = {'Content-Type': 'application/json'}
    request_data = {'request_id': request_id, 'data': data}
    response = requests.post(urls[target], headers=headers, data=json.dumps(request_data), timeout=800)
    res_data = json.loads(response.text)
    return res_data
