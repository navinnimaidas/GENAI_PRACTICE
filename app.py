import streamlit as st
import pandas as pd
import plotly.express as px
import asyncio
from main import Botendpoint

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="SQL GPT Bot",
    page_icon="🤖",
    layout="wide"
)

# ---------- INIT ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

bot = Botendpoint()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("⚙️ Settings")
    theme = st.selectbox("Theme", ["Light", "Dark"])
    show_chart = st.toggle("Auto Visualizations", True)
    st.markdown("---")
    st.info("💡 Ask natural language questions about your database")

# ---------- HEADER ----------
st.title("🤖 SQL GPT Assistant")
st.caption("Ask questions → Get SQL → See results & insights")

# ---------- CHAT HISTORY ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if isinstance(msg["content"], pd.DataFrame):
            st.dataframe(msg["content"], use_container_width=True)
        else:
            st.markdown(msg["content"])

# ---------- INPUT ----------
user_input = st.chat_input("Ask your data question...")

# ---------- ASYNC RUNNER ----------
async def run_query(query):
    return await bot.get_response(query)

# ---------- HANDLE INPUT ----------
if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Thinking... querying database..."):
            try:
                result = asyncio.run(run_query(user_input))

                # Try parsing into dataframe
                df = None
                if isinstance(result, list):
                    df = pd.DataFrame(result)
                elif isinstance(result, str):
                    try:
                        df = pd.read_json(result)
                    except:
                        pass

                # ---------- DISPLAY ----------
                if df is not None and not df.empty:
                    st.success("✅ Query executed successfully")

                    st.dataframe(df, use_container_width=True)

                    # ---------- VISUALIZATION ----------
                    if show_chart:
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        categorical_cols = df.select_dtypes(include=['object']).columns

                        if len(numeric_cols) > 0 and len(categorical_cols) > 0:
                            st.subheader("📊 Auto Visualization")

                            x_col = categorical_cols[0]
                            y_col = numeric_cols[0]

                            fig = px.bar(
                                df,
                                x=x_col,
                                y=y_col,
                                color=x_col,
                                title=f"{y_col} by {x_col}",
                                template="plotly_dark"
                            )
                            st.plotly_chart(fig, use_container_width=True)

                        elif len(numeric_cols) >= 2:
                            st.subheader("📈 Correlation Scatter")

                            fig = px.scatter(
                                df,
                                x=numeric_cols[0],
                                y=numeric_cols[1],
                                color=numeric_cols[0],
                                size=numeric_cols[1],
                                template="plotly_dark"
                            )
                            st.plotly_chart(fig, use_container_width=True)

                else:
                    st.markdown(result)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": df if df is not None else result
                })

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")