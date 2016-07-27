from __future__ import print_function

import requests
from bs4 import BeautifulSoup

from auto_eSD.config import secrets

# constants read from the esd.yml file.  check the README for more information
ESD_USERNAME = secrets['esd']['username']
ESD_PASSWORD = secrets['esd']['secret']
ESD_HIDDEN_NAME = secrets['esd']['hidden_file']

# constants for the functions below
ESD_LOGIN = 'http://esd.eschooldata.com/Login.aspx'
ESD_CR = 'http://esd.eschooldata.com/CustomReports/CRPT000010.aspx'


def fetch_access_db(destination='Access.zip'):
    """
    Logs in to eSchoolData and navigates to the 'Access Downloads' page.
    Posts a request to that page to get the hidden Access file.

    Args:
        destination (str): Destination (directory plus filename) where you
        want to write the access backup file.

    Returns:
        bool: True for success, False otherwise.
    """
    # initialize a session
    s = requests.Session()
    r = s.get(ESD_LOGIN)

    # create the payload for POST, then make the request, and go to the custom reports page
    login_payload = {
        '__VIEWSTATE': BeautifulSoup(r.content, 'html.parser').find(id='__VIEWSTATE')['value'],
        'txtUserName': ESD_USERNAME,
        'txtPassword': ESD_PASSWORD,
        'btnLogin': 'Login'
    }
    s.post(ESD_LOGIN, data=login_payload)
    r = s.get(ESD_CR, headers={'Referer': ESD_LOGIN})

    # make a POST request on the custom reports page to get the hidden zipped Access file
    fn = BeautifulSoup(r.content, 'html.parser').find(id='ContentPlaceHolder1_repFiles_Accessdownloader_0')['value']

    access_payload = {
        '__EVENTTARGET': None,
        '__EVENTARGUMENT': None,
        '__VIEWSTATE': BeautifulSoup(r.content, 'html.parser').find(id='__VIEWSTATE')['value'],
        '__PREVIOUSPAGE': BeautifulSoup(r.content, 'html.parser').find(id='__PREVIOUSPAGE')['value'],
        'ctl00$ContentPlaceHolder1$rdFileType': 2,
        'ctl00$ContentPlaceHolder1$repFiles$ctl00$Accessdownloader': fn,
        # thankfully the hashed hidden file name does not appear to change.  check the README for more info
        # you should presumably keep the hashed file name out of version control
        'ctl00$ContentPlaceHolder1$hidURL': ESD_HIDDEN_NAME
    }

    r = s.post(ESD_CR, data=access_payload, headers={'Referer': ESD_LOGIN})

    # if the request is successful, save the file
    if r.status_code == 200:
        with open(destination, 'wb') as out_file:
            out_file.write(r.content)
        print('Successfully grabbed Access.zip!')
        out = True
    else:
        r.raise_for_status()
        out = False

    return out
