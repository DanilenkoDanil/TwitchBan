import requests



def channel_check(username: str):
    client_id = 'jfiuj3y981o2j2k8bazv02a62kjdzt'
    client_secret = 'y8da03o661is3jdf3r9aadhsvzs9n2'

    response = requests.post(
        f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials')
    response_data = response.json()

    access_token = response_data['access_token']
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get(
        f'https://api.twitch.tv/helix/streams?user_login={username}',
        headers=headers
    )
    result_dict = response.json()
    if len(result_dict['data']) > 0:
        viewers = result_dict['data'][0]['viewer_count']
        response = requests.get(f"https://api.twitch.tv/helix/users?login={username}", headers=headers).json()
        twitch_id = response["data"][0]["id"]
        response = requests.get(
            f'https://api.twitch.tv/helix/users/follows?to_id={twitch_id}&first=1',
            headers=headers
        )
        subscribers = response.json()['total']
        return [viewers, subscribers]
    else:
        return False


print(channel_check('norskcazinotester'))
