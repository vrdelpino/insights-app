import requests
import streamlit as st
from frontend.config import LLM_URL

def call_llm_api(endpoint: str, payload: dict):
    try:
        return requests.post(f"{LLM_URL}/{endpoint}", json=payload, timeout=60)
    except requests.RequestException as e:
        st.error(f"❌ POST {endpoint} failed: {e}")
        return None

def get_llm_data(path: str):
    try:
        return requests.get(f"{LLM_URL}/{path}", timeout=30)
    except requests.RequestException as e:
        st.error(f"❌ GET {path} failed: {e}")
        return None
