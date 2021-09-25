import requests
from bs4 import BeautifulSoup as bs

class TicketChecker:
    def __init__(self, name) -> None:
        self.name = name
        self.request_url = None
        self.request_header = None
        self.request_data = None
        # TODO: Init Telegram Notifier 

    def set_attrs(self, request_url, request_header, request_data):
        self.request_url = request_url
        self.request_header = request_header
        self.request_data = request_data

    def get_data(self):
        response = requests.post(self.request_url, headers=self.request_header)
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
        
        # TODO: Send Telegram notification if available