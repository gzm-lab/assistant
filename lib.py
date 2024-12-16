import requests

def dl_vocal_msg(url,msg_id):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"mp3/{msg_id}.ogg", 'wb') as file:
            file.write(response.content)
        return True
    else:
        return False