# simple api requesting and posting a rough sketch

import requests
import json

# easiest way to manupilate json data is to use class and then run loops through it

URL_getting =''
URL_posting =''

#function to get from the url supplied in the main
def getting ():
    r = requests.get(URL_getting)
    return r.json()


def posting(payload):
    r = requests.post(URL_posting, data = json.dumps(payload))
    print(r)

def processing(data):
    make_lists = []

# serializing to post back to api
def get_payload(result_list):
    payload = dict()
    payload['countries'] = list(map(lambda result: ))
    return payload

def main():
    data = getting()
    result_list = processing(data)
    payload = get_payload(result_list)
    posting(payload)


if __name__ == '__main__':
    main()