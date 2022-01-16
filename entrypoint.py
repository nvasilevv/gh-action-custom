import datetime
import os
import json
import requests
import argparse
import re


def parse_args():
    parser = argparse.ArgumentParser(description="provide keyword")
    parser.add_argument("--keyword", required=True, type=str)
    return parser.parse_args()


def get_event_path() -> dict:
    github_event_path = os.environ.get('GITHUB_EVENT_PATH')
    if github_event_path:
        return {
            'isTest': False,
            'path': github_event_path
        }
    elif os.path.isfile('./sample_push_event.json'):
        return {
            'isTest': True,
            'path': './sample_push_event.json'
        }
    else:
        print('No JSON data to process! :(')


def check_if_word_present(message: str, keyword: str) -> bool:
    match = re.search(keyword, message)
    if match:
        return True
    else:
        return False


def create_release_if_necessary(event_path: dict, keyword: str) -> None:
    if not event_path['path']:
        print('No event_path found')
    events_file = open(event_path['path'])
    events = json.load(events_file)
    to_release = False
    for commit in events['commits']:
        if not to_release:
            to_release = check_if_word_present(commit['message'], keyword)
    if not to_release:
        print("Nothing to process")
        return
    version = datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S')
    data = {'tag_name': f'v{version}',
            'target_commitish': 'master',
            'name': f'v{version}',
            'body': f'Automated release based on keyword: {keyword}',
            'draft': False,
            'prerelease': False
            }
    url = f'https://api.github.com/repos/{os.getenv("GITHUB_REPOSITORY")}/releases?access_token={os.getenv("GITHUB_TOKEN")}'

    if event_path['isTest']:
        print("## [TESTING] Keyword was found but no release created.")
    else:
        response = requests.post(url, data=json.dumps(data))
        print(json.loads(response.content))


if __name__ == "__main__":
    args = parse_args()
    event_path = get_event_path()
    create_release_if_necessary(event_path, args.keyword)
