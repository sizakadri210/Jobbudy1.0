# app.py
import streamlit as st
import pandas as pd
import altair as alt
import datetime

from util.gmail_fetcher import fetch_job_emails

# Page setup
st.set_page_config(page_title="Job Tracker", page_icon="💼", layout="wide")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📊 Dashboard","📆Trackig","🕵️‍♂️Resume Analyzer"])

# Pages
if page == "🏠 Home":
    st.title("💼 Welcome to Job Buddy : Your Ultimate Companion for Job Search")
    st.write("This app helps you track and analyze your job applications automatically.")

    # List of motivational quotes
    quotes = [
        "Believe you can and you're halfway there. – Theodore Roosevelt",
        "Your limitation—it’s only your imagination.",
        "Push yourself, because no one else is going to do it for you.",
        "Great things never come from comfort zones.",
        "Dream it. Wish it. Do it.",
        "Success doesn’t just find you. You have to go out and get it.",
        "The harder you work for something, the greater you’ll feel when you achieve it.",
        "Don’t watch the clock; do what it does. Keep going. – Sam Levenson",
        "Stay positive, work hard, make it happen.",
        "The future depends on what you do today. – Mahatma Gandhi"
    ]

    # Get today's date and pick a quote based on day of the year
    today = datetime.date.today()
    quote_of_the_day = quotes[today.toordinal() % len(quotes)]

    # Display the quote with some styling
    st.markdown(f"""
    <div style="background-color:#DFF6FF; padding:20px; border-radius:10px; margin-bottom:20px;">
        <h3 style="color:#007ACC; text-align:center;">✨ Daily Motivational Quote ✨</h3>
        <p style="font-style:italic; font-size:18px; text-align:center;">"{quote_of_the_day}"</p>
    </div>
    """, unsafe_allow_html=True)

elif page == "📊 Dashboard":
    st.title("🪞 Job Application: Reflexion")

    try:
        data = fetch_job_emails()
        df = pd.DataFrame(data)

        if not df.empty:
            st.success(f"✅ Found {len(df)} emails.")

            # Convert 'Date' with timezone handling and drop invalid dates
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True).dt.tz_convert(None)
            df = df.dropna(subset=['Date'])  # Drop invalid dates

            # Extract useful datetime parts
            df['Year'] = df['Date'].dt.year
            df['Week_Num'] = df['Date'].dt.isocalendar().week
            df['Date_Only'] = df['Date'].dt.date  # for daily filtering

            # Metrics calculation
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days=1)
            last_7_days = today - datetime.timedelta(days=7)

            jobs_today = df[df['Date_Only'] == today]
            jobs_yesterday = df[df['Date_Only'] == yesterday]
            jobs_last_7_days = df[df['Date_Only'] >= last_7_days]

            # Display metrics in columns
            col1, col2, col3 = st.columns(3)
            col1.metric("🟢 Jobs Applied Today", len(jobs_today))
            col2.metric("🕒 Jobs Applied Yesterday", len(jobs_yesterday))
            col3.metric("📆 Jobs Applied Last 7 Days", len(jobs_last_7_days))

            st.markdown("---")

            # Weekly trend chart
            current_year = today.year
            df_current = df[df['Year'] == current_year]

            trend = df_current.groupby('Week_Num').size().reset_index(name='Applications')
            trend['Week_Label'] = 'Week ' + trend['Week_Num'].astype(str)

            chart = alt.Chart(trend).mark_line(point=True).encode(
                x=alt.X('Week_Label', title='Week Number'),
                y=alt.Y('Applications', title='Jobs Applied'),
                tooltip=['Week_Label', 'Applications']
            ).properties(
                title=f"📊 Weekly Job Application Trend - {current_year}",
                width=700
            )

            st.altair_chart(chart, use_container_width=True)

            # CSV Download button
            csv = df.to_csv(index=False)
            st.download_button("📥 Download Job Data as CSV", csv, "job_applications.csv", "text/csv")

            # Raw data table in expander
            with st.expander("🔍 Raw Email Data"):
                st.dataframe(df[['Date', 'Subject', 'From']].sort_values(by='Date', ascending=False))

        else:
            st.warning("No job-related emails found.")
            

    except Exception as e:
        st.error(f"Error: {e}")

elif page == "📆Trackig":
    st.title("📊 Job Application & Status")
    st.info("🚧 This feature is coming soon! You'll be able to track your applications and their statuses here.")

elif page == "🕵️‍♂️Resume Analyzer":
    st.title("🔍Your AI Powered Resume Analyzer")
    st.info("🚀 Coming soon! This tool will help you analyze and optimize your resume with AI insights.")
    
    
