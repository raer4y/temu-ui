import streamlit as st

st.set_page_config(
    page_title="TEMU.UI | Lost & Found",
    page_icon="👀",
    layout="wide",
)

def main():
    st.title("TEMU.UI")
    st.caption("Platform Lost & Found Universitas Indonesia")
    st.divider()
    st.info("Selamat datang di TEMU.UI!")

if __name__ == "__main__":
    main()