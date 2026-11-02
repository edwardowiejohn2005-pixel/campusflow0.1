
import json
import os
import urllib.request
import urllib.error


FILE_NAME = "tickets.json"
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def Load_Ticket():
    try:
        with open(FILE_NAME, "r") as file:
            tickets = json.load(file)

        if not isinstance(tickets, list):
            raise ValueError("Ticket storage must be a list.")

        return tickets

    except FileNotFoundError:
        return []

    except (json.JSONDecodeError, ValueError):
        print("Error: The tickets file contains invalid data.")
        return None

    except OSError as error:
        print("Could not read tickets:", error)
        return None


def Save_Ticket(tickets):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(tickets, file, indent=2)

        return True

    except OSError as error:
        print("Could not save ticket:", error)
        return False


def AI_Suggestions(description):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("AI Error: OPENROUTER_API_KEY is missing.")
        return

    prompt = (
        "You are a helpful campus IT support assistant. "
        "Suggest 4 practical steps to fix or investigate "
        "the following problem. Use simple, clear language.\n\n"
        f"Ticket description: {description}"
    )

    data = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    print("\nGetting AI suggestions...")

    try:
        with urllib.request.urlopen(
            request, timeout=30
        ) as response:
            result = json.load(response)

        suggestions = result["choices"][0]["message"]["content"]

        if not isinstance(suggestions, str) or not suggestions.strip():
            raise ValueError("Empty AI response")

        print("\nSuggestions:\n")
        print(suggestions)

    except urllib.error.HTTPError as error:
        print(f"AI request failed (HTTP {error.code}).")
        if error.code == 401:
            print("Check your API key.")
        elif error.code == 429:
            print("Rate limit reached. Try again later.")
        elif error.code in (502, 503):
            print("The AI service is temporarily unavailable.")

    except urllib.error.URLError:
        print("Network error: Check your internet connection.")

    except TimeoutError:
        print("The AI request timed out.")

    except (ValueError, KeyError, IndexError, TypeError):
        print("The AI returned an invalid response.")


def Create_Ticket():
    tickets = Load_Ticket()

    if tickets is None:
        print("Ticket creation cancelled to protect saved data.")
        return

    description = input(
        "What is your problem? "
    ).strip()

    if not description:
        print("Error: Description cannot be empty.")
        return

    existing_ids = [
        ticket["T_id"]
        for ticket in tickets
        if isinstance(ticket, dict)
        and isinstance(ticket.get("T_id"), int)
    ]

    ticket_id = max(existing_ids, default=0) + 1

    new_ticket = {
        "T_id": ticket_id,
        "T_description": description
    }

    tickets.append(new_ticket)

    if not Save_Ticket(tickets):
        return

    print("\nTicket created successfully!")
    print("ID:", new_ticket["T_id"])
    print("Description:", new_ticket["T_description"])

    AI_Suggestions(new_ticket["T_description"])


if __name__ == "__main__":
    Create_Ticket()
