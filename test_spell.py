from bs4 import BeautifulSoup
import requests
from lxml import html

# Variables
SITE = "http://0.0.0.0:5000"
register_url = SITE + "/register"
login_url = SITE + "/login"
payload = {
    'username': 'john',
    'password': 'john123',
    'password_2fa': '12345',
}

def startSession(url):
    session = requests.session()
    output = session.get(url)
    return session


def getCSRF(session, url, creds):
    tree = html.fromstring(session.get(url).text)
    token = list(set(tree.xpath("//input[@name='csrf_token']/@value")))[0]
    creds.update({'csrf_token': token})


def postCreds(session, creds, url):
    output = session.post(url, data=creds, headers=dict(referer=url))
    assert(output.status_code == 200)
    return output


def checkTag(output, tagID):
    soup = BeautifulSoup(output.text, "html.parser")
    resTags = soup.find('div', id=tagID)
    if resTags:
        for tag in resTags:
            print(tag)
            assert(tag == 'success')
    else:
        print(tagID + "was not found")


def delUser(creds):
    from app import app, db
    from app.models import User
    acct = creds.get('username')
    User.query.filter_by(username=acct).delete()
    db.session.commit()


##Registration
#Start register session
regSession = startSession(register_url)

#Obtain CSRF Token
getCSRF(regSession, register_url, payload)

#Register Credentials
regOutput = postCreds(regSession, payload, register_url)

#Find Register ID tag
print("Check Registration ID Tag")
checkTag(regOutput, 'success')

##Login
#Start login session
logSession = startSession(login_url)

#Obtain CSRF Token
getCSRF(logSession, login_url, payload)

#Login with Credentials
logOutput = postCreds(logSession, payload, login_url)

#Find Login ID tag
print("Check Login ID Tag")
checkTag(logOutput, 'result')
