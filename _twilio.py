"""
Created on Fri Jul 30 23:03:52 2021
@author: Musya
"""
from twilio.rest import Client
from datetime import datetime
def notify(sid,token):
    try:
        client = Client(sid,token)
        get_time = str(datetime.now())
        time = get_time[10:16]
        date = get_time[0:10]
        client.messages.create(to = ['Receivers Mobile Number'],
                               from_ = ['Senders Number'],
                               body = 'Body of the message here')
    except:
        print("Connection Error")
        pass
if __name__ == "__main__":
    notify()
