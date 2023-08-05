import json
from datetime import datetime


def mask_card_number(number):
    text, card_number = number.rsplit(" ", 1)
    formatted_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    result = f"{text} {formatted_number}"
    return result
def mask_account_number(number):
    return "**" + number[-4:]


def format_transaction(transaction):
    date = datetime.strptime(transaction["date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
    description = transaction["description"]
    amount = transaction["operationAmount"]["amount"]
    currency = transaction["operationAmount"]["currency"]["name"]

    if "from" in transaction:
        if transaction["from"].startswith("Счет"):
            from_number = mask_account_number(transaction["from"][5:])
            from_text = f"Счет {from_number}"
        else:
            from_number = mask_card_number(transaction["from"])
            from_text = from_number
    else:
        from_text = ""

    to_number = mask_account_number(transaction["to"][5:])
    to_text = f"Счет {to_number}"

    result = f"{date} {description}\n"
    if from_text:
        result += f"{from_text} -> {to_text}\n"
    else:
        result += f"{to_text}\n"
    result += f"{amount} {currency}"

    return result


def get_latest_completed_transactions(data, n_transactions=5):
    completed_transactions = [t for t in data if t.get("state") == "EXECUTED"]
    completed_transactions.sort(key=lambda t: t["date"], reverse=True)
    return completed_transactions[:n_transactions]


filename = "operation.json"

with open(filename, 'r') as file:
    data = json.load(file)

transactions = get_latest_completed_transactions(data)
formatted_transactions = [format_transaction(tr) for tr in transactions]

for tr in formatted_transactions:
    print(tr)
    print()
