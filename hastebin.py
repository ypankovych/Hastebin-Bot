import json
import requests

new_paste_url = 'https://hastebin.com/documents'

def paste(paste_content):
    try:
        response = requests.post(new_paste_url, data=paste_content, timeout=1000).json()
    except json.decoder.JSONDecodeError:
        return {'status': 0, 'message': 'Application Error'}
    if response.get('key'):
        return {'status': 1, 'result': response['key']}
    else:
        return {'status': 0, 'message': response['message']}
