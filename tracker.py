import requests
from bs4 import BeautifulSoup
import smtplib
import time

######## User Input Required ########
url = "product-url"
price_target = 500
email_from = "send-from@email.com"
passwd = "password-of-email-from"
email_to = "send-to@email.com"
#####################################

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")

title = soup.find(id="productTitle").get_text()
price = soup.find(id="price_inside_buybox").get_text()

# Removing 'CDN$' and ',' if the price is over $1,000
converted_price = float(price[5:].replace(",", ""))
print(converted_price)


def track_product():
    availability = soup.find(id="availability").get_text().strip()
    str = "out of stock"

    if availability.find(str) == -1:
        if converted_price <= price_target:
            email_notification()
        else:
            print("The price has not met the target price.")
    else:
        print("The product is currently out of stock.")


def email_notification():
    # Simple Mail Transfer Protocol, google port 587
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()  # Establish connection
    server.starttls()  # encrypt connection
    server.ehlo()  # Establish connection

    server.login(email_from, passwd)

    msg = f"Subject: [Alert] Amazon Price update!\n\n\
        \"{title.strip()}\" price fell down to ${converted_price}.\
        \n(Target Price was ${price_target}.)\
        \n\nCheck the product here: {url}"

    server.sendmail(email_from, email_to, msg)
    print("Email has successfully sent!")

    server.quit()


# Track the product once a day
while True:
    track_product()
    time.sleep(60 * 60 * 24)
