import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.data_processor import DataProcessor

st.set_page_config(page_title="Payout Tracking", page_icon="💳", layout="wide")

# Initialize data processor
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

st.title("💳 Payout Tracking & Cost Analysis")

# Check if data is available
data_status = st.session_state.data_processor.get_data_status()
if not data_status['all_uploaded']:
    st.warning("Please upload all required datasets first.")
    if st.button("Go to Data Upload"):
        st.switch_page("pages/1_📤_Data_Upload.py")
    st.stop()

# Get data
data = st.session_state.data_processor.get_all_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Payout basis filter
basis_options = ['All'] + list(data['payouts']['basis'].unique())
selected_basis = st.sidebar.selectbox("Payout Basis", basis_options)

# Influencer category filter (from influencers data)
categories = ['All'] + list(data['influencers']['category'].unique())
selected_category = st.sidebar.selectbox("Influencer Category", categories)

# Platform filter
platforms = ['All'] + list(data['influencers']['platform'].unique())
selected_platform = st.sidebar.selectbox("Platform", platforms)

# Payout amount range
min_payout = float(data['payouts']['total_payout'].min())
max_payout = float(data['payouts']['total_payout'].max())
payout_range = st.sidebar.slider(
    "Payout Amount Range (₹)",
    min_value=min_payout,
    max_value=max_payout,
    value=(min_payout, max_payout),
    step=100.0
)

# Apply filters
payouts_df = data['payouts'].copy()
influencers_df = data['influencers'].copy()

# Merge payouts with influencer data for filtering
payout_details = payouts_df.merge(
    influencers_df,
    left_on='influencer_id',
    right_on='ID',
    how='left'
)

if selected_basis != 'All':
    payout_details = payout_details[payout_details['basis'] == selected_basis]

if selected_category != 'All':
    payout_details = payout_details[payout_details['category'] == selected_category]

if selected_platform != 'All':
    payout_details = payout_details[payout_details['platform'] == selected_platform]

# Filter by payout amount
payout_details = payout_details[
    (payout_details['total_payout'] >= payout_range[0]) & 
    (payout_details['total_payout'] <= payout_range[1])
]

# Calculate comprehensive payout metrics
def calculate_payout_metrics():
    """Calculate comprehensive payout analytics"""
    
    # Basic payout metrics
    total_payouts = payout_details['total_payout'].sum()
    avg_payout = payout_details['total_payout'].mean()
    median_payout = payout_details['total_payout'].median()
    
    # Payout distribution by basis
    basis_distribution = payout_details['basis'].value_counts()
    
    # Rate analysis
    post_based = payout_details[payout_details['basis'] == 'post']
    order_based = payout_details[payout_details['basis'] == 'order']
    
    avg_post_rate = post_based['rate'].mean() if not post_based.empty else 0
    avg_order_rate = order_based['rate'].mean() if not order_based.empty else 0
    
    # Cost efficiency metrics
    tracking_data = data['tracking_data']
    
    # Calculate cost per order (CPO) - FIXED
    total_orders = pd.to_numeric(tracking_data['orders'], errors='coerce').fillna(0).sum()
    cpo = total_payouts / total_orders if total_orders > 0 else 0
    
    # Calculate cost per thousand impressions (CPM) - using reach as proxy for impressions
    posts_data = data['posts']
    total_reach = pd.to_numeric(posts_data['reach'], errors='coerce').fillna(0).sum()
    cpm = (total_payouts / total_reach * 1000) if total_reach > 0 else 0
    
    return {
        'total_payouts': total_payouts,
        'avg_payout': avg_payout,
        'median_payout': median_payout,
        'basis_distribution': basis_distribution,
        'avg_post_rate': avg_post_rate,
        'avg_order_rate': avg_order_rate,
        'cpo': cpo,
        'cpm': cpm,
        'total_orders': total_orders,
        'total_reach': total_reach
    }

metrics = calculate_payout_metrics()

# Key Payout Metrics
st.header("💰 Payout Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Payouts", f"₹{metrics['total_payouts']:,.0f}")

with col2:
    st.metric("Average Payout", f"₹{metrics['avg_payout']:,.0f}")

with col3:
    st.metric("Cost Per Order (CPO)", f"₹{metrics['cpo']:,.2f}")

with col4:
    st.metric("Cost Per Mille (CPM)", f"₹{metrics['cpm']:,.2f}")

