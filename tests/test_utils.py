from utils.utils import mask_card_number, mask_account_number, format_transaction, get_latest_completed_transactions
from datetime import datetime
import pytest

def test_mask_card_number():
    assert mask_card_number("Visa Classic 4842793835621314") == "Visa Classic 4842 79** **** 1314"
    assert mask_card_number("MasterCard 7158300734726758") == "MasterCard 7158 30** **** 6758"






