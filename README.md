# **SuperBowl Sentiment Analysis Dashboard**

This project aims to analyze Super Bowl 2025 commercial reactions and sentiments across platforms like **YouTube** and **Twitter**. The goal is to provide insights into public sentiment towards various brands based on user comments and sentiment analysis.

## **Overview**

With the growing impact of advertisements and commercials during the Super Bowl, understanding how people feel about specific brands is crucial for marketers. This project gathers comments from different platforms, performs **VADER Sentiment Analysis**, and presents the results in an interactive **Dashboard**.

### **Key Features**
- **Data Collection**: Comments are scraped from platforms like **YouTube** and **Twitter** using the **PRAW** library (for Reddit) and YouTube API for other sources.
- **Sentiment Analysis**: Utilizes **VADER Sentiment Analysis** to categorize comments into **positive**, **neutral**, or **negative** sentiment.
- **Interactive Dashboard**: Visualizes sentiment distributions, trends, and brand-specific insights using **Flask** and **Dash**.
- **Deployment**: Deployed on **Heroku** for public access.

## **Technologies Used**
- **Python** for data collection and analysis.
- **Pandas** for data manipulation and analysis.
- **VADER Sentiment Analysis** for sentiment classification.
- **Flask** and **Dash** for building the interactive dashboard.
- **Matplotlib** for visualizations (graphs, charts).
- **Heroku** for deployment.

## **Getting Started**

To run this project locally or contribute to it, follow the instructions below:

### **Prerequisites**
Make sure you have the following installed:
- **Python 3.x** or higher
- **Pip** (Python package installer)

### **Install Dependencies**
Clone this repository and install the necessary dependencies using the following commands:

```bash
git clone https://github.com/your_username/SuperBowl2025.git
cd SuperBowl2025
pip install -r requirements.txt
