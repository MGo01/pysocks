import json
import requests
from src.Socket import UDPSocket

url = 'https://catfact.ninja/fact'
i = 0

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
    jsonString = json.dumps(jsonDict)

    newSocket = UDPSocket(send_port=4443, socket_type='sender', buffer_size=2048)
    newSocket.sendData(data=jsonString, delayMS=0.1)
    i += 1

newSocket.stopSending()
newSocket.clearSockets()