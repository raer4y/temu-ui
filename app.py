import streamlit as st

st.set_page_config(
    page_title="TEMU.UI | Lost & Found",
    layout="wide",
)

def main():
    st.title("TEMU.UI")
    st.caption("Platform Lost & Found Universitas Indonesia")

    with st.sidebar:
        st.header("Navigasi")
        menu = st.radio(
            "Pilih Halaman:",
            [
                "Radar Barang",
                "Lapor",
                "Klaim Barang",
                "Cari KTM & Statistik",
            ],
        )

    if menu == "Radar Barang":
        st.header("Radar Barang")
        st.write("Belum ada data.")
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