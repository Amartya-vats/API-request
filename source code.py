# from partner import Partner
# from country import Country
from dateutil.parser import parse
import datetime
import requests
import json

class Country:
    def __init__(self):
        self.attendees = []
        self.name = None
        self.start_date = None

    def add_attendee(self, person):
        self.attendees.append(person.email)

    def get_payload(self):
        payload = dict()
        payload['attendeeCount'] = len(self.attendees)
        payload['attendees'] = sorted(self.attendees)
        payload['name'] = self.name
        payload['startDate'] = self.start_date
        return payload


# class to keep track of all partners
# consists of all data like name etc
class Partner:
    def __init__(self, data):
        self.first = data['firstName']
        self.last = data['lastName']
        self.email = data['email']
        self.country = data['country']
        self.dates = data['availableDates']


# here is where we can call the functions with the associated urls
URL_getting ='https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=__'
URL_posting ='https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=__'

#function to get from the url supplied in the main
def getting ():
    r = requests.get(URL_getting)
    return r.json()


def posting(payload):
    r = requests.post(URL_posting, data = json.dumps(payload))
    print(r)

def processing(data):
    list_of_country = []
    # below nested dictionary maintains the relation between country and 
    # dictionary of dates and the people who can attend
    country_dates_attendees = dict()

    for par in data["partners"]:
        x = Partner(par)
        if x.country not in country_dates_attendees:
            country_dates_attendees[x.country] = dict()
        for date in x.dates:
            if date not in country_dates_attendees[x.country]:
                country_dates_attendees[x.country][date] = set()
            country_dates_attendees[x.country][date].add(x)
    
    for country_name, dates_attendees in country_dates_attendees.items():
        # ordered dates are required to check for consistant dates
        sorted_dates = sorted(dates_attendees.keys())
        # variables tto check maximization
        most_attendees_count = float('-inf')
        most_attendees_day = None
        most_attendees = set()

        for index in range(len(sorted_dates[:-1])):
            pln_curr_date = sorted_dates[index]
            pln_next_date = sorted_dates[index + 1]

            curr_date = parse(pln_curr_date)
            next_date = parse(pln_next_date)

            curr_attendees = dates_attendees[pln_curr_date]
            next_attendees = dates_attendees[pln_next_date]
            
            # check for consecutive
            if next_date - curr_date != datetime.timedelta(1):
                continue
            
            # set intersection to check for attendees
            attendees = curr_attendees & next_attendees
            attendees_count = len(attendees)

            if attendees_count > most_attendees_count or \
                    (attendees_count == most_attendees_count and pln_curr_date < most_attendees_day):
                most_attendees_count = attendees_count
                most_attendees_day = pln_curr_date
                most_attendees = attendees

        country = Country()
        country.name = country_name
        if most_attendees_count > 0:
            country.start_date = most_attendees_day
        for person in most_attendees:
            country.add_attendee(person)
        list_of_country.append(country)

    return list_of_country

# serializing to post back to api
def get_payload(result_list):
    payload = dict()
    payload['countries'] = list(map(lambda result: result.get_payload(), result_list))
    return payload

def main():
    data = getting()
    result_list = processing(data)
    payload = get_payload(result_list)
    posting(payload)


if __name__ == '__main__':
    main()
