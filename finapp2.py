import os
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import google.generativeai as genai
genai.configure(
    api_key="AQ.Ab8RN6LYVy1Bfre88s7Auw6LlTXVoWkgZHp5QHcyRIU1HorQzw"
)
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)
st.set_page_config(
    page_title="FinGenius AI",
    page_icon="📈",
    layout="wide"
)
st.markdown("""
<style>
.stApp{
    background:#0f172a;
    color:white;
}
section[data-testid="stSidebar"]{
    background:#020617;
}
.metric-box{
    background:#1e293b;
    padding:20px;
    border-radius:15px;
    text-align:center;
}
.metric-title{
    color:#94a3b8;
    font-size:14px;
}
.metric-value{
    color:#3b82f6;
    font-size:28px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)
def get_stock_data(ticker):

    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "Company": info.get("longName"),
        "Sector": info.get("sector"),
        "Current Price": info.get("currentPrice"),
        "Market Cap": info.get("marketCap"),
        "PE Ratio": info.get("trailingPE"),
        "EPS": info.get("trailingEps"),
        "Revenue Growth": info.get("revenueGrowth"),
        "Profit Margin": info.get("profitMargins"),
        "Debt To Equity": info.get("debtToEquity"),
        "ROE": info.get("returnOnEquity"),
        "Dividend Yield": info.get("dividendYield")
    }
def get_company_dataset(ticker):
    stock = yf.Ticker(ticker)
    return {
        "Income Statement": stock.financials,
        "Balance Sheet": stock.balance_sheet,
        "Cash Flow": stock.cashflow,
        "Quarterly Financials": stock.quarterly_financials
    }
def get_price_history(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="1y")
def analyze_company(data, risk_profile):
    prompt = f"""
You are an expert stock market educator and equity research analyst.

Investor Risk Profile:
{risk_profile}

Company Data:
{data}

IMPORTANT INSTRUCTIONS:

1. Use VERY SIMPLE beginner-friendly language.
2. For EVERY topic below, write EXACTLY 5 to 7 lines.
3. Explain what the metric means.
4. Explain why it is important.
5. Explain what investors can learn from it.
6. Avoid technical jargon.
7. Do not guarantee profits.
8. Use clear headings.

TOPICS TO COVER:

# Executive Summary
(5-7 lines)

# Business Overview
(5-7 lines)

# Financial Health
(5-7 lines)

# Revenue Analysis
(5-7 lines)

# Growth Potential
(5-7 lines)

# Strengths
(5-7 lines)

# Weaknesses
(5-7 lines)

# Benefits For Investors
(5-7 lines)

# Limitations For Investors
(5-7 lines)

# Hidden Risks
(5-7 lines)

# Best Case Scenario
(5-7 lines)

# Worst Case Scenario
(5-7 lines)

# Suitable Investor Type
(5-7 lines)

Finally provide:

# Investment Score (/100)

Explain score in 5 lines.

# Risk Score (/100)

Explain score in 5 lines.
"""
    response = model.generate_content(prompt)
    return response.text
def compare_companies(company1, company2, financials1, financials2):

    prompt = f"""
You are a professional stock market educator.

COMPANY 1:
{company1}

FINANCIALS 1:
{financials1}

COMPANY 2:
{company2}

FINANCIALS 2:
{financials2}

IMPORTANT INSTRUCTIONS:

1. Use simple beginner-friendly language.
2. For EVERY section write EXACTLY 5 to 7 lines.
3. Explain which company performs better and why.
4. Explain advantages and disadvantages.
5. Avoid technical jargon.

TOPICS:

# Business Comparison
(5-7 lines)

# Revenue Comparison
(5-7 lines)

# Profitability Comparison
(5-7 lines)

# Financial Health Comparison
(5-7 lines)

# Debt Analysis
(5-7 lines)

# Growth Potential
(5-7 lines)

# Risk Analysis
(5-7 lines)

# Benefits Of Company 1
(5-7 lines)

# Benefits Of Company 2
(5-7 lines)

# Which Investor Should Choose Company 1
(5-7 lines)

# Which Investor Should Choose Company 2
(5-7 lines)

# Final Verdict
(5-7 lines)

# Overall Winner
(5-7 lines)

# Investment Recommendation
(5-7 lines)

Do not guarantee profits.
"""
    response = model.generate_content(prompt)
    return response.text
def portfolio_analysis(portfolio):
    prompt = f"""
Analyze this investment portfolio:
{portfolio}
Provide:
1. Diversification Score
2. Risk Analysis
3. Sector Exposure
4. Strengths
5. Weaknesses
6. Suggested Improvements
7. Long-Term Outlook
Explain clearly for beginners.
"""
    response = model.generate_content(prompt)
    return response.text
def load_csv_dataset(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None
def financial_tutor(question):
    prompt = f"""
You are a financial educator.
Question:
{question}
Explain using:
- Simple language
- Examples
- Practical investing insights
Answer:
"""
    response = model.generate_content(prompt)
    return response.text
st.sidebar.title("📈 FinGenius AI")
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Stock Analyzer",
        "Portfolio Analyzer",
        "Stock Comparison",
        "AI Financial Tutor"
    ]
)
risk_profile = st.sidebar.selectbox(
    "Risk Profile",
    [
        "Low",
        "Medium",
        "High"
    ]
)
if page == "Dashboard":
    st.title("📊 FinGenius AI Dashboard")
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.metric("Investment Score","84")
    with c2:
        st.metric("Risk Score","67")
    with c3:
        st.metric("Portfolio Health","88%")
    with c4:
        st.metric("Diversification","Good")
    chart_data = pd.DataFrame({
        "Month":[1,2,3,4,5,6],
        "Value":[100,115,110,130,145,160]
    })
    fig = px.line(
        chart_data,
        x="Month",
        y="Value",
        title="Portfolio Performance"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    AI Insights
    • Technology sector remains strong.
    • Diversification improves risk management.
    • Long-term investing generally reduces volatility impact.
    """)
