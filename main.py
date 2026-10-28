import json

def Load_Ticket(tickets):
#    try:
     with open("ticket.json", "r")as file:
        ticket = json.load(file)
        print(ticket)
 #   except FileNotFoundError:
        return []

def Save_Ticket(ticket):
    with open("ticket.json", "a")as file:
        json.dump(ticket, file, indent=2)

def Create_Ticket():
    Empty = []

    T_id = input("Input Ticket ID :  ").lower()
    T_description = input("What is Your Problem  : ").lower()

    reading = Load_Ticket(Empty)
    reading.append({"T_id": T_id, "T_description": T_description})
    Save_Ticket(reading)

Create_Ticket()
