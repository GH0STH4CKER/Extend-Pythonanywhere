import requests
from bs4 import BeautifulSoup
import os

USERNAME = os.environ["PA_USERNAME"]
PASSWORD = os.environ["PA_PASSWORD"]

session = requests.Session()

login_url = "https://www.pythonanywhere.com/login/"
r = session.get(login_url)
soup = BeautifulSoup(r.text, "html.parser")
login_csrf = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

payload = {
    "csrfmiddlewaretoken": login_csrf,
    "auth-username": USERNAME,
    "auth-password": PASSWORD,
    "login_view-current_step": "auth",
}
session.post(login_url, data=payload, headers={"Referer": login_url})

webapps_url = f"https://www.pythonanywhere.com/user/{USERNAME}/webapps/"
r = session.get(webapps_url)
soup = BeautifulSoup(r.text, "html.parser")
csrf = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

extend_url = f"https://www.pythonanywhere.com/user/{USERNAME}/webapps/{USERNAME}.pythonanywhere.com/extend"
r = session.post(extend_url, data={"csrfmiddlewaretoken": csrf}, headers={"Referer": webapps_url})

print("Extend status:", r.status_code, r.reason)
print("Final URL:", r.url)
