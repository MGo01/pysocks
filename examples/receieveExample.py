import json
from src.Socket import UDPSocket

def printCatFacts(data):

    catDictionary = json.loads(data)

    catString = (
        f"FUN CAT FACTS\n"
        f"=============\n"
        f"Fact:\n"
        f"{catDictionary['fact']}\n"
    )

    print(catString)

newSocket = UDPSocket(recv_port=4443, socket_type='receiver', buffer_size=2048)
newSocket.receiveData(callback=printCatFacts)
newSocket.clearSockets()