from datetime import datetime

from utils.utils import mask_card_number, mask_account_number, format_transaction, get_latest_completed_transactions


def test_mask_card_number():
    assert mask_card_number("Visa Classic 4842793835621314") == "Visa Classic 4842 79** **** 1314"
    assert mask_card_number("MasterCard 7158300734726758") == "MasterCard 7158 30** **** 6758"

def test_mask_account_number():
    assert mask_account_number("Счет 35383033474447895560") == '**5560'

def test_format_transaction():
    a = {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
      "amount": "31957.58",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"
  }
    b = ("26.08.2019 Перевод организации\n"
        "Maestro 1596 83** **** 5199 -> Счет **9589\n"
        "31957.58 руб.")
    assert format_transaction(a) == b

def test_get_latest_completed_transactions():
    data = [
        {
            "date": "2023-08-01T09:30:00.000",
            "description": "Перевод на счет",
            "operationAmount": {
                "amount": 100,
                "currency": {"name": "USD"}
            },
            "from": "Счет 12345678",
            "to": "Счет 23456789",
            "state": "EXECUTED"
        },
    ]
    result = get_latest_completed_transactions(data)
    assert result[0]["state"] == "EXECUTED"

    expected_date_order = sorted(
        [datetime.strptime(tr["date"], "%Y-%m-%dT%H:%M:%S.%f") for tr in result],
        reverse=True,
    )
    actual_dates_order = [
        datetime.strptime(tr["date"], "%Y-%m-%dT%H:%M:%S.%f") for tr in result
    ]
    assert actual_dates_order == expected_date_order





