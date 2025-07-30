# 📬 JobBuddy 1.0 – Personal Job Application Tracker

JobBuddy 1.0 is a personal assistant that helps you track your job applications by automatically scanning your Gmail for job-related emails like “job application,” “application received,” or “you applied.” It visualizes your progress over time using clean dashboards — perfect for staying organized in your job hunt!

> **Note:** This is a personal-use version and currently only works for the Gmail account configured during setup.

---

## 🔍 Features

- ✅ Gmail integration to fetch job application emails  
- 📊 Dashboard showing number of applications, today . yesterday and  per week
- 🔐 OAuth2 sign-in (currently personal-use only)  
- ⚙️ Built with Python, Streamlit, and Gmail API  

---

## 📸 Demo

![screenshot](demo_screenshot.png) <!-- Replace with your own screenshot -->

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Gmail API (OAuth 2.0)**
- **Pandas / Matplotlib / Plotly** (for data processing & charts)

---

## 🚀 How to Run (Personal Version)

> ⚠️ This version works only with your own Gmail account, as it's hardcoded or uses a single OAuth client.

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/jobbuddy-1.0.git
cd jobbuddy-1.0

2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt

3. Set up Gmail API
Go to Google Cloud Console

Create a new project

Enable the Gmail API

Create OAuth 2.0 Client ID for Desktop or Web

Download the credentials.json and place it in your project folder

4. Run Streamlit
bash
Copy
Edit
streamlit run app.py
🧪 Features to Add (Future)
 Multi-user support

 Job status tracking (Interview, Offer, Rejected)

 Export to Excel or Notion

 Application reminders

🙋‍♂️ **Why I Built This**
I built JobBuddy 1.0 to organize my own job hunt — instead of checking emails manually, I wanted a tool that fetches and visualizes my progress in one place.
It's a great personal productivity project that I’m proud of!



🧠 Author
Made with 💻 by Siza Kadri



