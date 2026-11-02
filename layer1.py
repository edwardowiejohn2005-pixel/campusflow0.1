import json

def Load_Ticket():
    try:
        with open("tickets.json", "r") as file:
            tickets = json.load(file)
            return tickets
    except FileNotFoundError:
        return []

def Save_Ticket(tickets):
    with open("tickets.json", "w") as file:
        json.dump(tickets, file, indent=2)

def Create_Ticket():
    Empty = []

    T_id = input("Input Ticket ID :  ").lower()
    T_description = input("What is Your Problem  : ").lower()

    reading = Load_Ticket(Empty)
    reading.append({"T_id": T_id, "T_description": T_description})
    Save_Ticket(reading)

Create_Ticket()
