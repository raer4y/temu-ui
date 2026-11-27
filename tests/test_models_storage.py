import pytest
from models.user import User
from models.item import LostReport, FoundReport, item_from_dict
from models.claim import Claim
from models.constants import KARMA_REWARD_RETURNED
from storage.json_storage import (
    load_users,
    save_users,
    load_items,
    save_items,
    load_claims,
    save_claims,
)


def test_user_model_and_karma():
    user = User(
        username="budi_ui",
        password_hash="hashed_pw_123",
        name="Budi Santoso",
        faculty="Fasilkom",
    )
    assert user.karma_points == 0

    # Uji penambahan karma sesuai konstanta resmi
    user.add_karma(KARMA_REWARD_RETURNED)
    assert user.karma_points == 50

    # Uji validasi: karma negatif wajib melempar ValueError
    with pytest.raises(ValueError):
        user.add_karma(-10)

    # Uji serialisasi JSON
    reconstructed = User.from_dict(user.to_dict())
    assert reconstructed.username == "budi_ui"
    assert reconstructed.name == "Budi Santoso"
    assert reconstructed.faculty == "Fasilkom"
    assert reconstructed.karma_points == 50


def test_item_inheritance_and_polymorphism():
    lost = LostReport(
        item_id="ITM-001",
        title="Tumbler Corkcicle Hitam",
        category="Tumbler / Botol Minum",
        location="Perpustakaan Pusat (Perpusat)",
        location_detail="Lantai 2 dekat sofa",
        description="Ada stiker Fasilkom di bagian bawah",
        reporter_username="budi_ui",
        reporter_name="Budi Santoso",
        reporter_faculty="Fasilkom",
        lost_time_estimate="2026-11-26 14:00",
        owner_contact="08123456789",
    )
    found = FoundReport(
        item_id="ITM-002",
        title="KTM UI a.n. Siti",
        category="KTM UI",
        location="Halte Stasiun UI",
        location_detail="Dekat gate tap-in",
        description="KTM angkatan 2024",
        reporter_username="ani_feb",
        reporter_name="Ani Wijaya",
        reporter_faculty="FEB",
        original_img_path="assets/orig_ktm.jpg",
        blurred_img_path="assets/blur_ktm.jpg",
        secret_question="Apa 3 digit terakhir NPM?",
        handoff_method="DIRECT",
        finder_contact="@aniwijaya",
        ktm_npm="2406123456",
    )

    assert lost.report_type == "LOST"
    assert found.report_type == "FOUND"

    # Uji validasi mark_status sesuai ITEM_STATUSES ("OPEN", "CLAIM_PENDING", "RETURNED")
    lost.mark_status("CLAIM_PENDING")
    assert lost.status == "CLAIM_PENDING"

    lost.mark_status("RETURNED")
    assert lost.status == "RETURNED"

    with pytest.raises(ValueError):
        lost.mark_status("STATUS_NGASAL")

    # Uji factory item_from_dict
    parsed_lost = item_from_dict(lost.to_dict())
    parsed_found = item_from_dict(found.to_dict())
    assert isinstance(parsed_lost, LostReport)
    assert isinstance(parsed_found, FoundReport)
    assert parsed_found.ktm_npm == "2406123456"


def test_claim_model_validation():
    claim = Claim(
        claim_id="CLM-001",
        item_id="ITM-002",
        claimer_username="siti_fisip",
        claimer_name="Siti Rahma",
        claimer_faculty="FISIP",
        claimer_contact="08987654321",
        secret_answer="456",
    )
    assert claim.status == "PENDING"

    with pytest.raises(ValueError):
        claim.decide("PENDING")

    with pytest.raises(ValueError):
        claim.decide("INVALID")

    claim.decide("APPROVED")
    assert claim.status == "APPROVED"


def test_json_storage_roundtrip(tmp_path):
    users_file = str(tmp_path / "users.json")
    items_file = str(tmp_path / "items.json")
    claims_file = str(tmp_path / "claims.json")

    assert load_users(users_file) == []
    assert load_items(items_file) == []
    assert load_claims(claims_file) == []

    # Simpan dan muat ulang Users (4 parameter wajib sesuai User.__init__)
    u1 = User("user1", "hash1", "User Satu", "FT")
    save_users([u1], users_file)
    loaded_users = load_users(users_file)
    assert len(loaded_users) == 1
    assert loaded_users[0].username == "user1"
    assert loaded_users[0].name == "User Satu"

    # Simpan dan muat ulang Items (LostReport & FoundReport)
    item1 = LostReport(
        "ITM-1", "Kunci Motor", "Kunci / STNK", "Kantin Pacil / Fasilkom", "Meja 3",
        "Gantungan merah", "user1", "User Satu", "FT", "10:00", "08111"
    )
    item2 = FoundReport(
        "ITM-2", "Payung Lipat", "Payung / Jaket", "Bikun Biru", "Kursi belakang",
        "Warna biru", "user1", "User Satu", "FT", "orig.png", "blur.png",
        "Merek payung?", "SAFE_DROP_OFF", "08111", "Pos Satpam Gerbang Utama"
    )
    save_items([item1, item2], items_file)
    loaded_items = load_items(items_file)
    assert len(loaded_items) == 2
    assert isinstance(loaded_items[0], LostReport)
    assert isinstance(loaded_items[1], FoundReport)

    # Simpan dan muat ulang Claims
    c1 = Claim("CLM-1", "ITM-2", "user2", "User Dua", "FMIPA", "08222", "Sakura")
    save_claims([c1], claims_file)
    loaded_claims = load_claims(claims_file)
    assert len(loaded_claims) == 1
    assert loaded_claims[0].secret_answer == "Sakura"