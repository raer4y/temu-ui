import streamlit as st
from pathlib import Path
from ui.feed_page import render_feed_page

st.set_page_config(
    page_title="TEMU.UI | Lost & Found",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css():
    css_path = Path("assets/style.css")
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding="utf-8")}</style>",
unsafe_allow_html=True)

def render_navbar():
    col_brand, col_auth = st.columns([4, 1], vertical_alignment="center")
    with col_brand:
        st.markdown("### TEMU.UI")
        st.caption("Lost & Found Universitas Indonesia")
    with col_auth:
        with st.popover("Masuk", use_container_width=True):
            st.write("Login Coming soon!")

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