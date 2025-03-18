This project is a **Reddit Post Dashboard** built using **Streamlit** that combines data visualization, AI-generated insights, and an interactive chatbot. The platform allows users to explore Reddit posts, view detailed engagement metrics, analyze post reliability using AI, and ask questions about the content directly through a chatbot.  

The solution is structured into three core files:  
- `app.py` – Homepage that displays an overview of Reddit posts.  
- `dashboard.py` – Detailed analysis of an individual Reddit post with visualizations and AI-generated insights.  
- `chatbot.py` – Backend logic for information retrieval, AI-based responses, and reliability evaluation using Google Gemini API.  

---

## 🏗️ **System Design and Thought Process**  
###  **1. Design Philosophy**  
The project was designed with a focus on:  
- **Clean and Professional UI:** Glassmorphism-style design with gradients, soft shadows, and hover effects.  
- **User Engagement:** Direct user interaction via a chatbot and dynamic visualizations.  
- **AI-Driven Insights:** Use of Google's Gemini AI for generating content-based responses and reliability scores.  
- **Scalability:** Handling large datasets efficiently using chunking and vector similarity techniques.  

---



### **2. Data Handling and Preprocessing**  
1. **Data Source:**  
   - Data is stored in `dataset.csv` and loaded using `pandas`.  
   - Data includes fields such as `title`, `selftext`, `author`, `score`, `likes`, `subreddit`, `comments`, etc.  

2. **Data Cleaning:**  
   - Missing values are handled by filling them with defaults (`0`, `None`, etc.).  
   - Text fields are combined into a `combined_text` field for efficient processing.  

3. **Chunking:**  
   - Long text is split into 500-word chunks to enhance retrieval accuracy.  
   - `TF-IDF` (Term Frequency-Inverse Document Frequency) is applied for chunk weighting.  

---

### **3. Information Retrieval and Similarity Matching**  
1. **TF-IDF Vectorization:**  
   - `TF-IDF` is used to convert text data into numeric vectors.  
   - High-frequency terms that are common across posts are given lower weights.  

2. **Cosine Similarity:**  
   - Measures the similarity between the user query and document chunks.  
   - Top `n` chunks are selected based on the highest similarity scores.  

3. **Context Construction:**  
   - The most relevant chunks are combined into a context for AI-based response generation.  

---

### **4. AI-Driven Response Generation**  
1. **Google Gemini API Integration:**  
   - AI-based conversational response is generated using the Gemini API.  
   - Prompts include:  
     - Context from the top-ranked document chunks.  
     - User query and conversation history.  

2. **Response Handling:**  
   - Responses are directly shown to the user in the chatbot interface.  
   - The chatbot can handle complex questions about the post's content.  

---

### **5. AI-Based Reliability Evaluation**  
1. **Reliability Prompt:**  
   - The AI model is prompted with metadata about the post (score, comments, sentiment, etc.).  
   - Task includes:  
     - Rating reliability from `0–100`.  
     - Stating reliability status (`Reliable` or `Unreliable`).  
     - Providing an explanation for the rating.  
     - Generating a concise summary of the post content.  

2. **Reliability Display:**  
   - The reliability score is displayed using a `progress bar`.  
   - Explanation and summary are shown directly in the UI.  

---

### **6. Visualization and Metrics**  
1. **Engagement Metrics:**  
   - Likes, comments, views, and scores are displayed using `st.metric()`.  
   - Clear separation of data using `st.columns()`.  

2. **Post Activity Over Time:**  
   - A line chart shows the number of posts over time using `Plotly`.  
   - Helps identify engagement trends and peak activity periods.  

3. **Top-Performing Posts:**  
   - A horizontal bar chart shows top-scoring posts using `Plotly`.  
   - Helps identify high-performing content and key contributors.  

4. **Top Subreddits and Authors:**  
   - Two pie charts show top 5 subreddits and authors using `Plotly`.  
   - Highlights where most activity is occurring.  

5. **Trending Topics:**  
   - A word cloud shows the most frequently mentioned terms in the post.  
   - Helps identify key themes and subjects.  

---

### **7. Conversation History**  
1. **State Management:**  
   - `st.session_state` is used to store conversation history.  
   - Previous conversation context is retained to generate more accurate responses.  

