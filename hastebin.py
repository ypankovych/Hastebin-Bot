import requests

new_paste_url = 'https://hastebin.com/documents'

def paste(paste_content):
    response = requests.post(new_paste_url, data=paste_content, timeout=1000)
    try:
        return response.json()['key']
    except KeyError:
        return False
