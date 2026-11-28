import base64
import hashlib
from pathlib import Path
import streamlit as st

from models.constants import UI_FACULTIES
from models.user import User
from storage.json_storage import load_users, save_users


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _get_logo_base64() -> str:
    logo_path = Path("assets/logo_ui.png")
    if not logo_path.exists():
        return ""
    return base64.b64encode(logo_path.read_bytes()).decode("utf-8")


def _inject_sso_css():
    st.markdown(
        """
        <style>
        .stApp { background-color: #F3F4F6 !important; }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #F5F5F5 !important;
            border: 1px solid #D1D5DB !important;
            border-radius: 6px !important;
            padding: 0 !important;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }
        .sso-header {
            background-color: #E6E7E9;
            border-bottom: 1px solid #D1D5DB;
            padding: 18px 26px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: -16px -16px 18px -16px;
        }
        .sso-title {
            font-size: 42px;
            font-weight: 400;
            color: #5F6368;
            line-height: 1;
            margin: 0;
        }
        .sso-sub {
            font-size: 13px;
            color: #6B7280;
            margin-top: 4px;
        }
        .sso-logo img {
            height: 52px;
            object-fit: contain;
        }
        .sso-prompt {
            color: #6B7280;
            font-size: 14px;
            margin-bottom: 12px;
            line-height: 1.4;
        }
        /* TOMBOL SSO UI*/
        div[data-testid="stFormSubmitButton"] button {
            background-color: #3B82C4 !important;
            color: #FFFFFF !important;
            border: 1px solid #2E6DA4 !important;
            border-radius: 5px !important;
            font-weight: 500 !important;
        }
        div[data-testid="stFormSubmitButton"] button:hover {
            background-color: #2E6DA4 !important;
        }
        .sso-footer {
            text-align: center;
            color: #3B82C4;
            font-size: 13px;
            margin-top: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sso_page():
    _inject_sso_css()

    if "sso_mode" not in st.session_state:
        st.session_state["sso_mode"] = "login"

    _, col_center, _ = st.columns([1.2, 1.6, 1.2])
    with col_center:
        if st.button("← Kembali ke TEMU.UI"):
            st.session_state["show_sso_page"] = False
            st.rerun()

        with st.container(border=True):
            logo_b64 = _get_logo_base64()
            logo_html = (
                f'<img src="data:image/png;base64,{logo_b64}" alt="UI Logo" />'
                if logo_b64
                else '<div style="text-align:right;font-weight:600;color:#111;">UNIVERSITAS<br>INDONESIA</div>'
            )
            st.markdown(
                f"""
                <div class="sso-header">
                    <div>
                        <div class="sso-title">SSO</div>
                        <div class="sso-sub">Single Sign On</div>
                    </div>
                    <div class="sso-logo">{logo_html}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.session_state["sso_mode"] == "login":
                st.markdown(
                    '<div class="sso-prompt">Masukkan username dan password UI Anda/<br>'
                    "<i>Enter your username and password:</i></div>",
                    unsafe_allow_html=True,
                )
                with st.form("cas_login_form", border=False):
                    username = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
                    password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")

                    _, col_btn = st.columns([2.2, 1])
                    with col_btn:
                        submitted = st.form_submit_button("Login", use_container_width=True)

                    if submitted:
                        uname = username.strip().lower()
                        pw_hash = hash_password(password)
                        matched = next(
                            (u for u in load_users() if u.username == uname and u.password_hash == pw_hash),
                            None,
                        )
                        if matched:
                            st.session_state["current_user"] = matched
                            st.session_state["show_sso_page"] = False
                            st.rerun()
                        else:
                            st.error("Username atau password salah.")

                st.divider()
                _, col_reg, _ = st.columns([0.5, 2, 0.5])
                with col_reg:
                    if st.button("Daftar Akun", use_container_width=True):
                        st.session_state["sso_mode"] = "register"
                        st.rerun()
                st.markdown(
                    '<div class="sso-footer">Bantuan (<i>Help</i>) • TEMU.UI</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="sso-prompt">Buat akun<br>',
                    unsafe_allow_html=True,
                )
                with st.form("cas_register_form", border=False):
                    new_user = st.text_input("Username", placeholder="Username baru (tanpa spasi)", label_visibility="collapsed")
                    new_pass = st.text_input("Password", type="password", placeholder="Password (min. 4 karakter)", label_visibility="collapsed")
                    name = st.text_input("Nama", placeholder="Nama Lengkap", label_visibility="collapsed")
                    faculty = st.selectbox("Fakultas / Unit", UI_FACULTIES)

                    _, col_btn = st.columns([1.8, 1.2])
                    with col_btn:
                        reg_submit = st.form_submit_button("Daftar", use_container_width=True)

                    if reg_submit:
                        uname = new_user.strip().lower()
                        users = load_users()
                        if not uname or " " in uname or len(new_pass) < 4 or not name.strip():
                            st.error("Username tanpa spasi, password min. 4 karakter, dan nama wajib diisi.")
                        elif any(u.username == uname for u in users):
                            st.error("Username sudah digunakan.")
                        else:
                            users.append(
                                User(
                                    username=uname,
                                    password_hash=hash_password(new_pass),
                                    name=name.strip(),
                                    faculty=faculty,
                                )
                            )
                            save_users(users)
                            st.session_state["sso_mode"] = "login"
                            st.success("Akun telah dibuat! Silakan login.")
                            st.rerun()

                st.divider()
                if st.button("Sudah punya akun? Login", use_container_width=True):
                    st.session_state["sso_mode"] = "login"
                    st.rerun()