# Add total influencers as a separate row
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_influencers = len(payout_details)
    st.metric("Total Influencers", total_influencers)

# Payout Analysis Charts
st.header("📊 Payout Analytics")

# First row of charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Payout Distribution by Basis")
    if not payout_details.empty:
        basis_stats = payout_details.groupby('basis').agg({
            'total_payout': ['sum', 'count', 'mean']
        }).round(0)
        basis_stats.columns = ['Total Amount', 'Count', 'Average']
        basis_stats = basis_stats.reset_index()
        
        fig_basis = px.pie(
            basis_stats,
            values='Total Amount',
            names='basis',
            title="Payout Distribution by Basis",
            color_discrete_sequence=['#FF6B35', '#1f77b4']
        )
        fig_basis.update_layout(height=400)
        st.plotly_chart(fig_basis, use_container_width=True)

with col2:
    st.subheader("Payout Amount Distribution")
    fig_dist = px.histogram(
        payout_details,
        x='total_payout',
        title="Payout Amount Distribution",
        nbins=20,
        color_discrete_sequence=['#FF6B35']
    )
    fig_dist.add_vline(
        x=metrics['avg_payout'], 
        line_dash="dash", 
        line_color="red", 
        annotation_text=f"Avg: ₹{metrics['avg_payout']:,.0f}"
    )
    fig_dist.update_layout(height=400)
    st.plotly_chart(fig_dist, use_container_width=True)

# Second row of charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Platform Cost Analysis")
    platform_costs = payout_details.groupby('platform').agg({
        'total_payout': 'sum',
        'influencer_id': 'count'
    }).reset_index()
    platform_costs['avg_cost_per_influencer'] = platform_costs['total_payout'] / platform_costs['influencer_id']
    
    fig_platform = px.bar(
        platform_costs,
        x='platform',
        y='total_payout',
        title="Total Payouts by Platform",
        color='avg_cost_per_influencer',
        color_continuous_scale='viridis'
    )
    fig_platform.update_layout(height=400)
    st.plotly_chart(fig_platform, use_container_width=True)

with col2:
    st.subheader("Category Cost Analysis")
    category_costs = payout_details.groupby('category').agg({
        'total_payout': 'sum',
        'influencer_id': 'count'
    }).reset_index()
    category_costs['avg_cost_per_influencer'] = category_costs['total_payout'] / category_costs['influencer_id']
    
    fig_category = px.bar(
        category_costs,
        x='category',
        y='total_payout',
        title="Total Payouts by Category",
        color='avg_cost_per_influencer',
        color_continuous_scale='plasma'
    )
    fig_category.update_layout(height=400)
    st.plotly_chart(fig_category, use_container_width=True)

# Rate Analysis
st.header("💸 Rate Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Rate Comparison by Basis")
    if not payout_details.empty:
        rate_comparison = payout_details.groupby('basis')['rate'].agg(['mean', 'median', 'std']).round(2)
        rate_comparison.columns = ['Average Rate', 'Median Rate', 'Std Deviation']
        
        st.dataframe(
            rate_comparison,
            use_container_width=True,
            column_config={
                'Average Rate': st.column_config.NumberColumn('Avg Rate (₹)', format='₹%.0f'),
                'Median Rate': st.column_config.NumberColumn('Median Rate (₹)', format='₹%.0f'),
                'Std Deviation': st.column_config.NumberColumn('Std Dev (₹)', format='₹%.0f')
            }
        )
        
        # Rate distribution by basis
        fig_rates = px.box(
            payout_details,
            x='basis',
            y='rate',
            title="Rate Distribution by Payout Basis",
            color='basis'
        )
        fig_rates.update_layout(height=300)
        st.plotly_chart(fig_rates, use_container_width=True)

