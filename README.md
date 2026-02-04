# 💰 Personal Finance Manager

A modern, sleek, and high-performance Personal Finance Manager built with **Python** and **Streamlit**. Take control of your financial life with real-time analytics, budget tracking, and goal management.

## ✨ Key Features

### 📊 Interactive Dashboard
- **Key Metrics**: Instantly view your Total Balance, Monthly Income, Monthly Expenses, and Savings Rate.
- **Dynamic Charts**: Visualize your income vs. expenses with interactive line and bar charts.
- **Recent Transactions**: Stay updated with your most recent financial activities at a glance.

### 💳 Transaction Management
- **Detailed Entry**: Add transactions with categories, dates, and descriptions.
- **Full CRUD Support**: Edit or delete any transaction easily.
- **Advanced Filtering**: Filter transactions by type, category, date range, or search descriptions.
- **Bulk Actions**: Efficiently manage multiple transactions at once.

### 📈 Detailed Analytics
- **Monthly Trends**: Compare your income and expenses over time.
- **Category Breakdown**: Understand exactly where your money is going with intuitive pie charts.
- **Spending Patterns**: Identify your busiest spending days and top categories.

### 🎯 Budgets & Goals
- **Smart Budgeting**: Set monthly spending limits for different categories and track your progress.
- **Savings Goals**: Define financial targets (e.g., Emergency Fund) and track your contributions toward achieving them.

### ⚙️ Settings & Data Security
- **Data Portability**: Export your entire financial history to a JSON file for backup.
- **Easy Import**: Restore your data from a JSON backup anytime.
- **Full Control**: Option to clear all data and start fresh.

---

## 🛠️ Technology Stack

- **Framework**: [Streamlit](https://streamlit.io/)
- **Data Processing**: [Pandas](https://pandas.pydata.org/)
- **Visualization**: [Plotly](https://plotly.com/)
- **Styling**: Custom CSS for a premium, modern UI

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Local Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd per-fin-kimi
   ```

2. **Run with uv (recommended)**:
   ```bash
   uv run streamlit run main.py
   ```

3. **Or run with pip**:
   ```bash
   pip install -r requirements.txt
   streamlit run main.py
   ```

---

## 🌐 Deployment to Streamlit Cloud

Ready to share your app? Follow these simple steps:

1. **Push your code** to a GitHub repository.
2. **Visit [Streamlit Cloud](https://share.streamlit.io/)** and sign in.
3. **Click "New app"** and select your repository, branch, and `main.py` as the entry point.
4. **Deploy!** Your app will be live at a custom `*.streamlit.app` URL.

> [!IMPORTANT]
> Since Streamlit Cloud is ephemeral, use the **Export/Import** feature in the Settings page to persist your data between sessions.

---

## 🔒 Privacy & Data
Your data stays with you. This app processes all information locally in your browser session or through the JSON files you export/import. No data is stored on external servers unless you explicitly configure a database.

---

Built with ❤️ by [Your Name/Github Handle]