elif page == "Stock Analyzer":
    st.title("🔍 Stock Analyzer")
    data_source = st.radio(
        "Choose Data Source",
        ["COMPANY NAME", "Upload CSV"]
    )
    if data_source == "COMPANY NAME":
        ticker = st.text_input(
            "Enter Stock Ticker",
            "AAPL"
        )
        if st.button("Analyze Stock"):
            with st.spinner("Fetching Data..."):
                data = get_stock_data(ticker)
                datasets = get_company_dataset(ticker)
            st.subheader("Company Fundamentals")
            st.json(data)
            st.subheader("📊 Income Statement")
            st.dataframe(datasets["Income Statement"])
            st.subheader("🏦 Balance Sheet")
            st.dataframe(datasets["Balance Sheet"])
            st.subheader("💵 Cash Flow")
            st.dataframe(datasets["Cash Flow"])
            hist = get_price_history(ticker)
            fig = px.line(
                hist,
                y="Close",
                title=f"{ticker} Price History"
            )
            st.plotly_chart(fig, use_container_width=True)
            report = analyze_company(
                data,
                risk_profile
            )
            st.subheader("AI Financial Report")
            st.markdown(report)
    else:
        uploaded_file = st.file_uploader(
            "Upload Stock Dataset CSV",
            type=["csv"]
        )
        if uploaded_file:
            df = load_csv_dataset(uploaded_file)
            st.subheader("Dataset Preview")
            st.dataframe(df)
            st.subheader("Dataset Statistics")
            st.dataframe(df.describe())
            numeric_cols = df.select_dtypes(
                include=["number"]
            ).columns
            if len(numeric_cols) > 0:
                selected_col = st.selectbox(
                    "Select Column To Visualize",
                    numeric_cols
                )
                fig = px.line(
                    df,
                    y=selected_col,
                    title=f"{selected_col} Trend"
                )
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
            report = model.generate_content(
                f"""
Analyze this stock dataset:
{df.head(50).to_string()}
Provide:
1. Key Insights
2. Trends
3. Risks
4. Growth Signals
5. Investor Summary
"""
            )
            st.subheader("AI Dataset Analysis")
            st.markdown(report.text)
