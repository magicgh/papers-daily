import os
import re
import yaml
import telebot
import logging
import requests
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO)

token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
chat_id = os.environ.get('CHAT_ID', '')


def get_yaml_data(yaml_file: str):

    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    return data


def send_message(url):
    bot = telebot.TeleBot(token=token)
    content = f'#VALSE \n {url}'
    result = bot.send_message(chat_id=chat_id, text=content, disable_web_page_preview=False)

    if result is not None:
        logging.info('Send message successfully.')


if __name__ == '__main__':
    yaml_path = os.path.join(".", "config", "valse.yaml")
    yaml_data = get_yaml_data(yaml_path)
    seq = yaml_data['Sequence Number']
    pattern_1 = '<h1 class="ph">VALSE 论文速览'
    pattern_2 = '<h1 class="ph">[0-9]{8}-[0-9]{2}'
    ua = UserAgent()
    while True:
        url = f"http://valser.org/article-{seq}-1.html"
        logging.info(url)
        r = requests.get(url, headers={"User-Agent": ua.random})

        null_exp = (r.text.find(pattern_1) == -1 and re.search(pattern_2, r.text) is None)

        if r.text.find('抱歉，您指定要查看的文章不存在或正在审核') != -1:
            break
        elif not null_exp:
            send_message(url)
        seq += 1

    yaml_data['Sequence Number'] = seq

    with open(yaml_path, 'w') as f:
        yaml.dump(yaml_data, f)

    logging.info('Update sequence number successfully.')