import os
import json
import telebot
import logging
import requests
import datetime

token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
chat_id = os.environ.get('CHAT_ID', '')

num_send = 3

def sort_papers(papers, length):
    output = dict()
    keys = list(papers.keys())
    keys.sort(reverse=True)
    keys = keys[:length]
    for key in keys:
        output[key] = papers[key]
    return output


def convert_to_message(filename: str):
    """
    @param filename: str
    """

    datenow = datetime.date.today()

    with open(filename, "r") as f:
        content = f.read()
        if not content:
            data = {}
        else:
            data = json.loads(content)

    folder = os.path.join(".", "assets", "history")
    if not os.path.exists(folder):
        os.makedirs(folder)

    output_filename = os.path.join(".", "assets", "history", f"{str(datenow)}.telegram.html")

    if not os.path.exists(output_filename):
        open(output_filename, 'x').close()

    with open(output_filename, "a+") as f:
        for topic in data.keys():
            f.write(f"<b><u>#{topic.replace(' ','')}</u></b> \n")
            for subtopic in data[topic].keys():
                day_content = data[topic][subtopic]
                if not day_content:
                    continue

                if topic != subtopic:
                    f.write(f"<b>#{subtopic.replace(' ','')}</b> \n")

                # sort papers by date
                day_content = sort_papers(day_content, num_send)

                for _, v in day_content.items():
                    if v is not None:
                        if v["repo_url"] is not None:
                            f.write(
                              f'• <a href="{v["paper_url"]}"><em>{v["title"]}</em></a> <a href="{v["pdf_url"]}"><em>[PDF]</em></a> <a href="{v["repo_url"]}"><em>[Code]</em></a>\n'
                            )
                        else:
                            f.write(f'• <a href="{v["paper_url"]}"><em>{v["title"]}</em></a> <a href="{v["pdf_url"]}"><em>[PDF]</em></a>\n')

            f.write("\n")
    logging.info("Finished.")
    return output_filename


def request_wallpaper():
    base_url = "https://bing.com"
    url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&ensearch=1&setmkt=en-us'
    r = requests.get(url)
    return base_url + r.json()['images'][0]['url']


def send_message(path):

    with open(path, 'r') as f:
        content = f.read()

    img = request_wallpaper()
    logging.info(img)

    datenow = datetime.date.today()
    output_date = datenow.strftime("%a, %b %-d")
    title = f"<b>Daily Bulletin</b> ({output_date})"
    bot = telebot.TeleBot(token=token)
    result_0 = bot.send_photo(chat_id=chat_id, photo=img, caption=title, parse_mode='HTML')

    if result_0 is not None:
        logging.info('Send image successfully.')

    result_1 = bot.send_message(chat_id=chat_id, text=content, parse_mode='HTML')

    if result_1 is not None:
        logging.info('Send message successfully.')