import ipaddress
from .models import IpAddress
import re
import json
from urllib.request import urlopen
import easygui

# gets client data (ip, country, city, ecc...)
def get_client_data():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    user_data = json.load(response)

    return (user_data)
    
# creates a new IpAddress object using the data 
def register_ip(user_data, user, date_time):

    new_IP = IpAddress(
        login_date=date_time ,
        ip_address = user_data['ip'],
        user_logged = user,
        city = user_data['city'],
        country = user_data['country']
    )
    new_IP.save()

# raises a warning if the current IP of the user differs from the previous registered 
def ip_warning(user):
    user_IPs = IpAddress.objects.filter(user_logged=user).order_by('login_date')

    # if there are already IP adresses registered for this user
    if len(user_IPs) > 1:
        previous_ip = user_IPs[1].ip_address
        ip_now = user_IPs[0].ip_address

        if ip_now != previous_ip:
            easygui.msgbox(f"your current IP addres does not match the previous one for this user", title="ip warning!")



