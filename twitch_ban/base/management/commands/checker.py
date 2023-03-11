import time

import requests
from django.core.management.base import BaseCommand
from base.models import Chanel, TelegramAccount
from datetime import datetime
from django.utils.timezone import make_aware
import telebot
bot = telebot.TeleBot(token="5826015068:AAGmVwCYBxSthSqAIEUbIhxCrWEgw5RkjqE")


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
    if response.status_code == 400:
        return False
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


def main():
    while True:
        for channel in Chanel.objects.all():
            if channel.ban is True:
                continue
            username = str(channel.link).split('/')[-1]
            print(username)
            try:
                check_result = channel_check(username)
            except Exception as e:
                print(e)
                time.sleep(60)
                continue
            print(check_result)
            if not check_result:
                channel.ban = True
                channel.ban_date = make_aware(datetime.now())
                channel.save()
                for account in TelegramAccount.objects.all():
                    bot.send_message(account.telegram_id, f'Канал {channel.link} был забанен!')
            else:
                channel.spectators = check_result[0]
                channel.subscribers = check_result[1]
                channel.save()
            print('+')
            time.sleep(10)
        time.sleep(30)


class Command(BaseCommand):
    help = 'Старт ТГ-бота'

    def handle(self, *args, **options):
        main()
