import socket
import pickle
import matplotlib.pyplot as plt

HEADERSIZE = 40
FORMAT = "utf-8"

HOST = '127.0.0.1' # The server's hostname or IP address    # Remember to change this if not correct!!!!!
PORT = 5557 # The port used by the server    # Remember to change this if not correct!!!!!


# Usikker på om vi skal ha dette lenger?

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Connected to server..')
    print('Enter a server you want to get weather data from...')
    server = input()
    s.sendall(bytes(server, FORMAT)) # Sends the request for specific weather data.
    # data = s.recv(1024)


    full_msg = b''
    new_msg = True
    while True:
        n_list = s.recv(1024) #Kan vær det må vær større en 16.
        if new_msg:
        #   print(f"new message length: {msg[:HEADERSIZE]}") bare printer ut len til "bytes" formaten
            msglen = int(n_list[:HEADERSIZE])
            new_msg = False

        full_msg += n_list
        print(len(full_msg)-HEADERSIZE)
        print(msglen)


        if len(full_msg)-HEADERSIZE == msglen:
            print("full message received")
        #  print(full_msg[HEADERSIZE:]) #Her er den listen i "bytes" altså i "pickle " format

            n_list = pickle.loads(full_msg[HEADERSIZE:]) #Her konverterer vi den til "string" format
            print(n_list) #Her printes det

            temp_list = n_list[0]
            perc_list = n_list[1]
            
        break


def graph(temperature, percipition, day):
    """
    Method to draw up a graph of temperature and percipition
    Param; temperature - list of temperatures
    Param; percipition - list of percipition
    Param; day - which day the user wants to see graph of (int)
    """

    time = [] # Time list
    for i in range(24):
        time.append(i+1)

    fig, (ax1, ax2) = plt.subplots(2, 1)
    # make a little space between the subplots
    fig.subplots_adjust(hspace=1)

    # Graph 1 temp
    ax1.plot(time, temperature)
    ax1.set(xlabel='time (h)', ylabel='temperature (c)', title=f'Temperature in Bergen at day {day}')
    ax1.grid()

    # Graph 2 perc
    ax2.plot(time, percipition)
    ax2.set(xlabel='time (h)', ylabel='percipition (mm)', title=f'Percipition in Bergen at day {day}')
    ax2.grid()

    plt.show()


# Day selection
print("Select a day to show graph from: (number)")
day = input()

# Error messaging
if int(day) > 3 or int(day) < 1:
    print('Only weatherdata for day 1-3')


# Shows the right graph
elif int(day) == 1: # Day 1
    graph(temp_list[:24], perc_list[:24], day)
elif int(day) == 2: # Day 2
    graph(temp_list[24:48], perc_list[24:48], day)
elif int(day) == 3: # Day 3
    graph(temp_list[48:], perc_list[48:], day)
