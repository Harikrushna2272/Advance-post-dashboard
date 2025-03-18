import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv('dataset.csv')

st.set_page_config(page_title="Reddit Post Dashboard", layout="wide")

st.markdown("""
    <style>
        /* Background and Font Styling */
        body {
            background-color: #f4f4f9; /* Light gray background for professional feel */
            font-family: 'Arial', sans-serif;
            color: #333333; /* Professional dark gray */
        }

        /* Container Styling (Glassmorphism + Gradient) */
        .container {
            background: linear-gradient(135deg, #4b0082, #8a2be2); /* Deep Purple to Blue Gradient */
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.2); /* Softer shadow for depth */
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 20px;
            border: 1px solid #6a0dad; /* Dark Purple Border */
        }

        /* Hover Effect */
        .container:hover {
            transform: translateY(-5px);
            box-shadow: 0px 12px 24px rgba(138, 43, 226, 0.4); /* Subtle purple glow */
            border-color: #8a2be2;
        }

        /* Post Title Styling */
        .post-title {
            font-size: 22px;
            font-weight: bold;
            color: #ffffff; /* White for contrast */
            text-decoration: none;
            transition: color 0.2s ease;
            margin-bottom: 8px;
            display: inline-block;
        }

        /* Hover Effect for Post Title */
        .post-title:hover {
            color: #0000FF; /* Gold on hover for elegance */
            transform: scale(1.03);
        }

        /* Post Content Styling */
        .post-content {
            font-size: 16px;
            color: #e0e0e0; /* Light gray for better readability */
            margin-top: 10px;
            line-height: 1.6;
        }

        /* Heading Styling */
        h1 {
            color: #4b0082 !important; /* Deep Purple for Professional Feel */
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        }

        /* Instructions Styling */
        .instructions {
            font-size: 16px;
            color: #555555;
            margin-top: 20px;
            text-align: center;
            letter-spacing: 0.5px;
        }

        /* Footer Styling */
        .footer {
            font-size: 14px;
            color: #777777;
            margin-top: 40px;
            text-align: center;
            padding-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)




# Title Section
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>📢 Reddit Post Overview</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Display posts in a more structured card layout
for index, row in df.iterrows():
    with st.container():
        st.markdown(f"""
            <div class="container">
                <a href="/dashboard?id={row['id']}" class="post-title">{row['title']}</a>
                <div class="post-content">{str(row.get('selftext', ''))[:200]}...</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='instructions'>🔗 <b>Click on the post title to view full details.</b></div>", unsafe_allow_html=True)

