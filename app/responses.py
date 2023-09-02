from bs4 import BeautifulSoup
import requests
from datetime import datetime
# from keep_alive import keep_alive

# keep_alive()
def schedule_generator():
    url = "https://scele.cs.ui.ac.id/mti/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    # print(soup)

    post_date = datetime.strptime(soup.find_all('div', class_='author')[0].text.split(", ")[1], '%d %B %Y').date()
    # print(datetime.now().date())
    # print(post_date)
    # print('[Informasi] Perkuliahan' in soup.find('div', class_='topic firstpost starter').find('div', class_='subject').text)
    # break
    if not ((datetime.now().date() == post_date) and ('[Informasi] Perkuliahan' in soup.find('div', class_='topic firstpost starter').find('div', class_='subject').text)):
        # time.sleep(1800)
        # continue
        return "wait 30 minutes, because there's no new schedule update today."
    else:
        latest_info_url = soup.find('div', class_ ="forumpost clearfix firstpost starter").find_all('a')[2].get('href')
        # print(latest_info_url)

        latest_info_page = requests.get(latest_info_url)
        latest_info_soup = BeautifulSoup(latest_info_page.text, 'html.parser')
        # print(latest_info_soup.find('div', class_="posting fullpost").find_all(['p', 'pre']))

        list_text = [elm.text.replace("\xa0", "") for elm in latest_info_soup.find('div', class_="posting fullpost").find_all(['p', 'pre'])]

        message = f"**POST DATE: {post_date}**\n\n"
        for elm in list_text:
            message += elm + "\n"
        # print(message)
        return message
        # break

        # <div class="author" role="heading" aria-level="2" id="yui_3_17_2_1_1693469421343_301">by <a href="https://scele.cs.ui.ac.id/mti/user/view.php?id=2098&amp;course=1">Nurul Fitria Gandhi Nurul</a> - Thursday, 31 August 2023, 11:42 AM</div>

def show_current_schedule():
    url = "https://scele.cs.ui.ac.id/mti/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    # print(soup)

    post_date = datetime.strptime(soup.find_all('div', class_='author')[0].text.split(", ")[1], '%d %B %Y').date()
    # print(datetime.now().date())
    # print(post_date)
    # print('[Informasi] Perkuliahan' in soup.find('div', class_='topic firstpost starter').find('div', class_='subject').text)
    # break
    # if not ((datetime.now().date() == post_date) and ('[Informasi] Perkuliahan' in soup.find('div', class_='topic firstpost starter').find('div', class_='subject').text)):
    #     time.sleep(1800)
    #     continue

    latest_info_url = soup.find('div', class_ ="forumpost clearfix firstpost starter").find_all('a')[2].get('href')
    # print(latest_info_url)

    latest_info_page = requests.get(latest_info_url)
    latest_info_soup = BeautifulSoup(latest_info_page.text, 'html.parser')
    # print(latest_info_soup.find('div', class_="posting fullpost").find_all(['p', 'pre']))

    list_text = [elm.text.replace("\xa0", "") for elm in latest_info_soup.find('div', class_="posting fullpost").find_all(['p', 'pre'])]
    
    message = f"**POST DATE: {post_date}**\n\n"
    for elm in list_text:
        message += elm + "\n"
    # print(message)
    return message