import json
import requests

new_paste_url = 'https://hastebin.com/documents'

def paste(paste_content):
    try:
        response = requests.post(new_paste_url, data=paste_content, timeout=1000).json()
    except json.decoder.JSONDecodeError:
        return 'Application Error'
    if response.get('key'):
        return response
    else:
        return response['message']
