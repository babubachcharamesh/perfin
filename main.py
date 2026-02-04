import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Personal Finance Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .expense-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
    }
    .income-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
    }
    .savings-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 2rem;
        padding: 0.75rem 2rem;
        border: none;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
    .edit-btn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.8rem !important;
    }
    .delete-btn {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%) !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.8rem !important;
    }
    .save-btn {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%) !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.8rem !important;
    }
    .cancel-btn {
        background: linear-gradient(135deg, #bdc3c7 0%, #2c3e50 100%) !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.8rem !important;
    }
    .transaction-row {
        background: #f8f9fa;
        border-radius: 0.75rem;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    .transaction-row:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .transaction-income {
        border-left-color: #43e97b !important;
    }
    .transaction-expense {
        border-left-color: #f5576c !important;
    }
</style>
""", unsafe_allow_html=True)

import os

# Data file path
DATA_FILE = "finance_data.json"

def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading data: {e}")
    return {"transactions": [], "budgets": {}, "goals": []}

def save_data():
    """Save current state to JSON file"""
    data = {
        "transactions": st.session_state.transactions,
        "budgets": st.session_state.budgets,
        "goals": st.session_state.goals
    }
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Initialize session state from file
if 'data_loaded' not in st.session_state:
    saved_data = load_data()
    st.session_state.transactions = saved_data.get("transactions", [])
    st.session_state.budgets = saved_data.get("budgets", {})
    st.session_state.goals = saved_data.get("goals", [])
    st.session_state.data_loaded = True

if 'editing_id' not in st.session_state:
    st.session_state.editing_id = None
if 'delete_confirm_id' not in st.session_state:
    st.session_state.delete_confirm_id = None

def get_next_id():
    """Get next available transaction ID"""
    if not st.session_state.transactions:
        return 1
    return max(t['id'] for t in st.session_state.transactions) + 1

def delete_transaction(transaction_id):
    """Delete a transaction by ID"""
    st.session_state.transactions = [
        t for t in st.session_state.transactions if t['id'] != transaction_id
    ]
    st.session_state.delete_confirm_id = None
    save_data()
    st.success("✅ Transaction deleted successfully!")
    st.rerun()

def update_transaction(transaction_id, updated_data):
    """Update a transaction by ID"""
    for i, t in enumerate(st.session_state.transactions):
        if t['id'] == transaction_id:
            st.session_state.transactions[i].update(updated_data)
            save_data()
            break
    st.session_state.editing_id = None
    st.success("✅ Transaction updated successfully!")
    st.rerun()

# Sidebar navigation
with st.sidebar:
    st.markdown("### 💰 Finance Manager")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "💳 Transactions", "📈 Analytics", "🎯 Budget & Goals", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    
    total_income = sum(t['amount'] for t in st.session_state.transactions if t['type'] == 'Income')
    total_expense = sum(t['amount'] for t in st.session_state.transactions if t['type'] == 'Expense')
    balance = total_income - total_expense
    
    st.metric("Balance", f"${balance:,.2f}")
    st.metric("Monthly Income", f"${total_income:,.2f}")
    st.metric("Monthly Expense", f"${total_expense:,.2f}")

# Dashboard Page
if page == "📊 Dashboard":
    st.markdown('<div class="main-header">Personal Finance Dashboard</div>', unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; font-size: 0.9rem; opacity: 0.9;">Total Balance</h3>
            <h2 style="margin:0; font-size: 2rem;">${balance:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="income-card">
            <h3 style="margin:0; font-size: 0.9rem; opacity: 0.9;">Total Income</h3>
            <h2 style="margin:0; font-size: 2rem;">${total_income:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="expense-card">
            <h3 style="margin:0; font-size: 0.9rem; opacity: 0.9;">Total Expenses</h3>
            <h2 style="margin:0; font-size: 2rem;">${total_expense:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        savings_rate = (balance / total_income * 100) if total_income > 0 else 0
        st.markdown(f"""
        <div class="savings-card">
            <h3 style="margin:0; font-size: 0.9rem; opacity: 0.9;">Savings Rate</h3>
            <h2 style="margin:0; font-size: 2rem;">{savings_rate:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Income vs Expenses")
        
        df = pd.DataFrame(st.session_state.transactions)
        df['date'] = pd.to_datetime(df['date'])
        
        daily_summary = df.groupby(['date', 'type'])['amount'].sum().reset_index()
        pivot_df = daily_summary.pivot(index='date', columns='type', values='amount').fillna(0)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=pivot_df.index, y=pivot_df.get('Income', [0]*len(pivot_df)),
            mode='lines+markers', name='Income',
            line=dict(color='#4facfe', width=3),
            fill='tozeroy'
        ))
        fig.add_trace(go.Scatter(
            x=pivot_df.index, y=pivot_df.get('Expense', [0]*len(pivot_df)),
            mode='lines+markers', name='Expenses',
            line=dict(color='#f5576c', width=3),
            fill='tozeroy'
        ))
        fig.update_layout(
            height=400,
            template='plotly_white',
            hovermode='x unified',
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Expense Breakdown")
        
        expenses_df = df[df['type'] == 'Expense']
        if not expenses_df.empty:
            category_expenses = expenses_df.groupby('category')['amount'].sum().reset_index()
            
            fig = px.pie(
                category_expenses, values='amount', names='category',
                hole=0.6, color_discrete_sequence=px.colors.sequential.Viridis
            )
            fig.update_layout(
                height=400,
                showlegend=True,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent Transactions with Edit/Delete
    st.subheader("🕐 Recent Transactions")
    
    recent_trans = sorted(st.session_state.transactions, key=lambda x: x['date'], reverse=True)[:5]
    
    for trans in recent_trans:
        icon = "🟢" if trans['type'] == 'Income' else "🔴"
        row_class = "transaction-income" if trans['type'] == 'Income' else "transaction-expense"
        
        with st.container():
            st.markdown(f"""
            <div class="transaction-row {row_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex: 1;">
                        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
                        <strong>{trans['date']}</strong> | 
                        <span style="color: {'#43e97b' if trans['type'] == 'Income' else '#f5576c'}; font-weight: 600;">
                            {trans['category']}
                        </span> | 
                        {trans['description']}
                    </div>
                    <div style="text-align: right; min-width: 150px;">
                        <span style="color: {'green' if trans['type'] == 'Income' else 'red'}; font-weight: 700; font-size: 1.1rem;">
                            {'+' if trans['type'] == 'Income' else '-'}${trans['amount']:,.2f}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Transactions Page with Full Edit/Delete
elif page == "💳 Transactions":
    st.markdown('<div class="main-header">Transaction Management</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Transaction", "📋 View & Manage", "🗑️ Bulk Actions"])
    
    # Tab 1: Add Transaction
    with tab1:
        with st.form("transaction_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                trans_type = st.selectbox("Type", ["Expense", "Income"])
                category = st.selectbox(
                    "Category",
                    ["Food", "Transport", "Housing", "Entertainment", "Utilities", "Healthcare", "Shopping", "Salary", "Freelance", "Investment", "Other"]
                )
            
            with col2:
                amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
                date = st.date_input("Date", datetime.now())
            
            description = st.text_input("Description", placeholder="Enter details...")
            
            submitted = st.form_submit_button("💾 Add Transaction")
            
            if submitted:
                new_transaction = {
                    "id": get_next_id(),
                    "date": date.strftime("%Y-%m-%d"),
                    "category": category,
                    "amount": amount,
                    "type": trans_type,
                    "description": description
                }
                st.session_state.transactions.append(new_transaction)
                save_data()
                st.success("✅ Transaction added successfully!")
                st.balloons()
    
    # Tab 2: View & Manage with Edit/Delete
    with tab2:
        if st.session_state.transactions:
            df = pd.DataFrame(st.session_state.transactions)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date', ascending=False)
            
            # Filters
            with st.expander("🔍 Filters", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    filter_type = st.multiselect("Filter by Type", df['type'].unique(), default=df['type'].unique())
                with col2:
                    filter_category = st.multiselect("Filter by Category", df['category'].unique(), default=df['category'].unique())
                with col3:
                    date_range = st.date_input("Date Range", [df['date'].min(), df['date'].max()])
                
                search_term = st.text_input("Search description", placeholder="Type to search...")
            
            # Apply filters
            mask = (
                df['type'].isin(filter_type) &
                df['category'].isin(filter_category) &
                (df['date'] >= pd.Timestamp(date_range[0])) &
                (df['date'] <= pd.Timestamp(date_range[1]))
            )
            if search_term:
                mask = mask & df['description'].str.contains(search_term, case=False, na=False)
            
            filtered_df = df[mask]
            
            # Display transactions with Edit/Delete
            st.write(f"Showing {len(filtered_df)} transactions")
            
            for idx, trans in filtered_df.iterrows():
                trans_id = trans['id']
                is_editing = st.session_state.editing_id == trans_id
                is_deleting = st.session_state.delete_confirm_id == trans_id
                
                row_class = "transaction-income" if trans['type'] == 'Income' else "transaction-expense"
                icon = "🟢" if trans['type'] == 'Income' else "🔴"
                
                # Edit Mode
                if is_editing:
                    with st.container():
                        st.markdown("#### ✏️ Edit Transaction")
                        with st.form(f"edit_form_{trans_id}"):
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                new_type = st.selectbox("Type", ["Expense", "Income"], 
                                                      index=0 if trans['type'] == 'Expense' else 1,
                                                      key=f"type_{trans_id}")
                            with col2:
                                new_category = st.selectbox("Category",
                                    ["Food", "Transport", "Housing", "Entertainment", "Utilities", 
                                     "Healthcare", "Shopping", "Salary", "Freelance", "Investment", "Other"],
                                    index=["Food", "Transport", "Housing", "Entertainment", "Utilities", 
                                           "Healthcare", "Shopping", "Salary", "Freelance", "Investment", "Other"].index(trans['category']),
                                    key=f"cat_{trans_id}")
                            with col3:
                                new_amount = st.number_input("Amount", min_value=0.01, value=float(trans['amount']),
                                                           key=f"amt_{trans_id}")
                            with col4:
                                new_date = st.date_input("Date", datetime.strptime(trans['date'], '%Y-%m-%d'),
                                                        key=f"date_{trans_id}")
                            
                            new_desc = st.text_input("Description", value=trans['description'],
                                                   key=f"desc_{trans_id}")
                            
                            col_save, col_cancel = st.columns(2)
                            with col_save:
                                if st.form_submit_button("💾 Save Changes", use_container_width=True):
                                    update_transaction(trans_id, {
                                        'type': new_type,
                                        'category': new_category,
                                        'amount': new_amount,
                                        'date': new_date.strftime('%Y-%m-%d'),
                                        'description': new_desc
                                    })
                            with col_cancel:
                                if st.form_submit_button("❌ Cancel", use_container_width=True):
                                    st.session_state.editing_id = None
                                    st.rerun()
                
                # Delete Confirmation Mode
                elif is_deleting:
                    with st.container():
                        st.error(f"⚠️ Are you sure you want to delete this transaction?")
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"**{trans['date']}** - {trans['category']} - ${trans['amount']:,.2f}")
                        with col2:
                            if st.button("✅ Yes, Delete", key=f"confirm_del_{trans_id}", use_container_width=True):
                                delete_transaction(trans_id)
                        with col3:
                            if st.button("❌ Cancel", key=f"cancel_del_{trans_id}", use_container_width=True):
                                st.session_state.delete_confirm_id = None
                                st.rerun()
                        st.markdown("---")
                
                # Normal View Mode
                else:
                    with st.container():
                        cols = st.columns([0.5, 1.5, 1.5, 2, 1.5, 1, 1])
                        
                        with cols[0]:
                            st.write(f"{icon}")
                        with cols[1]:
                            st.write(f"**{trans['date']}**")
                        with cols[2]:
                            color = "green" if trans['type'] == 'Income' else "red"
                            st.write(f"<span style='color:{color}; font-weight:600;'>{trans['category']}</span>", 
                                    unsafe_allow_html=True)
                        with cols[3]:
                            st.write(f"{trans['description']}")
                        with cols[4]:
                            color = "green" if trans['type'] == 'Income' else "red"
                            sign = "+" if trans['type'] == 'Income' else "-"
                            st.write(f"<span style='color:{color}; font-weight:700;'>{sign}${trans['amount']:,.2f}</span>", 
                                    unsafe_allow_html=True)
                        with cols[5]:
                            if st.button("✏️ Edit", key=f"edit_{trans_id}", use_container_width=True):
                                st.session_state.editing_id = trans_id
                                st.session_state.delete_confirm_id = None
                                st.rerun()
                        with cols[6]:
                            if st.button("🗑️ Delete", key=f"delete_{trans_id}", use_container_width=True):
                                st.session_state.delete_confirm_id = trans_id
                                st.session_state.editing_id = None
                                st.rerun()
                        
                        st.markdown("---")
            
            # Export option
            if not filtered_df.empty:
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Export Filtered to CSV",
                    csv,
                    "transactions.csv",
                    "text/csv"
                )
        else:
            st.info("No transactions yet. Add your first transaction above!")
    
    # Tab 3: Bulk Actions
    with tab3:
        st.subheader("🗑️ Bulk Delete")
        
        if st.session_state.transactions:
            df = pd.DataFrame(st.session_state.transactions)
            
            # Select transactions to delete
            st.write("Select transactions to delete:")
            
            # Create checkboxes for each transaction
            to_delete = []
            for trans in sorted(st.session_state.transactions, key=lambda x: x['date'], reverse=True):
                col1, col2 = st.columns([0.1, 0.9])
                with col1:
                    if st.checkbox("", key=f"bulk_{trans['id']}"):
                        to_delete.append(trans['id'])
                with col2:
                    icon = "🟢" if trans['type'] == 'Income' else "🔴"
                    st.write(f"{icon} **{trans['date']}** | {trans['category']} | {trans['description']} | "
                            f"{'+' if trans['type'] == 'Income' else '-'}${trans['amount']:,.2f}")
            
            if to_delete:
                st.warning(f"⚠️ You are about to delete {len(to_delete)} transaction(s)")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Confirm Bulk Delete", use_container_width=True, type="primary"):
                        st.session_state.transactions = [
                            t for t in st.session_state.transactions 
                            if t['id'] not in to_delete
                        ]
                        save_data()
                        st.success(f"✅ Deleted {len(to_delete)} transactions!")
                        st.rerun()
                with col2:
                    if st.button("❌ Clear Selection", use_container_width=True):
                        st.rerun()
            
            st.markdown("---")
            st.subheader("⚠️ Delete All Transactions")
            
            with st.expander("Click to delete ALL transactions"):
                confirm_text = st.text_input("Type 'DELETE ALL' to confirm")
                if confirm_text == "DELETE ALL":
                    if st.button("🗑️ DELETE EVERYTHING", type="secondary"):
                        st.session_state.transactions = []
                        save_data()
                        st.success("All transactions deleted!")
                        st.rerun()
        else:
            st.info("No transactions to delete.")

# Analytics Page
elif page == "📈 Analytics":
    st.markdown('<div class="main-header">Financial Analytics</div>', unsafe_allow_html=True)
    
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.strftime('%Y-%m')
        
        # Monthly Trends
        st.subheader("📊 Monthly Trends")
        
        monthly_data = df.groupby(['month', 'type'])['amount'].sum().reset_index()
        monthly_pivot = monthly_data.pivot(index='month', columns='type', values='amount').fillna(0)
        
        fig = go.Figure()
        if 'Income' in monthly_pivot.columns:
            fig.add_trace(go.Bar(
                name='Income',
                x=monthly_pivot.index,
                y=monthly_pivot['Income'],
                marker_color='#4facfe'
            ))
        if 'Expense' in monthly_pivot.columns:
            fig.add_trace(go.Bar(
                name='Expenses',
                x=monthly_pivot.index,
                y=monthly_pivot['Expense'],
                marker_color='#f5576c'
            ))
        
        fig.update_layout(
            barmode='group',
            height=500,
            template='plotly_white',
            xaxis_title="Month",
            yaxis_title="Amount ($)",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Category Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏷️ Top Spending Categories")
            expenses_df = df[df['type'] == 'Expense']
            if not expenses_df.empty:
                category_stats = expenses_df.groupby('category').agg({
                    'amount': ['sum', 'count']
                }).round(2)
                category_stats.columns = ['Total Spent', 'Transactions']
                category_stats = category_stats.sort_values('Total Spent', ascending=False)
                st.dataframe(category_stats, use_container_width=True)
        
        with col2:
            st.subheader("📅 Spending Patterns")
            if not expenses_df.empty:
                expenses_df['day_of_week'] = expenses_df['date'].dt.day_name()
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_spending = expenses_df.groupby('day_of_week')['amount'].sum().reindex(day_order).fillna(0)
                
                fig = px.bar(
                    x=day_spending.index,
                    y=day_spending.values,
                    labels={'x': 'Day of Week', 'y': 'Total Spent ($)'},
                    color=day_spending.values,
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add transactions to see analytics!")

# Budget & Goals Page
elif page == "🎯 Budget & Goals":
    st.markdown('<div class="main-header">Budget & Goals</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🎯 Budgets", "🏆 Goals"])
    
    with tab1:
        st.subheader("Set Monthly Budgets")
        
        categories = ["Food", "Transport", "Housing", "Entertainment", "Utilities", "Healthcare", "Shopping", "Other"]
        
        col1, col2 = st.columns(2)
        
        for i, category in enumerate(categories):
            with (col1 if i % 2 == 0 else col2):
                current_budget = st.session_state.budgets.get(category, 0)
                new_budget = st.number_input(
                    f"{category} Budget ($)",
                    min_value=0,
                    value=current_budget,
                    key=f"budget_{category}"
                )
                st.session_state.budgets[category] = new_budget
                save_data()
                
                # Calculate current spending
                current_spending = sum(
                    t['amount'] for t in st.session_state.transactions
                    if t['category'] == category and t['type'] == 'Expense'
                )
                
                if new_budget > 0:
                    progress = min(current_spending / new_budget, 1)
                    st.progress(progress)
                    st.caption(f"Spent: ${current_spending:,.2f} / ${new_budget:,.2f}")
                    
                    if current_spending > new_budget:
                        st.error(f"⚠️ Over budget by ${current_spending - new_budget:,.2f}!")
                    elif progress > 0.8:
                        st.warning("⚠️ Approaching budget limit!")
        
        st.success("Budgets updated automatically!")
    
    with tab2:
        st.subheader("💰 Savings Goals")
        
        with st.form("add_goal"):
            col1, col2, col3 = st.columns(3)
            with col1:
                goal_name = st.text_input("Goal Name", placeholder="e.g., Emergency Fund")
            with col2:
                target_amount = st.number_input("Target Amount ($)", min_value=1.0, step=100.0)
            with col3:
                deadline = st.date_input("Target Date", datetime.now() + timedelta(days=365))
            
            if st.form_submit_button("🎯 Add Goal"):
                st.session_state.goals.append({
                    "name": goal_name,
                    "target": target_amount,
                    "current": 0,
                    "deadline": deadline.strftime("%Y-%m-%d"),
                    "created": datetime.now().strftime("%Y-%m-%d")
                })
                save_data()
                st.success(f"Goal '{goal_name}' added!")
        
        # Display Goals
        if st.session_state.goals:
            for i, goal in enumerate(st.session_state.goals):
                progress = goal['current'] / goal['target'] if goal['target'] > 0 else 0
                
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.markdown(f"### {goal['name']}")
                        st.caption(f"Deadline: {goal['deadline']}")
                    
                    with col2:
                        st.progress(min(progress, 1.0))
                        st.caption(f"${goal['current']:,.2f} of ${goal['target']:,.2f} ({progress*100:.1f}%)")
                    
                    with col3:
                        add_amount = st.number_input(
                            "Add $", 
                            min_value=0.0, 
                            key=f"add_goal_{i}",
                            label_visibility="collapsed"
                        )
                        if add_amount > 0:
                            if st.button("💰", key=f"btn_goal_{i}"):
                                st.session_state.goals[i]['current'] += add_amount
                                save_data()
                                st.rerun()
                    
                    st.markdown("---")

# Settings Page
elif page == "⚙️ Settings":
    st.markdown('<div class="main-header">Settings</div>', unsafe_allow_html=True)
    
    st.subheader("💾 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### Export Data")
        data = {
            "transactions": st.session_state.transactions,
            "budgets": st.session_state.budgets,
            "goals": st.session_state.goals
        }
        json_str = json.dumps(data, indent=2)
        st.download_button(
            "📥 Download Backup (JSON)",
            json_str,
            "finance_backup.json",
            "application/json"
        )
    
    with col2:
        st.warning("### Import Data")
        uploaded_file = st.file_uploader("Upload backup file", type=['json'])
        if uploaded_file is not None:
            data = json.load(uploaded_file)
            st.session_state.transactions = data.get('transactions', [])
            st.session_state.budgets = data.get('budgets', {})
            st.session_state.goals = data.get('goals', [])
            save_data()
            st.success("✅ Data restored successfully!")
            st.rerun()
    
    st.markdown("---")
    
    st.subheader("⚠️ Danger Zone")
    
    if st.button("🗑️ Clear All Data", type="secondary"):
        confirm = st.checkbox("I understand this will delete all my data")
        if confirm:
            st.session_state.transactions = []
            st.session_state.budgets = {}
            st.session_state.goals = []
            save_data()
            st.success("All data cleared!")
            st.rerun()

# Footer
st.markdown("---")
st.caption("💰 Personal Finance Manager | Built with Streamlit | © 2026")