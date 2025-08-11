from dataclasses import dataclass


@dataclass
class Customer:
    """
    顧客データモデル
    """

    customer_id: str
    name: str
    address: str = ""
    phone: str = ""


@dataclass
class Bank:
    """
    銀行データモデル
    """

    bank_id: str
    bank_name: str
    account_number: str = ""
    branch: str = ""
