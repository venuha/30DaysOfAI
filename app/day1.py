# Day 1
# Connect to Snowflake

import streamlit as st
import os

st.title(":material/vpn_key: Day 1: Connect to Snowflake")

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()

except Exception:
    # Works locally
    from snowflake.snowpark import Session

    conn = st.secrets["connections"]["snowflake"]

    pk_path = conn["private_key_path"]

    if not os.path.exists(pk_path):
        raise FileNotFoundError(f"Private key not found at {pk_path}")

    with open(pk_path, "rb") as f:
        private_key_bytes = f.read()

    configs = dict(conn)
    configs["private_key"] = private_key_bytes

    # Remove path so Snowpark doesn't get confused
    configs.pop("private_key_path", None)

    session = Session.builder.configs(configs).create()

# Query Snowflake version
version = session.sql("SELECT CURRENT_VERSION()").collect()[0][0]

# Display results
st.success(f"Successfully connected! Snowflake Version: {version}")
