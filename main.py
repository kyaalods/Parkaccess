import requests
from bs4 import BeautifulSoup
import re
import json
import time
import datetime


hrb_webhook = 'https://discord.com/api/webhooks/988996004537839677/PkOPiWhOC6_vFHFfNtPsWP-9Me_h_IuzSaYC5RvRt9nbSXwzOMzkqx55i8tJjMtLIA53'


def discord_webhook(title, product_url, info, image):
  timestamp = time.time()

  list_data = '\n\n'.join(str(x) for x in info)  #Raffle information

  embed = {
    "description": 'Raffle Details' + '\n\n' + list_data,
    # "title": 'Titan',
    "author": {
      'name': title,
      'url': product_url,
      'icon_url': 'https://i.ibb.co/5TSw9px/LOGO-NEW.png'
    },
    "color": 1127128,
    "image": {
      "url": image
    },
    "footer": {
      "text": 'HRB Raffle Monitor v0.0.1'
    },
    "timestamp": str(datetime.datetime.utcfromtimestamp(timestamp))
  }

  data = {
    #"content": "This is titan Schedule",
    "username": 'Park Access Raffle',
    "content": '@everyone' + ' ' + title + 'Has been found',
    "embeds": [
      embed,
    ],
  }
  response = requests.post(hrb_webhook,
                           json=data,
                           headers={"Content-Type": "application/json"})


s = requests.Session()

headers = {
  'user-agent':
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

raffleTitle = []

data = {
  'form_type': 'storefront_password',
  'utf8': '✓',
  'password': 'nikepark1999',
}

response = s.post('https://parkaccess.com.ph/password',
                  headers=headers,
                  data=data)

if response.status_code == 200 or 302:
  while True:
    print('Scraping Parkaccess Membership Exclusive')
    members = s.get('https://parkaccess.com.ph/blogs/member-exclusives')
    soup = BeautifulSoup(members.text, 'html.parser')

    raffles = soup.find_all('div', {'class', 'article-body'})

    raffleLinks = []

    #Getting Raffle Links
    def scrapeParkAccess():

      for raffle in raffles:
        for i in raffle.find_all('a'):

          basedURL = 'https://parkaccess.com.ph/'
          #raffleLinks.append(basedURL+i.get('href'))
          links = s.get(basedURL + i.get('href'))
          soup = BeautifulSoup(links.text, 'html.parser')
          googleLinks = soup.find_all('div', {'class', 'main__article'})
          for links in googleLinks:
            try:
              raffleLinks.append(links.find('a')['href'])
            except:
              pass

    def scrapeGoogleForm():
      #Iterate to all raffle links
      for form in raffleLinks:
        links = s.get(form)
        soup = BeautifulSoup(links.text, 'html.parser')

        try:
          checkForm = soup.find('div', {'class', 'UatU5d'}).text
          print('Form Already Closed')
          if 'closed' in checkForm:
            time.sleep(15)
            pass

        except:
          #Scrape Google Form Here
          #print(form)
          title = soup.find('div', {'class', 'F9yp7e'}).text
          if title in raffleTitle:

            print('Raffles Already posted')
            time.sleep(15)
            continue
          else:
            #print('Form is open')
            raffleTitle.append(title)

            r = s.get(form).text
            output = BeautifulSoup(r, 'html.parser')

            data = output.find('div', {'class', 'cBGGJ'})
            image = output.find_all('img')[1]['src']
            title = output.find('title').text
            details = data.get_text(strip=True, separator='\n').splitlines()

            discord_webhook(title=title,
                            product_url=form,
                            info=details,
                            image=image)

            time.sleep(15)
            print('Scraping Again')
            continue

    scrapeParkAccess()
    scrapeGoogleForm()
else:
  print('IP BANNED')