with col2:
    st.subheader("Platform Efficiency")
    
    # Calculate platform efficiency metrics - REMOVED CPO FROM TABLE DISPLAY
    platform_efficiency = []
    for platform in payout_details['platform'].unique():
        platform_data = payout_details[payout_details['platform'] == platform]
        platform_posts = data['posts'][data['posts']['platform'] == platform]
        
        total_cost = platform_data['total_payout'].sum()
        total_reach = pd.to_numeric(platform_posts['reach'], errors='coerce').fillna(0).sum()
        
        platform_cpm = (total_cost / total_reach * 1000) if total_reach > 0 else 0
        
        platform_efficiency.append({
            'platform': platform,
            'total_cost': total_cost,
            'cpm': platform_cpm,
            'total_reach': total_reach
        })
    
    efficiency_df = pd.DataFrame(platform_efficiency)
    
    if not efficiency_df.empty:
        st.dataframe(
            efficiency_df[['platform', 'cpm', 'total_cost']],  # REMOVED CPO COLUMN
            use_container_width=True,
            column_config={
                'cpm': st.column_config.NumberColumn('CPM (₹)', format='₹%.2f'),
                'total_cost': st.column_config.NumberColumn('Total Cost (₹)', format='₹%.0f')
            }
        )

# Detailed Payout Tracking
st.header("📋 Detailed Payout Tracking")

# Add search functionality
search_term = st.text_input("🔍 Search Influencer", placeholder="Enter influencer name...")

# Filter by search term
if search_term:
    payout_details = payout_details[
        payout_details['name'].str.contains(search_term, case=False, na=False)
    ]

# Detailed payout table
st.subheader("Influencer Payout Details")

if not payout_details.empty:
    # Simple tracking data aggregation with error handling - REMOVED DEBUG INFO
    tracking_cols = data['tracking_data'].columns.tolist()
    
    # Check available columns and create aggregation dict
    agg_dict = {}
    if 'revenue' in tracking_cols:
        agg_dict['revenue'] = 'sum'
    if 'orders' in tracking_cols:
        agg_dict['orders'] = 'sum'
    
    if agg_dict:  # Only proceed if we have valid columns
        # Convert numeric columns and handle errors
        tracking_data_clean = data['tracking_data'].copy()
        
        if 'orders' in agg_dict:
            tracking_data_clean['orders'] = pd.to_numeric(tracking_data_clean['orders'], errors='coerce').fillna(0)
        if 'revenue' in agg_dict:
            tracking_data_clean['revenue'] = pd.to_numeric(tracking_data_clean['revenue'], errors='coerce').fillna(0)
        
        tracking_summary = tracking_data_clean.groupby('influencer_id').agg(agg_dict).reset_index()
        
        detailed_payouts = payout_details.merge(
            tracking_summary,
            on='influencer_id',
            how='left'
        ).fillna(0)
        
        # Calculate revenue per rupee spent
        detailed_payouts['revenue_per_rupee'] = np.where(
            detailed_payouts['total_payout'] > 0,
            (pd.to_numeric(detailed_payouts['revenue'], errors='coerce').fillna(0) / 
             pd.to_numeric(detailed_payouts['total_payout'], errors='coerce').fillna(1)).round(3),
            0
        )
        
        # Sort by total payout descending
        detailed_payouts = detailed_payouts.sort_values('total_payout', ascending=False)
        
        # Select columns for display - REMOVED cost_per_order and orders columns
        display_cols = ['name', 'category', 'platform', 'basis', 'rate', 'total_payout']
        
        if 'revenue' in detailed_payouts.columns:
            display_cols.append('revenue')
        if 'revenue_per_rupee' in detailed_payouts.columns:
            display_cols.append('revenue_per_rupee')
        
        available_cols = [col for col in display_cols if col in detailed_payouts.columns]
        
        st.dataframe(
            detailed_payouts[available_cols],
            use_container_width=True,
            column_config={
                'rate': st.column_config.NumberColumn('Rate (₹)', format='₹%.0f'),
                'total_payout': st.column_config.NumberColumn('Total Payout (₹)', format='₹%.0f'),
                'revenue': st.column_config.NumberColumn('Revenue (₹)', format='₹%.0f'),
                'revenue_per_rupee': st.column_config.NumberColumn('Revenue/₹', format='%.3f')
            }
        )
    else:
        # Fallback if no tracking data available
        display_cols = ['name', 'category', 'platform', 'basis', 'rate', 'total_payout']
        available_cols = [col for col in display_cols if col in payout_details.columns]
        
        st.dataframe(
            payout_details[available_cols].sort_values('total_payout', ascending=False),
            use_container_width=True,
            column_config={
                'rate': st.column_config.NumberColumn('Rate (₹)', format='₹%.0f'),
                'total_payout': st.column_config.NumberColumn('Total Payout (₹)', format='₹%.0f')
            }
        )

