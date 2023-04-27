# -*- coding:utf-8 -*-
import json

import requests


def send_request(target, data, request_id):
    headers = {'Content-Type': 'application/json'}
    # request_data = {'requestID': request_id, 'data': data}
    request_data = data
    response = requests.post(target, headers=headers, data=json.dumps(request_data), timeout=1000)
    print(response)
    res_data = json.loads(response.text)
    return res_data


if __name__ == '__main__':
    urls = {'collect_info': 'http://121.41.58.52:8497/collect_info',
            'request_txt': 'http://10.252.64.73:6015/api/v1.0/ps_generate',
            'online': 'https://otterwang.com/request_paper'}

    data = {
        'userID': '000001',
        'name': '小李',
        'gender': '',
        'age': '',
        'under-course': '北邮',
        'under-major': '计算机',
        'GPA': ' 3.5',
        'GRE': ' 300',
        'SAT': ' ',
        'TOFEL': '90',
        'IELTS': '',
        'interExe': '大四暑假三星实习两个月，开发了一个人脸识别门禁系统',
        'workingExe': '',
        'projectExe': 'hofeild神经网络的优化与在人脸识别中应用',
        'honor&award': '',
        'prefer-country': '美国',
        'prefer-university': '哈佛',
        'prefer-major': '计算机',
        'motivation': '我爸爸是个程序员，总给我做各种有趣的应用，我也想成为一个可以把创意通过程序实现出来的人',
        'long-term-program': '在学校学习编程，毕业后加入大型互联网公司，以后创业开发自己的app'
    }

    res = send_request(urls['request_txt'], data, '20230325')
    print(res)
