"""
Main Streamlit application for the Insights app.
"""
import streamlit as st
import requests
import json
import time
from frontend.chat.core import process_query, clear_chat_history
from frontend.metrics.core import (
    load_metrics, show_metric_details, show_domain_metrics,
    show_dashboard_metrics, search_metrics, search_domains, search_dashboards
)



# Configure the page
st.set_page_config(
    page_title="Insights App",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you with metrics today?"}]

# Function to remove old results when showing details
def remove_old_results(result_type: str):
    st.session_state.messages = [msg for msg in st.session_state.messages 
                               if not (msg["role"] == "assistant" and 
                                     (f"Fetching {result_type}" in msg["content"] or
                                      f"Details for {result_type}" in msg["content"] or
                                      f"Metrics in {result_type}" in msg["content"]))]

# Create a two-column layout
col1, col2 = st.columns([0.85, 0.15])

# Main chat area
with col1:
    # Display chat messages
    messages_container = st.container()
    with messages_container:
        for message_idx, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Display metrics if present
                if "metrics" in message:
                    st.markdown("#### Available Metrics:")
                    cols = st.columns(3)
                    for idx, metric in enumerate(message["metrics"]):
                        col = cols[idx % 3]
                        with col:
                            button_key = f"metric_{metric}_{message_idx}"
                            if st.button(f"🔍 {metric}", key=button_key):
                                remove_old_results("metric")
                                show_metric_details(metric)
                                st.rerun()
                
                # Display metric details if present
                if "metric_details" in message:
                    details = message["metric_details"]
                    st.markdown("#### Metric Details:")
                    st.markdown(f"**Name:** {details.get('name', 'N/A')}")
                    st.markdown(f"**Description:** {details.get('description', 'N/A')}")
                    st.markdown(f"**Owner:** {details.get('owner', 'N/A')}")
                    if details.get('owner_email'):
                        st.markdown(f"**Owner Email:** {details.get('owner_email', 'N/A')}")
                    st.markdown(f"**Domain:** {details.get('domain', 'N/A')}")
                    st.markdown(f"**Data Source:** {details.get('data_source', 'N/A')}")
                    
                    # Show related metrics if available
                    if message.get("show_comprehensive"):
                        st.markdown("---")
                        st.markdown("#### Related Metrics:")
                        if "related_metrics" in details:
                            cols = st.columns(3)
                            for idx, metric in enumerate(details["related_metrics"]):
                                col = cols[idx % 3]
                                with col:
                                    button_key = f"related_metric_{metric}_{message_idx}"
                                    if st.button(f"🔍 {metric}", key=button_key):
                                        remove_old_results("metric")
                                        show_metric_details(metric)
                                        st.rerun()
                
                # Display domain metrics if present
                if "domain_metrics" in message:
                    if message.get("show_comprehensive"):
                        st.markdown("#### Domain Information:")
                        if "domain_details" in message and message["domain_details"]:
                            details = message["domain_details"]
                            st.markdown(f"**Name:** {details.get('name', 'N/A')}")
                            st.markdown(f"**Description:** {details.get('description', 'N/A')}")
                            st.markdown(f"**Owner:** {details.get('owner', 'N/A')}")
                            if details.get('owner_email'):
                                st.markdown(f"**Owner Email:** {details.get('owner_email', 'N/A')}")
                        st.markdown("---")
                    
                    st.markdown("#### Metrics in this domain:")
                    cols = st.columns(3)
                    for idx, metric in enumerate(message["domain_metrics"]):
                        col = cols[idx % 3]
                        with col:
                            button_key = f"domain_metric_{metric}_{message_idx}"
                            if st.button(f"🔍 {metric}", key=button_key):
                                remove_old_results("metric")
                                show_metric_details(metric)
                                st.rerun()
                
                # Display dashboard metrics if present
                if "dashboard_metrics" in message:
                    if message.get("show_comprehensive"):
                        st.markdown("#### Dashboard Information:")
                        if "dashboard_details" in message and message["dashboard_details"]:
                            details = message["dashboard_details"]
                            st.markdown(f"**Name:** {details.get('name', 'N/A')}")
                            st.markdown(f"**Description:** {details.get('description', 'N/A')}")
                            st.markdown(f"**Owner:** {details.get('owner', 'N/A')}")
                            if details.get('owner_email'):
                                st.markdown(f"**Owner Email:** {details.get('owner_email', 'N/A')}")
                            st.markdown(f"**Last Updated:** {details.get('last_updated', 'N/A')}")
                        st.markdown("---")
                    
                    st.markdown("#### Metrics in this dashboard:")
                    cols = st.columns(3)
                    for idx, metric in enumerate(message["dashboard_metrics"]):
                        col = cols[idx % 3]
                        with col:
                            button_key = f"dashboard_metric_{metric}_{message_idx}"
                            if st.button(f"🔍 {metric}", key=button_key):
                                remove_old_results("metric")
                                show_metric_details(metric)
                                st.rerun()
                
                if message.get("tool_usage"):
                    with st.expander("🔍 See how I got this answer", expanded=False):
                        for idx, step in enumerate(message["tool_usage"], 1):
                            st.markdown(f"**Step {idx}: Using {step['tool_name']}**")
                            st.markdown("🤔 **Thought:**")
                            st.markdown(f"```\n{step['thought']}\n```")
                            st.markdown("🛠️ **Tool Called:**")
                            st.markdown(f"- Tool: `{step['tool_name']}`")
                            st.markdown(f"- Input: `{json.dumps(step['tool_input'], indent=2)}`")
                            st.markdown("📝 **Response:**")
                            st.markdown(f"```\n{step['tool_output']}\n```")
                            if idx < len(message["tool_usage"]):
                                st.markdown("---")

    # Status area for showing processing steps
    status_container = st.empty()

    # Chat input
    if prompt := st.chat_input("Ask something about the metrics..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process the query with visible status updates
        with st.chat_message("assistant"):
            with status_container.container():
                st.info("🔄 Processing your query...")
                try:
                    with st.spinner("🤔 Thinking..."):
                        success = process_query(prompt)
                        if success:
                            st.success("✅ Response generated successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to process query. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error processing query: {str(e)}")

# Tools panel - Simplified to only show clear chat button
with col2:
    st.markdown("### 🛠️ Quick Actions")
    if st.button("🔄 Clear Chat", use_container_width=True, help="Clear the current chat history"):
        clear_chat_history()
        st.rerun() 