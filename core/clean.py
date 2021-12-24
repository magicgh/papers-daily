import os
import json
import datetime

expire_days = 14


def clean_outdated_papers(filename: str):
    datenow = datetime.date.today()
    if not os.path.exists(filename):
        open(filename, 'x').close()

    with open(filename, "r") as f:
        content = f.read()
        if content:
            data = json.loads(content)
        else:
            return None
    json_data = data.copy()

    for topic in json_data.keys():
        if not json_data[topic]:
            del json_data[topic]
        for subtopic in json_data[topic].keys():
            papers = json_data[topic][subtopic]
            if not papers:
                del json_data[topic][subtopic]
            for id, info in papers.items():
                if (datenow - info["publish_time"]).days > expire_days:
                    del papers[id]

    with open(filename, "w") as f:
        json.dump(json_data, f)


if __name__ == '__main__':

    folder = os.path.join(".", "assets")
    if not os.path.exists(folder):
        os.makedirs(folder)

    json_file = os.path.join(".", "assets", "daily_arxiv.json")
    clean_outdated_papers(json_file)