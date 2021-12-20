import os
import json
import telebot
import logging
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
    output_date = datenow.strftime("%b %-d")

    with open(filename, "r") as f:
        content = f.read()
        if not content:
            data = {}
        else:
            data = json.loads(content)

    output_filename = os.path.join(".", "core", "history", f"{str(datenow)}.telegram.html")

    if not os.path.exists(output_filename):
        open(output_filename, 'w').close()

    with open(output_filename, "a+") as f:
        f.write(f"<b><ins>Daily Bulletin</ins> ({output_date})</b>\n")
        for topic in data.keys():
            f.write(f"<b>#{topic.replace(' ','')}</b> \n")
            for subtopic in data[topic].keys():
                day_content = data[topic][subtopic]
                if not day_content:
                    continue
                # the head of each part
                if topic != subtopic:
                    f.write(f"#{subtopic.replace(' ','')} \n")

                # sort papers by date
                day_content = sort_papers(day_content, num_send)

                for _, v in day_content.items():
                    if v is not None:
                        f.write(f'• <a href="{v["paper_url"]}"><em>{v["title"]}</em></a> \n')

            f.write("\n")
    logging.info("Finished.")
    return output_filename


def send_message(path):

    with open(path, 'r') as f:
        content = f.read()

    bot = telebot.TeleBot(token=token)
    result = bot.send_message(chat_id=chat_id, text=content, parse_mode='HTML')

    if result is not None:
        logging.info('Send message successfully.')
