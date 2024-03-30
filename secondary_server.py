import zmq

# Initialize ZeroMQ context and socket for communication with main server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def process_message(message):
    # Example processing of received message
    player_id = message.get("player_id")
    data = message.get("data")
    return {"received_player_id": player_id, "received_data": data}

if __name__ == "__main__":
    while True:
        message = socket.recv_json()
        response = process_message(message)
        socket.send_json(response)
