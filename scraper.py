import requests
from bs4 import BeautifulSoup as bs
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
        

    def set_attrs(self, request_url, request_headers, request_data, reservation_url):
        self.request_url = request_url
        self.request_headers = request_headers
        self.request_data = request_data
        self.reservation_url = reservation_url

    def get_data(self):
        response = requests.post(self.request_url, data=self.request_data, headers=self.request_headers)
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
                {seat_info['from_to']} 배편의 자리가 생겼습니다. 링크를 클릭해 예약을 진행하세요.
                

                예약 링크: {self.reservation_url}

                잔여 좌석: {seat_info['seat_left']}

                출발시간: {seat_info['dep_time']}
                배편이름: {seat_info['ship']}
                자리등급: {seat_info['seat_kind']}
                """

                messages.append(message)
            
            print("Seat found! Sending message")
            self.notifier.send_alert(messages=messages)
    
    def send_messages(self, messages:Union[str, list]):
        self.notifier.send_alert(messages=messages)
