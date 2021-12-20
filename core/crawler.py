#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import yaml
import json
import arxiv
import os
import logging

base_url = "https://arxiv.paperswithcode.com/api/v0/papers/"


def get_authors(authors, first_author=False):
    output = str()
    if first_author == False:
        output = ", ".join(str(author) for author in authors)
    else:
        output = authors[0]
    return output


def get_yaml_data(yaml_file: str):

    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    return data


def get_daily_papers(topic: str, query: str, max_results: int = 2):

    content = dict()

    search_engine = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate)

    cnt = 0

    for result in search_engine.results():

        paper_id = result.get_short_id()
        paper_title = result.title
        paper_url = result.entry_id
        pdf_url = result.pdf_url
        code_url = base_url + paper_id
        paper_abstract = result.summary.replace("\n", " ")
        paper_authors = get_authors(result.authors)
        paper_first_author = get_authors(result.authors, first_author=True)
        primary_category = result.primary_category

        publish_time = result.published.date()

        # eg: 2108.09112v1 -> 2108.09112
        ver_pos = paper_id.find('v')
        if ver_pos == -1:
            paper_key = paper_id
        else:
            paper_key = paper_id[0:ver_pos]

        try:
            r = requests.get(code_url).json()
            # source code link
            content[paper_key] = {
              "publish_time": str(publish_time),
              "title": paper_title,
              "author": f"{paper_first_author} et.al.",
              "paper_url": paper_url,
              "pdf_url": pdf_url
            }
            if "official" in r and r["official"]:
                cnt += 1
                repo_url = r["official"]["url"]
                content[paper_key]["repo_url"] = repo_url
            else:
                content[paper_key]["repo_url"] = None

        except Exception as e:
            logging.critical(f"exception: {e} with id: {paper_key}")

    return {topic: content}


def update_json_file(filename: str, data):

    if not os.path.exists(filename):
        open(filename, 'w').close()

    with open(filename, "r") as f:
        content = f.read()
        if not content:
            m = {}
        else:
            m = json.loads(content)

    json_data = m.copy()

    # update papers in each keywords
    for topic in data.keys():
        if not topic in json_data.keys():
            json_data[topic] = {}
        for subtopic in data[topic].keys():
            papers = data[topic][subtopic]

            if subtopic in json_data[topic].keys():
                json_data[topic][subtopic].update(papers)
            else:
                json_data[topic][subtopic] = papers

    with open(filename, "w") as f:
        json.dump(json_data, f)
