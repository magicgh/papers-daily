import os
import logging
from bot import convert_to_message, send_message
from crawler import get_yaml_data, get_daily_papers, update_json_file

num_result = 7

# DEBUG
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    data_collector = dict()

    yaml_path = os.path.join(".", "assets", "config.yaml")
    yaml_data = get_yaml_data(yaml_path)

    for topic, contents in yaml_data.items():

        assert isinstance(contents, dict)

        for subtopic, keyword in contents.items():

            logging.info(f"Keyword: {subtopic}")
            try:
                data = get_daily_papers(topic=subtopic, query=keyword, max_results=num_result)
            except:
                logging.warning(f'Cannot get {subtopic} data from arxiv.')
                data = None
            # time.sleep(random.randint(2, 10))

            if not topic in data_collector.keys():
                data_collector[topic] = {}

            if data:
                data_collector[topic].update(data)

    # logging.info(data_collector)

    folder = os.path.join(".", "assets")

    if not os.path.exists(folder):
        os.makedirs(folder)

    json_file = os.path.join(".", "assets", "arxiv.json")

    update_json_file(json_file, data_collector)

    path = convert_to_message(json_file)

    send_message(path)