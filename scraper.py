import requests
from bs4 import BeautifulSoup as bs
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import notifier
from typing import Union

class TicketChecker:
    def __init__(self, name) -> None:
        self.name = name
        self.request_url = None
        self.request_headers = None
        self.request_data = None
        self.reservation_url = None

        self.notifier = notifier.TelegramNotification()
        
        # Session with retry strategy
        self.session = requests.session()
        assert_status_hook = lambda response, *args, **kwargs: response.raise_for_status()
        self.session.hooks['response'] = [assert_status_hook]

        retry_strategy = Retry(
            total=10,
            status_forcelist=[413, 429, 500, 502, 503, 504],
            method_whitelist=['GET'],
            backoff_factor=2
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)        

    def set_attrs(self, request_url, request_headers, request_data, reservation_url):
        self.request_url = request_url
        self.request_headers = request_headers
        self.request_data = request_data
        self.reservation_url = reservation_url

    def get_data(self):
        response = self.session.post(self.request_url, data=self.request_data, headers=self.request_headers)
        response_bs = bs(response.content, 'html.parser')

        return response_bs
    
    def parse_data(self, response_bs):
        parsed = response_bs.find_all('tr')
        parsed = [tr.find_all('td') for tr in parsed]
        parsed = [
            {
                'from_to': l[1].text, 
                'dep_time': l[2].text, 
                'ship': l[3].text, 
                'seat_kind': l[4].text, 
                'seat_left': l[5].text,
            } 
            for l in parsed]
        
        return parsed
    
    def check_empty_seat(self, parsed):
        available = []
        for seat_info in parsed:
            try:
                seats = int(seat_info['seat_left'])
                if seats >= 1:
                    available.append(seat_info)
            except ValueError as e:
                print(repr(e))
                raise e
            except Exception as e:
                print(repr(e))
                raise e
        
        if available:
            messages = []
            for seat_info in available:
                message = f"""
                {seat_info['from_to']} ????????? ????????? ???????????????. ????????? ????????? ????????? ???????????????.
                

                ?????? ??????: {self.reservation_url}

                ?????? ??????: {seat_info['seat_left']}

                ????????????: {seat_info['dep_time']}
                ????????????: {seat_info['ship']}
                ????????????: {seat_info['seat_kind']}
                """

                messages.append(message)
            
            print("Seat found! Sending message")
            self.notifier.send_alert(messages=messages)
    
    def send_messages(self, messages:Union[str, list]):
        self.notifier.send_alert(messages=messages)
