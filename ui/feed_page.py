from pathlib import Path
import streamlit as st

from models.claim import Claim
from models.constants import CATEGORIES, UI_LOCATIONS
from storage.json_storage import load_claims, load_items, save_claims, save_items


def _mask_npm(npm: str | None) -> str:
    if not npm:
        return "-"
    return f"{npm[:6]}****" if len(npm) >= 6 else "****"


def _next_claim_id(claims: list[Claim]) -> str:
    return f"CLM-{len(claims) + 1:03d}"


def render_feed_page(current_user):
    st.subheader("Radar Barang")

    col_type, col_cat, col_loc, col_q = st.columns([1.2, 1.5, 1.5, 1.8])
    with col_type:
        type_filter = st.selectbox("Tipe", ["Semua", "Ditemukan", "Hilang"])
    with col_cat:
        cat_filter = st.selectbox("Kategori", ["Semua"] + CATEGORIES)
    with col_loc:
        loc_filter = st.selectbox("Lokasi", ["Semua"] + UI_LOCATIONS)
    with col_q:
        query = st.text_input("Cari barang", placeholder="tumbler, KTM, charger...")

    items = load_items()
    filtered = []
    for item in items:
        if type_filter == "Ditemukan" and item.report_type != "FOUND":
            continue
        if type_filter == "Hilang" and item.report_type != "LOST":
            continue
        if cat_filter != "Semua" and item.category != cat_filter:
            continue
        if loc_filter != "Semua" and item.location != loc_filter:
            continue
        if query.strip():
            q = query.strip().lower()
            if q not in item.title.lower() and q not in item.description.lower():
                continue
        filtered.append(item)

    if not filtered:
        st.caption("Tidak ada laporan yang cocok.")
        return

    cols = st.columns(3)
    for idx, item in enumerate(filtered):
        with cols[idx % 3]:
            with st.container(border=True):
                label = "DITEMUKAN" if item.report_type == "FOUND" else "HILANG"
                st.caption(f"**{label}** • {item.status} • {item.category}")
                st.markdown(f"#### {item.title}")

                if item.report_type == "FOUND":
                    if item.blurred_img_path and Path(item.blurred_img_path).exists():
                        st.image(item.blurred_img_path, use_container_width=True)
                        st.caption("Foto disamarkan sampai verifikasi disetujui.")

                if item.category == "KTM UI" and item.ktm_npm:
                    st.markdown(f"**DARURAT KTM** — NPM `{_mask_npm(item.ktm_npm)}`")

                st.write(item.description)
                st.caption(f"Lokasi: {item.location} ({item.location_detail})")
                st.caption(f"Pelapor: {item.reporter_name} ({item.reporter_faculty})")

                if item.report_type == "FOUND" and item.status != "RETURNED":
                    with st.popover("Ini Barang Saya", use_container_width=True):
                        if current_user is None:
                            st.warning("Silakan masuk akun terlebih dahulu di pojok kanan atas.")
                        elif current_user.username == item.reporter_username:
                            st.caption("Ini laporan yang kamu buat sendiri.")
                        else:
                            st.markdown(f"**Pertanyaan Verifikasi:** {item.secret_question}")
                            with st.form(f"claim_form_{item.item_id}"):
                                answer = st.text_input("Jawabanmu")
                                contact = st.text_input("Kontak WA / LINE kamu")
                                if st.form_submit_button("Kirim Klaim", use_container_width=True):
                                    if not answer.strip() or not contact.strip():
                                        st.error("Jawaban dan kontak wajib diisi.")
                                    else:
                                        claims = load_claims()
                                        claims.append(
                                            Claim(
                                                claim_id=_next_claim_id(claims),
                                                item_id=item.item_id,
                                                claimer_username=current_user.username,
                                                claimer_name=current_user.name,
                                                claimer_faculty=current_user.faculty,
                                                claimer_contact=contact.strip(),
                                                secret_answer=answer.strip(),
                                            )
                                        )
                                        save_claims(claims)
                                        if item.status == "OPEN":
                                            item.mark_status("CLAIM_PENDING")
                                            save_items(items)
                                        st.success("Klaim terkirim. Cek progres di menu Klaim Barang.")
                elif item.report_type == "LOST" and item.status != "RETURNED":
                    with st.popover("Bantu Hubungi Pemilik", use_container_width=True):
                        if current_user is None:
                            st.warning("Khusus untuk Civitas UI. Masuk SSO UI dulu untuk melihat kontak pemilik.")
                        else:
                            st.write(f"Kontak Pemilik: **{item.owner_contact}**")
                            st.caption(f"Perkiraan hilang: {item.lost_time_estimate}")
                            st.caption("Gunakan kontak ini hanya untuk mengembalikan barang.")