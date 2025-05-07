"""
Metrics-related functionality for the Streamlit app.
"""
import streamlit as st
import json

from frontend.utils.api import call_llm_api, get_llm_data
from frontend.config import LLM_URL


def load_metrics():
    """Load and display available metrics with direct access buttons."""
    try:
        with st.spinner('Loading metrics...'):
            response = get_llm_data("metrics")

            if response and response.status_code == 200:
                result = response.json()
                metrics = result.get("metrics", [])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Here are all available metrics:",
                    "metrics": metrics
                })

                return True
            else:
                st.error(f"Failed to load metrics ({response.status_code})")
                if response and response.text:
                    st.error(response.text)
                return False
    except Exception as e:
        st.error(f"Error loading metrics: {str(e)}")
        return False


def show_metric_details(metric_name: str):
    """Display detailed information about a specific metric."""
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Fetching details for metric '{metric_name}'..."
    })

    response = call_llm_api("query", {
        "query": f"Get details for metric: {metric_name}",
        "chat_history": []
    })

    if response and response.status_code == 200:
        result = response.json()
        details = extract_tool_output(result, "get_metric_details")

        if details:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Details for metric '{metric_name}':",
                "metric_details": details,
                "show_comprehensive": True
            })
            return True
        else:
            st.warning(f"No details found for metric: {metric_name}")
            return False
    else:
        st.error(f"Failed to get metric details ({response.status_code})")
        return False


def show_domain_metrics(domain_name: str):
    """Display all metrics in a specific domain."""
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Fetching metrics for domain '{domain_name}'..."
    })

    domain_response = call_llm_api("query", {
        "query": f"Get details for domain: {domain_name}",
        "chat_history": []
    })

    metrics_response = call_llm_api("query", {
        "query": f"List all metrics in domain: {domain_name}",
        "chat_history": []
    })

    metrics = extract_tool_output(metrics_response.json(), "get_domain_metrics") if metrics_response else []
    domain_details = extract_tool_output(domain_response.json(), "get_domain_details") if domain_response else None

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Information for domain '{domain_name}':",
        "domain_metrics": metrics,
        "domain_details": domain_details,
        "show_comprehensive": True
    })
    return True


def show_dashboard_metrics(dashboard_name: str):
    """Display all metrics in a specific dashboard."""
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Fetching metrics for dashboard '{dashboard_name}'..."
    })

    dashboard_response = call_llm_api("query", {
        "query": f"Get details for dashboard: {dashboard_name}",
        "chat_history": []
    })

    metrics_response = call_llm_api("query", {
        "query": f"List all metrics in dashboard: {dashboard_name}",
        "chat_history": []
    })

    metrics = extract_tool_output(metrics_response.json(), "get_dashboard_metrics") if metrics_response else []
    dashboard_details = extract_tool_output(dashboard_response.json(), "get_dashboard_details") if dashboard_response else None

    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Information for dashboard '{dashboard_name}':",
        "dashboard_metrics": metrics,
        "dashboard_details": dashboard_details,
        "show_comprehensive": True
    })
    return True


def search_metrics(query: str):
    """Search for metrics that match the query."""
    clean_old_search_results()

    response = get_llm_data("metrics")
    if response and response.status_code == 200:
        result = response.json()
        all_metrics = result.get("metrics", [])
        matching = [m for m in all_metrics if query.lower() in m.lower()]

        if matching:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Found {len(matching)} metrics matching '{query}':",
                "matching_metrics": matching
            })
            return True
        else:
            st.warning(f"No metrics found matching '{query}'")
            return False
    else:
        st.error(f"Failed to search metrics ({response.status_code})")
        return False


def search_domains(query: str):
    """Search for domains that match the query."""
    clean_old_search_results()

    response = get_llm_data("domains")
    if response and response.status_code == 200:
        result = response.json()
        all_domains = result.get("domains", [])
        matching = [d for d in all_domains if query.lower() in d.lower()]

        if matching:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Found {len(matching)} domains matching '{query}':",
                "matching_domains": matching
            })
            return True
        else:
            st.warning(f"No domains found matching '{query}'")
            return False
    else:
        st.error(f"Failed to search domains ({response.status_code})")
        return False


def search_dashboards(query: str):
    """Search for dashboards that match the query."""
    clean_old_search_results()

    response = get_llm_data("dashboards")
    if response and response.status_code == 200:
        result = response.json()
        all_dashboards = result.get("dashboards", [])
        matching = [d for d in all_dashboards if query.lower() in d.lower()]

        if matching:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Found {len(matching)} dashboards matching '{query}':",
                "matching_dashboards": matching
            })
            return True
        else:
            st.warning(f"No dashboards found matching '{query}'")
            return False
    else:
        st.error(f"Failed to search dashboards ({response.status_code})")
        return False


def clean_old_search_results():
    """Remove previous search result messages from chat history."""
    st.session_state.messages = [
        msg for msg in st.session_state.messages
        if not (msg["role"] == "assistant" and "matching" in msg.get("content", ""))
    ]


def extract_tool_output(result_json, tool_name):
    """Extract tool output from a tool_usage step."""
    if not result_json or "tool_usage" not in result_json:
        return None

    for step in result_json["tool_usage"]:
        if step["tool_name"] == tool_name:
            try:
                return json.loads(step["tool_output"])
            except Exception:
                continue
    return None