elif page == "Portfolio Analyzer":
    st.title("💼 Portfolio Analyzer")
    st.write("Enter holdings")
    stock1 = st.text_input(
        "Stock 1",
        "AAPL"
    )
    qty1 = st.number_input(
        "Quantity 1",
        value=10
    )
    stock2 = st.text_input(
        "Stock 2",
        "MSFT"
    )
    qty2 = st.number_input(
        "Quantity 2",
        value=5
    )
    if st.button("Analyze Portfolio"):
        allocation = pd.DataFrame({
            "Stock":[stock1,stock2],
            "Allocation":[qty1,qty2]
        })
        fig = px.pie(
            allocation,
            names="Stock",
            values="Allocation",
            title="Portfolio Allocation"
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )
        portfolio = {
            stock1: qty1,
            stock2: qty2
        }
        with st.spinner("Analyzing Portfolio..."):
            report = portfolio_analysis(
                portfolio
            )
        st.markdown(report)
elif page == "Stock Comparison":
    st.title("⚖️ Stock Comparison")
    comparison_mode = st.radio(
        "Comparison Mode",
        [
            "Yahoo finance",
            "Upload Two CSV Files"
        ]
    )
    if comparison_mode == "Yahoo finance":
        stock1 = st.text_input(
            "First Company",
            "AAPL"
        )
        stock2 = st.text_input(
            "Second Company",
            "MSFT"
        )
        if st.button("Compare Stocks"):
            data1 = get_stock_data(stock1)
            data2 = get_stock_data(stock2)
            st.columns(2)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(stock1)
                st.json(data1)
            with col2:
                st.subheader(stock2)
                st.json(data2)
            result = compare_companies(
                data1,
                data2,
                {},
                {}
            )
            st.subheader("AI Comparison Report")
            st.markdown(result)
    else:
        csv1 = st.file_uploader(
            "Upload Company 1 CSV",
            type=["csv"],
            key="csv1"
        )
        csv2 = st.file_uploader(
            "Upload Company 2 CSV",
            type=["csv"],
            key="csv2"
        )
        if csv1 and csv2:
            df1 = pd.read_csv(csv1)
            df2 = pd.read_csv(csv2)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Company 1 Dataset")
                st.dataframe(df1.head())
            with col2:
                st.subheader("Company 2 Dataset")
                st.dataframe(df2.head())
            num_cols1 = df1.select_dtypes(
                include=["number"]
            ).columns
            num_cols2 = df2.select_dtypes(
                include=["number"]
            ).columns
            common_cols = list(
                set(num_cols1).intersection(num_cols2)
            )
            if common_cols:
                metric = st.selectbox(
                    "Select Metric",
                    common_cols
                )
                compare_df = pd.DataFrame({
                    "Company 1": df1[metric],
                    "Company 2": df2[metric]
                })
                fig = px.line(
                    compare_df,
                    title=f"{metric} Comparison"
                )
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
            result = model.generate_content(
                f"""
Compare these two company datasets.
Company 1:
{df1.head(50).to_string()}
Company 2:
{df2.head(50).to_string()}
Provide:
1. Revenue Comparison
2. Profitability Comparison
3. Growth Analysis
4. Financial Strength
5. Risks
6. Better Investment Choice
7. Final Verdict
"""
            )
            st.subheader("AI Comparison Report")
            st.markdown(result.text)
elif page == "AI Financial Tutor":
    st.title("🤖 AI Financial Tutor")
    question = st.text_area(
        "Ask Anything About Finance"
    )
    if st.button("Ask Gemini"):
        with st.spinner("Thinking..."):
            answer = financial_tutor(question)
        st.markdown(answer)