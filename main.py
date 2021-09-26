import config, scraper, notifier
import time

def scrape(config, scraper):
    scraper.set_attrs(
        config.request_url,
        config.request_headers,
        config.request_data,
        config.reservation_url
    )

    response_bs = scraper.get_data()
    parsed = scraper.parse_data(response_bs)
    scraper.check_empty_seat(parsed)

    if send_log:
        scraper.send_messages(response_bs)

def main(send_log=False):

    scrape(config.UlleungConfig(
        port_from=config.HUPO_ID,
        port_to=config.ULLEUNG_ID,
        departure=config.HUPO2ULLEUNG_DATE,
        ), 
        scraper.TicketChecker("hupo2ulleung")
        )
    scrape(config.UlleungConfig(
        port_from=config.ULLEUNG_ID,
        port_to=config.HUPO_ID,
        departure=config.ULLEUNG2HUPO_DATE,
        ), 
        scraper.TicketChecker("ulleung2hupo")
        )
    scrape(config.DokdoConfig(
        port_from=config.ULLEUNG_ID,
        port_to=config.DOKDO_ID,
        departure=config.DOKDO_DATE,
        ), 
        scraper.TicketChecker("dokdo")
        )
    

if __name__ == "__main__":
    base_config = config.BaseCofig()
    
    count = 0
    sleep = base_config.check_interval
    log_count = base_config.log_interval
    send_log = False
    while 1:
        if config.SEND_LOG and count != 0 and count % log_count == 0:
            send_log = True
        
        main(send_log=send_log)
        print(f"Check count: {count}. Sleep for {sleep} seconds")
        
        send_log = False
        count += 1
        time.sleep(sleep)