2. **Reset Option:**  
   - User can reset the conversation history using a reset button.  
   - Helps clear state and restart the interaction.  

---

### **8. Professional UI/UX**  
1. **Glassmorphism and Gradients:**  
   - The dashboard uses a deep purple-to-blue gradient with soft shadows.  
   - Modern and professional look.  

2. **Hover Effects:**  
   - Containers scale up slightly on hover for better interactivity.  
   - Shadow intensity increases on hover.  

3. **Dark Mode Theme:**  
   - The color scheme is balanced for both light and dark mode compatibility.  
   - High contrast for better readability.  

---


## 🚀 **Flow of the Project**  
1. **User opens homepage:**  
   - Overview of posts is shown in a structured card format.  
   - User clicks on a post to view more details.
  
<img width="1459" alt="Screenshot 2025-03-18 at 2 09 15 PM" src="https://github.com/user-attachments/assets/c881d4c3-831c-490a-83af-e483c06b8a93" />


2. **Dashboard View:**  
   - Displays post details, engagement, and visualizations.  
   - Shows AI-based reliability and summary.  
   - User can interact with the chatbot.
  
<img width="1162" alt="Screenshot 2025-03-18 at 2 20 43 PM" src="https://github.com/user-attachments/assets/67e2a891-83b4-44b0-a935-f317eaf58ff8" />


<img width="1146" alt="Screenshot 2025-03-18 at 2 16 15 PM" src="https://github.com/user-attachments/assets/63d5a1f8-ed84-4afa-b2f0-047d49accd71" />


<img width="1133" alt="Screenshot 2025-03-18 at 2 16 23 PM" src="https://github.com/user-attachments/assets/6f90137c-c050-4352-80aa-6147e8c97c43" />


<img width="1146" alt="Screenshot 2025-03-18 at 2 16 34 PM" src="https://github.com/user-attachments/assets/30ec2d85-0b56-42c2-b10d-38291953ad79" />


<img width="1163" alt="Screenshot 2025-03-18 at 2 16 43 PM" src="https://github.com/user-attachments/assets/6721938a-dac8-4be3-a95f-976be666c608" />


<img width="1162" alt="Screenshot 2025-03-18 at 2 16 50 PM" src="https://github.com/user-attachments/assets/6706fc95-dbd9-4e27-9f0f-f0f1b0dc7e85" />


<img width="1165" alt="Screenshot 2025-03-18 at 2 17 16 PM" src="https://github.com/user-attachments/assets/5944d4bc-55fc-45d9-adc0-e7b3e18e897a" />



3. **Backend Processing:**  
   - AI retrieves relevant context using similarity matching.  
   - Generates response using Gemini API.  
   - Evaluates reliability and generates a summary.  

---

## 🏆 **Strengths and Innovative Aspects**  
✅ Combines structured (metrics) and unstructured (text) data.  
✅ Uses AI for real-time analysis and conversational responses.  
✅ Professional UI with modern visual styling.  
✅ Efficient chunking and similarity matching for fast response.  
✅ Intuitive and easy-to-use interface.  

---

## 🔥 **Challenges and How They Were Solved**  
| Challenge | Solution |  
|----------|----------|  
| SSL Error in NLTK | Installed certificate manually using `Install Certificates.command`. |  
| Slow response time in large datasets | Used chunking and TF-IDF to reduce search space. |  
| Vulnerable Data Finding | Through Exploratory Data Analysis. |  
| UI Consistency | Used consistent CSS for dark/light mode. |  

---

## 🛠️ **Tech Stack**  
| Component | Technology Used |  
|-----------|-----------------|  
| Frontend | Streamlit |  
| Backend | Python |  
| Data Processing | Pandas |  
| AI/ML | Google Gemini API |  
| NLP | NLTK |  
| Visualization | Plotly, Matplotlib |  
| Similarity Matching | TF-IDF + Cosine Similarity |  

---

## 🎥 **Video Link : 
https://drive.google.com/file/d/14VTkfcSGk8uvTZVL6poxMcd2Fhe0v8tz/view?usp=sharing

## 📽️ **Project Link :
https://research-engineering-intern-assignment-yqia9zwn97ga8wwwwkxwrc.streamlit.app/

## 🚀 **How to Run the Project**  
1. **Clone the Repository:**  
```bash
git clone https://github.com/your-repo-name.git