# Performance Insights
st.header("💡 Performance Insights")

if not payout_details.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Top Performers by Revenue")
        
        if 'detailed_payouts' in locals() and 'revenue_per_rupee' in detailed_payouts.columns:
            top_performers = detailed_payouts[detailed_payouts['revenue_per_rupee'] > 0].nlargest(5, 'revenue_per_rupee')[['name', 'total_payout', 'revenue_per_rupee']]
            if not top_performers.empty:
                st.dataframe(
                    top_performers,
                    use_container_width=True,
                    column_config={
                        'total_payout': st.column_config.NumberColumn('Payout (₹)', format='₹%.0f'),
                        'revenue_per_rupee': st.column_config.NumberColumn('Revenue/₹', format='%.2f')
                    }
                )
            else:
                st.info("No revenue data available for ranking.")
        else:
            # Show top by payout amount
            top_payouts = payout_details.nlargest(5, 'total_payout')[['name', 'total_payout', 'basis']]
            st.dataframe(
                top_payouts,
                use_container_width=True,
                column_config={
                    'total_payout': st.column_config.NumberColumn('Payout (₹)', format='₹%.0f')
                }
            )
    
    with col2:
        st.subheader("📊 Payout Summary by Basis")
        
        basis_summary = payout_details.groupby('basis').agg({
            'total_payout': ['sum', 'count', 'mean']
        }).round(0)
        basis_summary.columns = ['Total Amount', 'Count', 'Average']
        basis_summary = basis_summary.reset_index()
        
        st.dataframe(
            basis_summary,
            use_container_width=True,
            column_config={
                'Total Amount': st.column_config.NumberColumn('Total (₹)', format='₹%.0f'),
                'Average': st.column_config.NumberColumn('Average (₹)', format='₹%.0f')
            }
        )

# Budget Planning
st.header("📊 Budget Planning")

if not payout_details.empty:
    total_budget = payout_details['total_payout'].sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Budget Used",
            f"₹{total_budget:,.0f}",
            f"Across {len(payout_details)} influencers"
        )
    
    with col2:
        if 'detailed_payouts' in locals() and 'revenue' in detailed_payouts.columns:
            total_revenue = detailed_payouts['revenue'].sum()
            st.metric(
                "Total Revenue Generated",
                f"₹{total_revenue:,.0f}",
                f"ROI: {(total_revenue/total_budget*100):.1f}%" if total_budget > 0 else "No data"
            )
        else:
            st.metric(
                "Revenue Data",
                "Not Available",
                "Upload tracking data for ROI analysis"
            )
    
    with col3:
        avg_payout_per_influencer = total_budget / len(payout_details) if len(payout_details) > 0 else 0
        st.metric(
            "Average Cost per Influencer",
            f"₹{avg_payout_per_influencer:,.0f}",
            f"Across all platforms"
        )

    # Budget allocation recommendations
    st.subheader("💰 Budget Allocation by Category & Platform")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Performance by Category:**")
        category_performance = payout_details.groupby('category').agg({
            'total_payout': 'sum',
            'influencer_id': 'count'
        }).reset_index()
        category_performance['avg_per_influencer'] = category_performance['total_payout'] / category_performance['influencer_id']
        
        st.dataframe(
            category_performance,
            column_config={
                'total_payout': st.column_config.NumberColumn('Total Spend', format='₹%.0f'),
                'influencer_id': st.column_config.NumberColumn('Count', format='%d'),
                'avg_per_influencer': st.column_config.NumberColumn('Avg/Influencer', format='₹%.0f')
            }
        )
    
    with col2:
        st.write("**Performance by Platform:**")
        platform_performance = payout_details.groupby('platform').agg({
            'total_payout': 'sum',
            'influencer_id': 'count'
        }).reset_index()
        platform_performance['avg_per_influencer'] = platform_performance['total_payout'] / platform_performance['influencer_id']
        
        st.dataframe(
            platform_performance,
            column_config={
                'total_payout': st.column_config.NumberColumn('Total Spend', format='₹%.0f'),
                'influencer_id': st.column_config.NumberColumn('Count', format='%d'),
                'avg_per_influencer': st.column_config.NumberColumn('Avg/Influencer', format='₹%.0f')
            }
        )

else:
    st.info("No payout data available for the selected filters.")