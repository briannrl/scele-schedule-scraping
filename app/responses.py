from bs4 import BeautifulSoup
import requests
from datetime import datetime

class Scraping:
    def __init__(self):
        self.url = "https://scele.cs.ui.ac.id/mti/"
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')
        self.post_date = datetime.strptime(self.soup.find_all('div', class_='author')[0].text.split(", ")[1], '%d %B %Y').date()

    def scrape_schedule(self):
        latest_info_url = self.soup.find('div', class_ ="forumpost clearfix firstpost starter").find_all('a')[2].get('href')

        latest_info_page = requests.get(latest_info_url)
        latest_info_soup = BeautifulSoup(latest_info_page.text, 'html.parser')

        list_text = [elm.text.replace("\xa0", "") for elm in latest_info_soup.find('div', class_="posting fullpost").find_all(['p', 'pre'])]

        message = f"**POST DATE: {self.post_date}**\n\n"
        for elm in list_text:
            message += elm + "\n"
        return message

def schedule_generator():
    scraping = Scraping()

    if not ((datetime.now().date() == scraping.post_date) and ('[Informasi] Perkuliahan' in scraping.soup.find('div', class_='topic firstpost starter').find('div', class_='subject').text)):
        return
    else:
        scraping.scrape_schedule()

def show_current_schedule():
    scraping = Scraping()
    scraping.scrape_schedule()