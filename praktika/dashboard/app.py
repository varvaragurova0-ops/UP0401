import os
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Магазин игрушек — Аналитика",
    page_icon="🧸",
    layout="wide",
)
st.title("🧸 Магазин игрушек — Панель руководителя")

# === БОКОВАЯ ПАНЕЛЬ ===
with st.sidebar:
    st.header("⚙️ Фильтры")
    days = st.selectbox(
        "Период", [7, 30, 90, 365], index=1,
        format_func=lambda x: f"{x} дней",
    )
    if st.button("🔄 Обновить"):
        st.cache_data.clear()
        st.rerun()

    st.divider()
    st.subheader("🔑 Авторизация")
    username = st.text_input("Логин")
    password = st.text_input("Пароль", type="password")
    if st.button("Войти") and username and password:
        r = requests.post(
            f"{API_URL}/api/auth/login/",
            json={"username": username, "password": password},
        )
        if r.status_code == 200:
            st.session_state["token"] = r.json()["access"]
            st.success("Успешный вход")
        else:
            st.error("Неверный логин или пароль")


def auth_headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


# === ФУНКЦИИ ЗАГРУЗКИ ===
@st.cache_data(ttl=60)
def load_kpi(days, token):
    r = requests.get(
        f"{API_URL}/api/reports/kpi/",
        params={"days": days},
        headers={"Authorization": f"Bearer {token}"},
    )
    return r.json()


@st.cache_data(ttl=60)
def load_revenue(days, token):
    r = requests.get(
        f"{API_URL}/api/reports/revenue/",
        params={"days": days},
        headers={"Authorization": f"Bearer {token}"},
    )
    return pd.DataFrame(r.json())


@st.cache_data(ttl=60)
def load_top_toys(token):
    r = requests.get(
        f"{API_URL}/api/reports/top-toys/",
        headers={"Authorization": f"Bearer {token}"},
    )
    return pd.DataFrame(r.json())


@st.cache_data(ttl=60)
def load_manager_load(days, token):
    r = requests.get(
        f"{API_URL}/api/reports/manager-load/",
        params={"days": days},
        headers={"Authorization": f"Bearer {token}"},
    )
    return pd.DataFrame(r.json())


@st.cache_data(ttl=60)
def load_stock(token):
    r = requests.get(
        f"{API_URL}/api/reports/stock/",
        headers={"Authorization": f"Bearer {token}"},
    )
    return pd.DataFrame(r.json())


token = st.session_state.get("token")
if not token:
    st.warning("Войдите в систему через боковую панель, чтобы увидеть данные")
    st.stop()

# === KPI-ПЛИТКИ ===
kpi = load_kpi(days, token)
c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Выручка, ₽", f"{kpi['revenue']:,.0f}")
c2.metric("📦 Продаж", kpi["sales_count"])
c3.metric("🧾 Средний чек, ₽", f"{kpi['avg_check']:,.0f}")
c4.metric("🏬 В наличии", kpi["in_stock"])

# === ГРАФИК ВЫРУЧКИ ===
st.header("📈 Динамика выручки")
revenue_df = load_revenue(days, token)
if not revenue_df.empty:
    fig = px.line(revenue_df, x="date", y="total", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# === 2 КОЛОНКИ ===
col1, col2 = st.columns(2)

with col1:
    st.header("🏆 Топ-5 игрушек")
    top = load_top_toys(token)
    if not top.empty:
        fig = px.bar(top, x="count", y="toy", color="brand", orientation="h")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("👥 Загрузка менеджеров")
    managers = load_manager_load(days, token)
    if not managers.empty:
        fig = px.pie(managers, values="orders", names="manager")
        st.plotly_chart(fig, use_container_width=True)

# === СКЛАД ===
st.header("🏬 Состояние склада")
stock = load_stock(token)
if not stock.empty:
    fig = px.pie(
        stock, values="count", names="status",
        color_discrete_map={
            "available": "green",
            "out_of_stock": "orange",
            "discontinued": "red",
        },
    )
    st.plotly_chart(fig, use_container_width=True)