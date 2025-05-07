import json
from datetime import datetime
import streamlit as st

from frontend.utils.api import call_llm_api
from frontend.config import LLM_URL


def display_tool_usage(tool_usage):
    """Display the step-by-step analysis of tool usage."""
    with st.expander("🔍 See how I got this answer", expanded=False):
        for idx, step in enumerate(tool_usage, 1):
            st.markdown(f"#### Step {idx}: Using {step['tool_name']}")
            st.markdown("**🤔 Agent's Thought:**")
            st.markdown(f"```\n{step['thought']}\n```")
            st.markdown("**🛠️ Tool Called:**")
            st.markdown(f"- **Tool:** `{step['tool_name']}`")
            st.markdown(f"- **Input:** `{json.dumps(step['tool_input'], indent=2)}`")
            st.markdown("**📝 Tool Response:**")
            st.markdown(f"```\n{step['tool_output']}\n```")
            if idx < len(tool_usage):
                st.markdown("---")


def display_chat_message(role, content, tool_usage=None):
    """Display a chat message in a WhatsApp-like style."""
    with st.container():
        if role == "user":
            st.markdown(
                f"""
                <div style='
                    display: flex;
                    justify-content: flex-end;
                    margin: 0.5rem 0;
                '>
                    <div style='
                        background-color: #005C4B;
                        color: white;
                        padding: 0.75rem 1rem;
                        border-radius: 8px;
                        border-top-right-radius: 2px;
                        max-width: 70%;
                        box-shadow: 0 1px 0.5px rgba(0,0,0,0.13);
                        word-wrap: break-word;
                        position: relative;
                    '>
                        {content}
                        <div style='
                            font-size: 0.7rem;
                            color: rgba(255,255,255,0.6);
                            text-align: right;
                            margin-top: 0.3rem;
                            margin-bottom: -0.2rem;
                        '>
                            {datetime.now().strftime('%H:%M')}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='
                    display: flex;
                    justify-content: flex-start;
                    margin: 0.5rem 0;
                '>
                    <div style='
                        background-color: #202C33;
                        color: white;
                        padding: 0.75rem 1rem;
                        border-radius: 8px;
                        border-top-left-radius: 2px;
                        max-width: 70%;
                        box-shadow: 0 1px 0.5px rgba(0,0,0,0.13);
                        word-wrap: break-word;
                        position: relative;
                    '>
                        {content}
                        <div style='
                            font-size: 0.7rem;
                            color: rgba(255,255,255,0.6);
                            text-align: left;
                            margin-top: 0.3rem;
                            margin-bottom: -0.2rem;
                        '>
                            {datetime.now().strftime('%H:%M')}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if tool_usage:
                display_tool_usage(tool_usage)


def process_query(user_query):
    """Process a user query and return the response."""
    try:
        st.info("🔌 Connecting to LLM service...")

        response = call_llm_api("query", {
            "query": user_query,
            "context": {
                "chat_history": get_chat_history(),
                "current_time": datetime.now().isoformat()
            }
        })

        if response and response.status_code == 200:
            result = response.json()

            st.info("🧠 Processing response...")

            st.session_state.messages.append({
                "role": "assistant",
                "content": result["final_response"],
                "tool_usage": result.get("tool_usage", []),
                "timestamp": datetime.now().isoformat(),
                "type": "text"
            })

            return True
        else:
            error_msg = "❌ Failed to get response."
            if response is not None and response.text:
                error_msg += f"\nDetails: {response.text}"
            st.error(error_msg)
            return False
    except Exception as e:
        st.error(f"❌ Error making request: {str(e)}")
        return False


def clear_chat_history():
    """Clear the chat history."""
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you with metrics today?"}]


def get_chat_history():
    """Get the formatted chat history."""
    return [
        {
            "role": msg["role"],
            "content": msg["content"]
        }
        for msg in st.session_state.messages
    ]
