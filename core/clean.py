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
        if not content:
            data = {}
        else:
            data = json.loads(content)

    json_data = data.copy()

    for topic in json_data.keys():
        for subtopic in data[topic].keys():
            papers = data[topic][subtopic]
            for id, info in papers.items():
                if (datenow - info["publish_date"]).days > expire_days:
                    del papers[id]

    with open(filename, "w") as f:
        json.dump(json_data, f)


if __name__ == '__main__':
    json_file = os.path.join(".", "assets", "daily_arxiv.json")
    clean_outdated_papers(json_file)