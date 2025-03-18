import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter
from nltk.corpus import stopwords
import nltk
import sys
import os
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from chatbot import chunk_text, get_top_chunks, generate_gemini_response
from chatbot import evaluate_reliability_for_post


df = pd.read_csv('dataset.csv')

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

query_params = st.query_params
post_id = query_params.get("id", None)

if post_id:
    post = df[df['id'] == post_id].iloc[0]

    st.title(post['title'])
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    col1.write(f"👤 Author : {post['author']}")
    col2.write(f"📅 Created On: {post['created_datetime']}")
    col3.write(f"🏡 Subreddit : {post['subreddit']}")
    st.write("---")


    col1, col2 = st.columns(2)

    #LEFT COLUMN: Display Content
    with col1:
        st.subheader("📝 Content of Post"); st.write(f"**Sentiment:** {post['sentiment']}" if 'sentiment' in post and pd.notna(post['sentiment']) else "No sentiment available")

    #RIGHT COLUMN: Display Sentiment (if available)

    # Selftext Below
    st.write(post['selftext'])


    st.write("---")

    # Reliability Section SECTION :
    st.subheader("🧠 Source Reliability")
    if post_id:
        with st.spinner("Evaluating reliability..."):
            reliability_score, reliability_status, explanation, summary = evaluate_reliability_for_post(post_id)
        if reliability_score is not None:
            st.write(f"**Status:** {reliability_status}")
            st.progress(reliability_score / 100)
            st.write(f"**Score:** {reliability_score}/100")
            st.write(f"{explanation}")
        else:
            st.write("Could not determine reliability.")

    st.write("---")

    # Engagement Metrics SECTION :
    st.subheader("📊 Engagement Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    likes = 0 if pd.isna(post['likes']) else post['likes']
    comments = 0 if pd.isna(post['num_comments']) else post['num_comments']
    views = 0 if pd.isna(post['view_count']) else post['view_count']
    reward = 0 if pd.isna(post['num_awarders']) else post['num_awarders']
    score = 0 if pd.isna(post['score']) else post['score']

    col1.metric("👍 Likes", likes)
    col2.metric("💬 Comments", comments)
    col3.metric("👀 Views", views)
    col4.metric("🏆 Awarders", reward)
    col5.metric("🏅 Post Score", score)
    st.write("---")

   
    col1, col2 = st.columns(2)
    # LEFT COLUMN: TIME-SERIES VISUALIZATION SECTION :
    
    st.subheader(f"📈 Post Activity of {post['subreddit']}")

    subreddit_data = df[df['subreddit'] == post['subreddit']].copy()

    subreddit_data['created_datetime'] = pd.to_datetime(subreddit_data['created_datetime'], errors='coerce')
    subreddit_data = subreddit_data.dropna(subset=['created_datetime'])

    if not subreddit_data.empty:
        post_count = subreddit_data.set_index('created_datetime').resample('D').size()

        if not post_count.empty:
            fig = px.line(
                x=post_count.index,
                y=post_count.values,
                labels={'x': 'Date', 'y': 'Number of Posts'},
                title=f"Number of Posts done by {post['subreddit']} Over Time"
            )
            fig.update_traces(mode='lines+markers', line_color='#636EFA')
            fig.update_layout(
                xaxis_title='Date',
                yaxis_title='Number of Posts',
                template='plotly_dark'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(
            """
            
            - This chart shows the posting activity related to subreddit over time. It helps track the frequency and consistency of posts within this category. Analyzing this data can reveal trends, engagement patterns, and peak activity periods. Identifying such insights can guide content strategies and community engagement efforts.
            """
            )
        else:
            st.warning(f"No post activity found for {post['subreddit']}.")
    else:
        st.warning(f"No post data found for {post['subreddit']}.")

    # RIGHT COLUMN: TOP-PERFORMING POSTS BY SCORE SECTION :
    st.write("---")

    # BAR CHART: TOP 10 POSTS BY SCORE WITH AUTHORS SECTION :
    st.subheader("📊 Top-Performing Posts by Score (With Authors)")

    top_10_posts = df[['author', 'score']].nlargest(10, 'score')
    
    if not top_10_posts.empty:
        fig = px.bar(
            top_10_posts,
            x='score',
            y='author',
            orientation='h',
            title="Top 10 Posts by Score",
            labels={'score': 'Score', 'author': 'Author'},
            color='score',  
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            xaxis_title='Score',
            yaxis_title='Author',
            template='plotly_dark',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            """
            - This chart highlights the highest-scoring posts along with their authors. It helps identify the most impactful content and the contributors driving engagement. High scores often reflect strong user interaction, relevance, and quality of content. Understanding this can encourage more targeted and engaging content creation.
            """
        )
    else:
        st.warning("No top-performing posts available for visualization.")

    st.write("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌍 Top 5 Subreddit by Post")
        
        top_subreddits = df['subreddit'].value_counts().head(5).reset_index()
        top_subreddits.columns = ['subreddit', 'post_count']

        fig = px.pie(
            top_subreddits,
            values='post_count',
            names='subreddit',
            title='Top 5 Subreddits Contributing to Posts',
            color_discrete_sequence=px.colors.qualitative.Set3,
            hover_data=['post_count']
        )
        
        fig.update_traces(textinfo='percent+label', pull=[0.1] * 5)
        fig.update_layout(height=400, width=400, showlegend=True)

        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            """
            - This pie chart shows the top 5 subreddits contributing the most posts. It helps to quickly identify which subreddits are most active and influential in terms of post volume. Larger slices represent subreddits with more posts, giving a clear picture of where most of the activity is happening.
            """
        )

    with col2:
        st.subheader("👥 Top 5 Authors by Post")

        top_authors = df['author'].value_counts().head(5).reset_index()
        top_authors.columns = ['author', 'post_count']

        fig = px.pie(
            top_authors,
            values='post_count',
            names='author',
            title='Top 5 Authors Contributing to Posts',
            color_discrete_sequence=px.colors.qualitative.Set2,
            hover_data=['post_count']
        )
        
        fig.update_traces(textinfo='percent+label', pull=[0.1] * 5)
        fig.update_layout(height=400, width=400, showlegend=True)

        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            """
            - This pie chart highlights the top 5 authors who have made the most posts. It helps identify the most active contributors within the community. A larger slice means that the author has posted more frequently, showing their influence and engagement level.
            """
        )

    st.write("---")

    # WORD CLOUD FOR CURRENT POST section :
    st.subheader("🌥️ Trending Topics")

    def preprocess_text(text):
        text = re.sub(r'\W', ' ', text)  # Remove special characters
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespaces
        text = text.lower()  # Convert to lowercase
        tokens = text.split()
        tokens = [word for word in tokens if word not in stop_words]
        return tokens

    if not pd.isna(post['title']) or not pd.isna(post['selftext']):
        title_text = post['title'] if not pd.isna(post['title']) else ''
        selftext_text = post['selftext'] if not pd.isna(post['selftext']) else ''
        
        combined_text = f"{title_text} {selftext_text}"
        current_post_tokens = preprocess_text(combined_text)

        if current_post_tokens:
            current_post_text = ' '.join(current_post_tokens)

            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='black',
                colormap='plasma',
                max_words=100,
                contour_width=1,
                contour_color='steelblue'
            ).generate(current_post_text)

            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
            st.markdown(
                """
                - This section highlights the most frequently mentioned words in the current post using a word cloud. Larger words indicate higher frequency, showing which topics or terms are most relevant to the post. This helps quickly identify the key themes and focus areas of the post at a glance. The word cloud visually represents the core message and trending subjects in an engaging format.
                """
            )
        else:
            st.warning("Not enough text data to generate a word cloud.")
    else:
        st.warning("No text available for this post.")



    st.write("---")

    # Summary Section :
    st.subheader("📋 Summary of the Post")
    with st.expander("📋 **Summary of the Post**", expanded=True):
        if summary and summary != "No summary available.":
            st.markdown(f"**Summary:** {summary}")
        else:
            st.markdown("*No summary available.*")

    st.write("---")
    
    # Chat Section :
    st.subheader("💬 Ask a Question About This Post")

    user_query = st.text_input("Type your question here:")

    if user_query:
        with st.spinner("🤖 Thinking..."):
            response = generate_gemini_response(user_query)

        st.subheader("🤖 Answer")
        st.write(response)


else:
    st.write("No post selected. Please go back to the home page.")

