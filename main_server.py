import zmq

# Initialize ZeroMQ context and socket for communication with secondary server
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def send_message_to_secondary_server(message):
    socket.send_json(message)
    response = socket.recv_json()
    return response

# Example function to send player data to the secondary server
def send_player_data_to_secondary_server(player_id, data):
    message = {
        "player_id": player_id,
        "data": data
    }
    return send_message_to_secondary_server(message)

if __name__ == "__main__":
    # Example usage
    player_id = 123
    player_data = {"name": "John", "score": 100}
    
    # Send player data to the secondary server
    response = send_player_data_to_secondary_server(player_id, player_data)
    print("Response from secondary server:", response)
