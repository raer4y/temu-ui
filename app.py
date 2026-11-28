from pathlib import Path
import streamlit as st

from ui.feed_page import render_feed_page
from ui.sso_page import render_sso_page

st.set_page_config(
    page_title="TEMU.UI | Lost & Found",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def load_css():
    css_path = Path("assets/style.css")
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


def render_navbar():
    if "current_user" not in st.session_state:
        st.session_state["current_user"] = None

    user = st.session_state["current_user"]
    col_brand, col_auth = st.columns([4, 1.3], vertical_alignment="center")
    with col_brand:
        st.markdown("### TEMU.UI")
        st.caption("Lost & Found Universitas Indonesia")
    with col_auth:
        if user is None:
            if st.button("Masuk SSO UI", use_container_width=True):
                st.session_state["show_sso_page"] = True
                st.rerun()
        else:
            with st.popover(f"@{user.username}", use_container_width=True):
                st.markdown(f"**{user.name}**")
                st.caption(f"{user.faculty} • {user.karma_points} Makara Karma")
                st.divider()
                if st.button("Keluar", use_container_width=True):
                    st.session_state["current_user"] = None
                    st.rerun()

    menu = st.segmented_control(
        "Menu",
        ["Radar Barang", "Lapor", "Klaim Barang", "Cari KTM & Statistik"],
        default="Radar Barang",
        label_visibility="collapsed",
    )
    st.divider()
    return menu or "Radar Barang"


def main():
    load_css()

    if st.session_state.get("show_sso_page"):
        render_sso_page()
        return

    menu = render_navbar()

    if menu == "Radar Barang":
        render_feed_page(st.session_state.get("current_user"))
    elif menu == "Lapor":
        st.header("Lapor Barang")
        st.write("Form belum dibuat.")
    elif menu == "Klaim Barang":
        st.subheader("Klaim barang anda")
        st.write("Belum ada klaim.")
    elif menu == "Cari KTM & Statistik":
        st.header("Cari KTM & Statistik")
        st.write("Belum ada data.")


if __name__ == "__main__":
    main()