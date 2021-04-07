from socket import socket, AF_INET, SOCK_DGRAM, create_server, SOCK_STREAM
import pickle
import csv
import ast
import pandas as pd


FORMAT = "utf-8"
HEADERSIZE = 40
# This class saves data
# app = Flask(__name__)


# class storageRecvDataUdp:
#     def __init__(self, host, port):
#         self.host = host
#         self.port = port
#         self.sock = socket(AF_INET, SOCK_DGRAM)
#         # self.recv = dataSenderUdp("localhost", 5556)

#     def turn_on_udp_recv(self):
#         self.sock.bind((self.host, self.port))
#         self.recv_data()

#     def recv_data(self):
#         print("Started the one that receives data")
#         # Empty file content to receive new
#         with open("data.csv", "w") as data_file:
#             data_file.truncate(0)
#         data_file.close()
#         try:
#             while True:
#                 data, addr = self.sock.recvfrom(1024)
#                 decoded = data.decode()
#                 decoded = ast.literal_eval(decoded)
#                 with open("data.csv", "a", encoding=FORMAT) as data_file:
#                     save_data = csv.writer(
#                         data_file, delimiter=";", quotechar="'", quoting=csv.QUOTE_MINIMAL, lineterminator="\r"
#                     )
#                     save_data.writerow([decoded[0], decoded[1]])
#                 data_file.close()
#         except:
#             return "Something went wrong"


# class tcpServer:
  

# def __init__(self, host, port):
#     self.host = host
#     self.port = port



def get_data_from_storage(station):
    """
    Function that get a hour from the user, and returns temperature and precipitation from that hour
    """
    
    if station == "1": # Data fra storage 1

        data = pd.read_csv("Storage1.csv", ";")  # Remember to change this if not correct!!!!!
        
        data_dict = data.to_dict()  # Converts DataFrame to a nested Dictionary

        # Splits up the nested dictionary
        key_list = []  # Gets the keys to split up the nested dictionary
        for key in data_dict.keys():
            key_list.append(key)

       
        temp_dict = data_dict[key_list[0]]  # Dictionary with temperature
        prec_dict = data_dict[key_list[1]]  # Dictionary with precipitation

        temp_list = []
    
        for key in temp_dict:
            temp_list.append(temp_dict.get(key))

        prec_list = []
        for key in prec_dict:
            prec_list.append(prec_dict.get(key))
        
        return temp_list, prec_list


    elif station == "2" or station == "3": # Data fra storage 2 eller 3
        data = pd.read_csv("Storage2.csv", ";") # Endre til rett fil!!!!!

        data_dict = data.to_dict()

        key_list = [] #Key 0 & 1 = station 2 ---- 2 & 3 = station 3
        for key in data_dict.keys():
            key_list.append(key)

        if station == "2":

            temp_dict_2 = data_dict[key_list[0]]
            perc_dict_2 = data_dict[key_list[1]]

            temp_list_2 = []
            for key in temp_dict_2:
                temp_list_2.append(temp_dict_2.get(key))
            
            perc_list_2 = []
            for key in perc_dict_2:
                perc_list_2.append(perc_dict_2.get(key))

            return temp_list_2, perc_list_2

        else: # Station 3
            temp_dict_3 = data_dict[key_list[2]]
            perc_dict_3 = data_dict[key_list[3]]

            temp_list_3 = []
            for key in temp_dict_3:
                temp_list_3.append(temp_dict_3.get(key))
            
            perc_list_3 = []
            for key in perc_dict_3:
                perc_list_3.append(perc_dict_3.get(key))

            return temp_list_3, perc_list_3
    

    else:
        return "Station does not exist"


def tcp_connection_client(host, port):
    """
    Function that connects the server to a TCP client, and handles data from the serverstorage file using get_data() 
    based on data the user wants.
    """

    with socket(AF_INET, SOCK_STREAM) as s:

        print('Binding socket')
        s.bind((host, port))  # Binds socket
        print('Waiting for connection..')
        s.listen()

        while True:
            clientsocket, address = s.accept()
            print('Connected by', address)
            data = clientsocket.recv(1024).decode() # Selection of server

            n_list = pickle.dumps(get_data_from_storage(data))

            n_list = bytes(f'{len(n_list):<{HEADERSIZE}}', FORMAT) + n_list
            clientsocket.send(n_list)




if __name__ == '__main__':
    # server = storageRecvDataUdp("localhost", 5557)
    # server.turn_on_udp_recv()

    tcp_connection_client('127.0.0.1', 5557)

    
