import json
import requests
from pysocks.src.Socket import UDPSocket
from pysocks.src.message import SerialMessage

url = 'https://catfact.ninja/fact'
i = 0
newMessage = SerialMessage(serial_type='json')

while i < 10:
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print ("OoOops: Something Else", err)

    jsonDict = r.json()
    newMessage.createMessage(jsonDict)

    newSocket = UDPSocket(send_port=4443, socket_type='sender', buffer_size=2048)
    newSocket.sendData(data=newMessage, delayMS=0.1)
    i += 1

newSocket.stopSending(encoding='utf-8')
newSocket.clearSockets()