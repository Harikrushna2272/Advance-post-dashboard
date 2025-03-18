import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google.generativeai import configure, GenerativeModel
import streamlit as st
import re

GEMINI_API_KEY = "AIzaSyBB1lkfhA7vpgN0egLWWYADVwRBmkT5syc" 
configure(api_key=GEMINI_API_KEY)
model = GenerativeModel('gemini-2.0-flash')

df = pd.read_csv('dataset.csv')

def combine_text(row):
    fields = [
        row.get('title', ''),
        row.get('selftext', ''),
        row.get('selftext_html', ''),
        row.get('scraped_data', '')
    ]
    return ' '.join([str(field) for field in fields if pd.notna(field)])

df['combined_text'] = df.apply(combine_text, axis=1)

# Chunk the combined text
def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# index for RAG
df['chunks'] = df['combined_text'].apply(chunk_text)

#  Match user query Similarity
def get_top_chunks(query, top_n=3):
    all_chunks = []
    index_map = {}

    for i, row in df.iterrows():
        for chunk in row['chunks']:
            all_chunks.append(chunk)
            index_map[chunk] = i

    vectorizer = TfidfVectorizer()
    chunk_vectors = vectorizer.fit_transform(all_chunks)
    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, chunk_vectors).flatten()
    top_indices = np.argsort(similarities)[::-1][:top_n]

    top_chunks = [(all_chunks[i], similarities[i], index_map[all_chunks[i]]) for i in top_indices]
    return top_chunks

def generate_gemini_response(query):
    top_chunks = get_top_chunks(query)

    if not top_chunks:
        return "No relevant information found."

    context = "\n\n".join([chunk[0] for chunk in top_chunks])

    # conversation context
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = ""

    st.session_state.conversation_history += f"User: {query}\n"

    prompt = f"""
    Context:
    {context}

    Conversation History:
    {st.session_state.conversation_history}

    User Query: {query}
    Answer:
    """

    try:
        response = model.generate_content(prompt)
        if response and response.text:
            st.session_state.conversation_history += f"AI: {response.text}\n"
            return response.text
    except Exception as e:
        return f"Error generating response: {e}"

    return "No response generated."

# Reliability of the Source

def evaluate_reliability(post):
    """
    Use Gemini to assess the reliability of a post and generate a reliability score and summary.
    """
    if post is None:
        return None, "Unknown", "No data available for evaluation.", "No summary available."

    prompt = f"""
    Evaluate the reliability of the following Reddit post:

    Title: {post.get('title', '')}
    Selftext: {post.get('selftext', '')}
    Author: {post.get('author', '')}
    Score: {post.get('score', '')}
    Likes: {post.get('likes', '')}
    Comments: {post.get('num_comments', '')}
    View Count: {post.get('view_count', '')}
    Subreddit: {post.get('subreddit', '')}
    Sentiment: {post.get('sentiment', '')}
    Awards: {post.get('num_awarders', '')}
    Hidden: {post.get('hidden', '')}
    Domain: {post.get('domain', '')}
    Contest_mode: {post.get('contest_mode', '')}
    Is_unreliable_domain: {post.get('is_unreliable_domain', '')}
    Over_18: {post.get('over_18', '')}
    Banned_by: {post.get('banned_by', '')}
    Is_crosspostable: {post.get('is_crosspostable', '')}
    Locked: {post.get('locked', '')}
    Scraped_data: {post.get('scraped_data', '')}

    **TASK:**  
    1. Rate the reliability of the source on a scale of 0 to 100.  
    2. State explicitly if the source is "Reliable" or "Unreliable."  
    3. Provide a brief explanation for the rating.  
    4. Generate a concise 2-3 sentence summary of the post content.  

    **Format the output as follows:**  
    - Score: [numeric value from 0 to 100]  
    - Status: [Reliable or Unreliable]  
    - Explanation: [Reason for the rating]  
    - Summary: [3-4 sentence summary of the post content]  
    """

    try:
        response = model.generate_content(prompt)

        if response and response.text:
            output = response.text.strip().split("\n")

            reliability_score = None
            reliability_status = "Unknown"
            explanation = "No explanation provided."
            summary = "No summary available."

            for line in output:
                if "Score:" in line:
                    match = re.search(r'\d+', line)
                    if match:
                        reliability_score = int(match.group())
                if "Status:" in line:
                    if "Reliable" in line:
                        reliability_status = "Reliable"
                    elif "Unreliable" in line:
                        reliability_status = "Unreliable"
                if "Explanation:" in line:
                    explanation = line.replace("Explanation:", "").strip()
                if "Summary:" in line:
                    summary = line.replace("Summary:", "").strip()

            if reliability_score is None:
                reliability_score = 50  
            if reliability_status == "Unknown":
                reliability_status = "Unreliable" if reliability_score < 50 else "Reliable"
            if explanation == "No explanation provided." and len(output) > 0:
                explanation = " ".join(output)
            if summary == "No summary available." and len(output) > 0:
                summary = " ".join(output)

            return reliability_score, reliability_status, explanation, summary

    except Exception as e:
        print(f"⚠️ Error in reliability evaluation: {e}")

    return None, "Unknown", "No explanation provided.", "No summary available."


def evaluate_reliability_for_post(post_id):
    if not post_id:
        return None, "Unknown", "No post ID provided."

    post = df[df['id'] == post_id].iloc[0]

    if post is None:
        return None, "Unknown", "Post not found."

    return evaluate_reliability(post)

# Streamlit App 
if __name__ == "__main__":
    st.title("🤖 Conversational Chatbot with Reliability Check")

    user_query = st.text_input("💬 Ask a question:")

    if user_query:
        with st.spinner("Thinking..."):
            response = generate_gemini_response(user_query)

        if response:
            st.write(f"🤖 **Gemini:** {response}")

    if 'conversation_history' in st.session_state:
        st.subheader("📝 Conversation History")
        st.write(st.session_state.conversation_history)

    st.subheader("🧠 Source Reliability Evaluation")

    post_id = st.session_state.get("post_id", None)

    if post_id:
        with st.spinner("Evaluating reliability..."):
            reliability_score, reliability_status, explanation = evaluate_reliability_for_post(post_id)

        if reliability_score is not None:
            st.write(f"**Status:** {reliability_status}")
            st.progress(reliability_score / 100)
            st.write(f"**Score:** {reliability_score}/100")
            st.write(f"**Explanation:** {explanation}")
        else:
            st.write("Could not determine reliability.")

    if st.button("🔄 Reset Conversation"):
        st.session_state.conversation_history = ""
        st.write("Conversation history cleared!")
