import json
import os
from models.user import User
from models.item import ItemReport, item_from_dict
from models.claim import Claim

USERS_FILE = "data/users.json"
ITEMS_FILE = "data/items.json"
CLAIMS_FILE = "data/claims.json"


def _load_json(filepath: str) -> list[dict]:
    # 1. Jika file belum ada (not os.path.exists(filepath)), return []
    # 2. Buka file dengan encoding="utf-8", try json.load(f), except json.JSONDecodeError return []
    if not os.path.exists(filepath):
        return []

    with open(filepath, 'r', encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def _save_json(filepath: str, data: list[dict]) -> None:
    # 1. Buat folder jika belum ada: os.makedirs(os.path.dirname(filepath), exist_ok=True)
    # 2. Tulis ke file dengan json.dump(data, f, indent=2, ensure_ascii=False)
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def load_users(filepath: str = USERS_FILE) -> list[User]:
    # Panggil _load_json(filepath), lalu ubah tiap dict menjadi objek User menggunakan User.from_dict
    raw_data = _load_json(filepath)
    return [User.from_dict(item) for item in raw_data]


def save_users(users: list[User], filepath: str = USERS_FILE) -> None:
    # Ubah tiap objek User menjadi dict menggunakan u.to_dict(), lalu simpan dengan _save_json
    raw_data=[user.to_dict() for user in users]
    _save_json(filepath, raw_data)

def load_items(filepath: str = ITEMS_FILE) -> list[ItemReport]:
    raw_data= _load_json(filepath)
    return [item_from_dict(item) for item in raw_data]

def save_items(items: list[ItemReport], filepath: str = ITEMS_FILE) -> None:
    raw_data=[item.to_dict() for item in items]
    _save_json(filepath, raw_data)

def load_claims(filepath: str= CLAIMS_FILE) -> list[Claim]:
    raw_data= _load_json(filepath)
    return [Claim.from_dict(item) for item in raw_data]

def save_claims(claims: list[Claim], filepath: str =CLAIMS_FILE) -> None:
    raw_data=[claim.to_dict() for claim in claims]
    _save_json(filepath, raw_data)
