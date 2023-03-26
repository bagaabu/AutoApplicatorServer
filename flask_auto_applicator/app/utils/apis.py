from .const import urls


def send_request(target, data, request_id):
    headers = {'Content-Type': 'application/json'}
    request_data = {'request_id': request_id, 'data': data}
    response = requests.post(urls[target], headers=headers, data=json.dumps(request_data))
    res_data = json.loads(response.text)
    return res_data
