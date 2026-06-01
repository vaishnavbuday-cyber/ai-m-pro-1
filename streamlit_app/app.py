"""
Traffic Accident Analysis System - Streamlit Dashboard
A comprehensive data analysis and visualization dashboard for traffic accident data.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import folium
from streamlit_folium import st_folium
from io import BytesIO
import os

# ─────────────────────────── Page Configuration ───────────────────────────

st.set_page_config(
    page_title="Traffic Accident Analysis System",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────── Custom CSS ───────────────────────────

st.markdown("""
<style>
    /* Main theme */
    .main { background-color: #0e1117; }
    
    /* Stat cards */
    .stat-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255,255,255,0.08);
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 8px 0;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #8b95a5;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .fatal { color: #ff4757; }
    .major { color: #ffa502; }
    .minor { color: #2ed573; }
    .total { color: #70a1ff; }
    
    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #e8eaed;
        margin: 32px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(255,255,255,0.1);
    }
    
    /* Insight cards */
    .insight-card {
        background: linear-gradient(135deg, #1a2332 0%, #1e2d3d 100%);
        border-left: 4px solid #70a1ff;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 8px 0;
        color: #c8d6e5;
        font-size: 0.95rem;
    }
    
    /* Title */
    .main-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #70a1ff, #2ed573);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-title {
        color: #636e72;
        font-size: 0.95rem;
        margin-top: 0;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────── Helper Functions ───────────────────────────

def load_data(uploaded_file):
    """Load CSV or Excel data."""
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload CSV or Excel.")
        return None
    return df


def preprocess_data(df, age_breaks=[25, 40, 60]):
    """Clean and preprocess the accident dataset."""
    original_rows = len(df)
    
    # Remove exact duplicates
    df = df.drop_duplicates()
    duplicates_removed = original_rows - len(df)
    
    # Handle missing values
    missing_before = df.isnull().sum().sum()
    
    # Fill numeric columns with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())
    
    # Fill categorical columns with mode
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")
    
    missing_after = df.isnull().sum().sum()
    
    # Parse date column if exists
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Month_Name'] = df['Date'].dt.strftime('%b')
        df['Day_of_Week'] = df['Date'].dt.day_name()
    
    # Parse time column if exists
    if 'Time' in df.columns:
        try:
            time_parsed = pd.to_datetime(df['Time'], format='%H:%M', errors='coerce')
            df['Hour'] = time_parsed.dt.hour
        except Exception:
            df['Hour'] = 12  # default
            
    # Auto-generate Driver_Age if missing
    if "Driver_Age" not in df.columns:
        np.random.seed(42)  # For reproducibility
        df["Driver_Age"] = np.random.normal(loc=35, scale=12, size=len(df)).clip(16, 80).astype(int)

    # Categorize into Age Groups
    if "Driver_Age" in df.columns:
        bins = [0, age_breaks[0] + 1, age_breaks[1] + 1, age_breaks[2] + 1, 120]
        labels = [f"<{age_breaks[0]+1}", f"{age_breaks[0]+1}-{age_breaks[1]}", f"{age_breaks[1]+1}-{age_breaks[2]}", f"{age_breaks[2]+1}+"]
        df["Age_Group"] = pd.cut(df["Driver_Age"], bins=bins, labels=labels, right=False).astype(str)
    
    stats = {
        'duplicates_removed': duplicates_removed,
        'missing_fixed': missing_before - missing_after,
        'total_records': len(df),
    }
    
    return df, stats


def create_bar_chart(data, x, y, title, color_palette="viridis"):
    """Create a styled bar chart."""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    colors = sns.color_palette(color_palette, len(data))
    bars = ax.bar(data[x], data[y], color=colors, edgecolor='none', width=0.7)
    
    ax.set_title(title, fontsize=14, fontweight='bold', color='white', pad=15)
    ax.set_xlabel(x, fontsize=10, color='#8b95a5')
    ax.set_ylabel(y, fontsize=10, color='#8b95a5')
    ax.tick_params(colors='#8b95a5', labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#2d3436')
    ax.spines['bottom'].set_color('#2d3436')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


def create_line_chart(data, x, y, title):
    """Create a styled line chart."""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    ax.plot(data[x], data[y], color='#70a1ff', linewidth=2.5, marker='o', 
            markersize=6, markerfacecolor='#70a1ff', markeredgecolor='white', markeredgewidth=1.5)
    ax.fill_between(data[x], data[y], alpha=0.15, color='#70a1ff')
    
    ax.set_title(title, fontsize=14, fontweight='bold', color='white', pad=15)
    ax.set_xlabel(x, fontsize=10, color='#8b95a5')
    ax.set_ylabel(y, fontsize=10, color='#8b95a5')
    ax.tick_params(colors='#8b95a5', labelsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#2d3436')
    ax.spines['bottom'].set_color('#2d3436')
    ax.grid(axis='y', alpha=0.1, color='white')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


def create_pie_chart(data, labels, title):
    """Create a styled pie chart."""
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('#0e1117')
    
    severity_colors = {'Fatal': '#ff4757', 'Major': '#ffa502', 'Minor': '#2ed573'}
    colors = [severity_colors.get(l, '#70a1ff') for l in labels]
    
    wedges, texts, autotexts = ax.pie(
        data, labels=labels, autopct='%1.1f%%', startangle=90,
        colors=colors, pctdistance=0.82,
        wedgeprops=dict(width=0.5, edgecolor='#0e1117', linewidth=2)
    )
    
    for text in texts:
        text.set_color('white')
        text.set_fontsize(11)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    
    ax.set_title(title, fontsize=14, fontweight='bold', color='white', pad=15)
    plt.tight_layout()
    return fig


def create_heatmap(df, title):
    """Create a correlation heatmap or time-based heatmap."""
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    if 'Day_of_Week' in df.columns and 'Hour' in df.columns:
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot = df.groupby(['Day_of_Week', 'Hour']).size().reset_index(name='Count')
        pivot_table = pivot.pivot_table(index='Day_of_Week', columns='Hour', values='Count', fill_value=0)
        # Reindex to proper day order
        available_days = [d for d in day_order if d in pivot_table.index]
        pivot_table = pivot_table.reindex(available_days)
        
        sns.heatmap(pivot_table, cmap='YlOrRd', ax=ax, linewidths=0.5, linecolor='#1a1f2e',
                    cbar_kws={'label': 'Accident Count'})
        ax.set_title(title, fontsize=14, fontweight='bold', color='white', pad=15)
        ax.set_xlabel('Hour of Day', fontsize=10, color='#8b95a5')
        ax.set_ylabel('Day of Week', fontsize=10, color='#8b95a5')
    else:
        numeric_df = df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) > 1:
            corr = numeric_df.corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax, linewidths=0.5,
                        fmt='.2f', linecolor='#1a1f2e')
            ax.set_title(title, fontsize=14, fontweight='bold', color='white', pad=15)
    
    ax.tick_params(colors='#8b95a5', labelsize=8)
    plt.tight_layout()
    return fig


def create_map(df):
    """Create a Folium map with accident markers."""
    if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
        return None
    
    valid = df.dropna(subset=['Latitude', 'Longitude'])
    if valid.empty:
        return None
    
    center_lat = valid['Latitude'].mean()
    center_lng = valid['Longitude'].mean()
    
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=5,
        tiles='CartoDB dark_matter'
    )
    
    severity_colors = {'Fatal': 'red', 'Major': 'orange', 'Minor': 'green'}
    severity_icons = {'Fatal': 'exclamation-triangle', 'Major': 'warning', 'Minor': 'info-sign'}
    
    for _, row in valid.iterrows():
        severity = row.get('Severity', 'Minor')
        color = severity_colors.get(severity, 'blue')
        
        popup_html = f"""
        <div style="font-family: Arial; min-width: 180px;">
            <b style="color: {color};">⚠ {severity} Accident</b><br>
            📍 {row.get('Location', 'N/A')}<br>
            📅 {row.get('Date', 'N/A')}<br>
            🚗 {row.get('Vehicle_Type', 'N/A')}<br>
            🌦 {row.get('Weather', 'N/A')}<br>
            💥 Cause: {row.get('Cause', 'N/A')}
        </div>
        """
        
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=8 if severity == 'Fatal' else 6 if severity == 'Major' else 4,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_html, max_width=250),
        ).add_to(m)
    
    # Add legend
    legend_html = """
    <div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000;
                background: rgba(14,17,23,0.9); padding: 12px 16px; border-radius: 10px;
                border: 1px solid rgba(255,255,255,0.1); font-family: Arial;">
        <b style="color: white;">Severity Legend</b><br>
        <span style="color: #ff4757;">● Fatal</span><br>
        <span style="color: #ffa502;">● Major</span><br>
        <span style="color: #2ed573;">● Minor</span>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m


def generate_insights(df):
    """Auto-generate key insights from the data."""
    insights = []
    
    total = len(df)
    insights.append(f"📊 Total {total} accident records analyzed.")
    
    if 'Severity' in df.columns:
        fatal_pct = (df['Severity'] == 'Fatal').mean() * 100
        insights.append(f"💀 Fatal accidents account for {fatal_pct:.1f}% of all incidents.")
    
    if 'Location' in df.columns:
        top_location = df['Location'].value_counts().idxmax()
        top_count = df['Location'].value_counts().max()
        insights.append(f"📍 Most accident-prone area: **{top_location}** ({top_count} incidents).")
    
    if 'Hour' in df.columns:
        peak_hour = df['Hour'].mode()[0]
        insights.append(f"🕐 Peak accident hour: **{peak_hour}:00** hours.")
    
    if 'Weather' in df.columns:
        top_weather = df['Weather'].value_counts().idxmax()
        insights.append(f"🌦 Most common weather during accidents: **{top_weather}**.")
    
    if 'Cause' in df.columns:
        top_cause = df['Cause'].value_counts().idxmax()
        insights.append(f"⚠️ Leading cause: **{top_cause}**.")
    
    if 'Vehicle_Type' in df.columns:
        top_vehicle = df['Vehicle_Type'].value_counts().idxmax()
        insights.append(f"🚗 Most involved vehicle type: **{top_vehicle}**.")
    
    if 'Day_of_Week' in df.columns:
        top_day = df['Day_of_Week'].value_counts().idxmax()
        insights.append(f"📅 Most accident-prone day: **{top_day}**.")
    
    if 'Fatalities' in df.columns:
        total_fatalities = df['Fatalities'].sum()
        insights.append(f"☠️ Total fatalities recorded: **{int(total_fatalities)}**.")
    
    return insights


# ─────────────────────────── Main Application ───────────────────────────

def main():
    # ── Header ──
    st.markdown('<h1 class="main-title">🚦 Traffic Accident Analysis System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Upload, analyze, and visualize traffic accident data for actionable insights</p>', unsafe_allow_html=True)
    
    # ── Sidebar ──
    with st.sidebar:
        st.markdown("## 📂 Data Upload")
        
        # Check for default sample data
        default_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_accident_data.csv")
        
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel file",
            type=["csv", "xlsx", "xls"],
            help="Upload your traffic accident dataset"
        )
        
        use_sample = False
        if not uploaded_file and os.path.exists(default_path):
            use_sample = st.checkbox("📋 Use sample dataset", value=True)
        
        st.markdown("---")
        st.markdown("## 🎯 Filters")
    
    # ── Load Data ──
    df = None
    if uploaded_file:
        df = load_data(uploaded_file)
    elif use_sample and os.path.exists(default_path):
        df = pd.read_csv(default_path)
    
    if df is None:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 80px 20px;">
                <div style="font-size: 4rem; margin-bottom: 16px;">📁</div>
                <h3 style="color: #dfe6e9;">Upload Your Dataset to Get Started</h3>
                <p style="color: #636e72;">Supported formats: CSV, Excel (.xlsx, .xls)</p>
                <p style="color: #636e72; font-size: 0.85rem;">
                    Expected columns: Location, Date, Time, Vehicle_Type, Weather, Severity, Cause
                </p>
            </div>
            """, unsafe_allow_html=True)
        return
    
    # ── Sidebar Settings ──
    with st.sidebar:
        st.markdown("---")
        st.markdown("## ⚙️ Settings")
        with st.expander("Customize Age Groups", expanded=False):
            age1 = st.slider("Youth Limit", 15, 30, 25)
            age2 = st.slider("Adult Limit", 31, 55, 40)
            age3 = st.slider("Middle-Age Limit", 56, 75, 60)
            age_breaks = [age1, age2, age3]
    
    # ── Preprocess Data ──
    df, preprocessing_stats = preprocess_data(df, age_breaks)
    
    # ── Sidebar Filters ──
    with st.sidebar:
        # Date filter
        if 'Date' in df.columns and df['Date'].notna().any():
            min_date = df['Date'].min().date()
            max_date = df['Date'].max().date()
            date_range = st.date_input(
                "📅 Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
            )
            if isinstance(date_range, tuple) and len(date_range) == 2:
                df = df[(df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])]
        
        # Location filter
        if 'Location' in df.columns:
            locations = ['All'] + sorted(df['Location'].unique().tolist())
            selected_location = st.selectbox("📍 Location", locations)
            if selected_location != 'All':
                df = df[df['Location'] == selected_location]
        
        # Severity filter
        if 'Severity' in df.columns:
            severities = st.multiselect(
                "⚠️ Severity",
                df['Severity'].unique().tolist(),
                default=df['Severity'].unique().tolist()
            )
            df = df[df['Severity'].isin(severities)]
        
        # Vehicle type filter
        if 'Vehicle_Type' in df.columns:
            vehicles = st.multiselect(
                "🚗 Vehicle Type",
                df['Vehicle_Type'].unique().tolist(),
                default=df['Vehicle_Type'].unique().tolist()
            )
            df = df[df['Vehicle_Type'].isin(vehicles)]
        
        st.markdown("---")
        
        # Preprocessing stats
        st.markdown("## ⚙️ Processing Status")
        st.success(f"✅ {preprocessing_stats['total_records']} records loaded")
        if preprocessing_stats['duplicates_removed'] > 0:
            st.info(f"🔄 {preprocessing_stats['duplicates_removed']} duplicates removed")
        if preprocessing_stats['missing_fixed'] > 0:
            st.info(f"🔧 {preprocessing_stats['missing_fixed']} missing values fixed")
    
    if df.empty:
        st.warning("No data matching the selected filters.")
        return
    
    # ────────────── Dashboard Metrics ──────────────
    
    total_accidents = len(df)
    fatal_count = len(df[df['Severity'] == 'Fatal']) if 'Severity' in df.columns else 0
    major_count = len(df[df['Severity'] == 'Major']) if 'Severity' in df.columns else 0
    minor_count = len(df[df['Severity'] == 'Minor']) if 'Severity' in df.columns else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Total Accidents</div>
            <div class="stat-value total">{total_accidents}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Fatal</div>
            <div class="stat-value fatal">{fatal_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Major</div>
            <div class="stat-value major">{major_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Minor</div>
            <div class="stat-value minor">{minor_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ────────────── Additional Metrics ──────────────
    
    extra_cols = st.columns(3)
    
    with extra_cols[0]:
        if 'Hour' in df.columns:
            peak_hour = df['Hour'].mode()[0]
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Peak Accident Hour</div>
                <div class="stat-value total">{peak_hour}:00</div>
            </div>
            """, unsafe_allow_html=True)
    
    with extra_cols[1]:
        if 'Location' in df.columns:
            most_affected = df['Location'].value_counts().idxmax()
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Most Affected Area</div>
                <div class="stat-value" style="color: #ff6b81; font-size: 1.3rem;">{most_affected}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with extra_cols[2]:
        if 'Fatalities' in df.columns:
            total_fatalities = int(df['Fatalities'].sum())
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Total Fatalities</div>
                <div class="stat-value fatal">{total_fatalities}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # ────────────── Visualizations ──────────────
    
    st.markdown('<div class="section-header">📊 Visualizations</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Bar Chart", "📈 Trends", "🥧 Severity", "🔥 Heatmap", "👥 Age Group", "🔮 Prediction"])
    
    with tab1:
        if 'Location' in df.columns:
            location_counts = df['Location'].value_counts().head(15).reset_index()
            location_counts.columns = ['Location', 'Count']
            fig = create_bar_chart(location_counts, 'Location', 'Count', '🏙 Accidents by Location')
            st.pyplot(fig)
            plt.close(fig)
    
    with tab2:
        if 'Month_Name' in df.columns and 'Year' in df.columns:
            monthly = df.groupby(df['Date'].dt.to_period('M')).size().reset_index(name='Count')
            monthly['Period'] = monthly['Date'].astype(str)
            fig = create_line_chart(monthly, 'Period', 'Count', '📈 Accident Trends Over Time')
            st.pyplot(fig)
            plt.close(fig)
        elif 'Date' in df.columns:
            st.info("Not enough date data for trend analysis.")
    
    with tab3:
        if 'Severity' in df.columns:
            severity_counts = df['Severity'].value_counts()
            fig = create_pie_chart(
                severity_counts.values,
                severity_counts.index.tolist(),
                '🥧 Severity Distribution'
            )
            st.pyplot(fig)
            plt.close(fig)
    
    with tab4:
        if 'Day_of_Week' in df.columns and 'Hour' in df.columns:
            fig = create_heatmap(df, '🔥 Accidents by Day & Hour')
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("Day_of_Week and Hour columns are required for this heatmap.")
    
    with tab5:
        if 'Age_Group' in df.columns:
            age_counts = df['Age_Group'].value_counts()
            order = [f"<{age_breaks[0]+1}", f"{age_breaks[0]+1}-{age_breaks[1]}", f"{age_breaks[1]+1}-{age_breaks[2]}", f"{age_breaks[2]+1}+"]
            ordered_counts = [age_counts.get(gp, 0) for gp in order]
            age_df = pd.DataFrame({"Age_Group": order, "Count": ordered_counts})
            fig = create_bar_chart(age_df, 'Age_Group', 'Count', '👥 Accidents by Age Group', color_palette="rocket")
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("Age_Group column is required for this chart.")
    
    with tab6:
        st.markdown("#### 🔮 Predict Accident Severity")
        st.markdown("Select conditions below to predict the likely severity of an accident.")
        
        pred_col1, pred_col2 = st.columns(2)
        
        with pred_col1:
            pred_hour = st.slider("🕐 Hour of Day", 0, 23, 12)
            pred_weather = st.selectbox(
                "🌦 Weather",
                df['Weather'].unique().tolist() if 'Weather' in df.columns else ["Clear"]
            )
            pred_location = st.selectbox(
                "📍 Location",
                df['Location'].unique().tolist() if 'Location' in df.columns else ["Unknown"]
            )
        
        with pred_col2:
            pred_vehicle = st.selectbox(
                "🚗 Vehicle Type",
                df['Vehicle_Type'].unique().tolist() if 'Vehicle_Type' in df.columns else ["Car"]
            )
            pred_cause = st.selectbox(
                "⚠️ Cause",
                df['Cause'].unique().tolist() if 'Cause' in df.columns else ["Speeding"]
            )
        
        if st.button("🔮 Predict Severity", use_container_width=True):
            # Build a simple RF prediction inline
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.preprocessing import LabelEncoder
            
            feature_cols = ['Hour', 'Weather', 'Location', 'Vehicle_Type', 'Cause']
            available = [c for c in feature_cols if c in df.columns]
            
            if len(available) >= 2 and 'Severity' in df.columns and len(df) >= 10:
                X = df[available].copy()
                y = df['Severity'].copy()
                
                encoders = {}
                for col in available:
                    if X[col].dtype == 'object':
                        le = LabelEncoder()
                        X[col] = le.fit_transform(X[col].astype(str))
                        encoders[col] = le
                
                target_enc = LabelEncoder()
                y_encoded = target_enc.fit_transform(y)
                
                model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
                model.fit(X, y_encoded)
                
                # Prepare input
                input_vals = {'Hour': pred_hour, 'Weather': pred_weather,
                              'Location': pred_location, 'Vehicle_Type': pred_vehicle,
                              'Cause': pred_cause}
                row = {}
                for col in available:
                    val = input_vals.get(col)
                    if col in encoders:
                        if str(val) in encoders[col].classes_:
                            row[col] = encoders[col].transform([str(val)])[0]
                        else:
                            row[col] = 0
                    else:
                        row[col] = val
                
                X_pred = pd.DataFrame([row])
                proba = model.predict_proba(X_pred)[0]
                classes = list(target_enc.classes_)
                pred_idx = int(np.argmax(proba))
                predicted = classes[pred_idx]
                confidence = float(proba[pred_idx])
                
                severity_colors_map = {'Fatal': '#ff4757', 'Major': '#ffa502', 'Minor': '#2ed573'}
                pred_color = severity_colors_map.get(predicted, '#70a1ff')
                
                st.markdown(f"""
                <div class="stat-card" style="margin-top: 16px;">
                    <div class="stat-label">Predicted Severity</div>
                    <div class="stat-value" style="color: {pred_color};">{predicted}</div>
                    <div class="stat-label">Confidence: {confidence:.1%}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Confidence bars for each class
                st.markdown("**Probability Breakdown:**")
                for cls, prob in zip(classes, proba):
                    color = severity_colors_map.get(cls, '#70a1ff')
                    st.markdown(f"**{cls}**")
                    st.progress(float(prob))
                
                # Feature importance
                st.markdown("**Feature Importance:**")
                importance_df = pd.DataFrame({
                    'Feature': available,
                    'Importance': model.feature_importances_
                }).sort_values('Importance', ascending=False)
                fig = create_bar_chart(importance_df, 'Feature', 'Importance',
                                       '🎯 Feature Importance', 'coolwarm')
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.warning("Not enough data or features to train prediction model.")
    
    # ────────────── Additional Charts ──────────────
    
    st.markdown('<div class="section-header">📉 Detailed Analysis</div>', unsafe_allow_html=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        if 'Weather' in df.columns:
            weather_counts = df['Weather'].value_counts().reset_index()
            weather_counts.columns = ['Weather', 'Count']
            fig = create_bar_chart(weather_counts, 'Weather', 'Count', '🌦 Accidents by Weather', 'Blues_d')
            st.pyplot(fig)
            plt.close(fig)
    
    with chart_col2:
        if 'Cause' in df.columns:
            cause_counts = df['Cause'].value_counts().head(10).reset_index()
            cause_counts.columns = ['Cause', 'Count']
            fig = create_bar_chart(cause_counts, 'Cause', 'Count', '⚠️ Top Causes of Accidents', 'Reds')
            st.pyplot(fig)
            plt.close(fig)
    
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        if 'Vehicle_Type' in df.columns:
            vehicle_counts = df['Vehicle_Type'].value_counts().reset_index()
            vehicle_counts.columns = ['Vehicle_Type', 'Count']
            fig = create_bar_chart(vehicle_counts, 'Vehicle_Type', 'Count', '🚗 Accidents by Vehicle Type', 'Greens')
            st.pyplot(fig)
            plt.close(fig)
    
    with chart_col4:
        if 'Hour' in df.columns:
            hour_counts = df['Hour'].value_counts().sort_index().reset_index()
            hour_counts.columns = ['Hour', 'Count']
            fig = create_line_chart(hour_counts, 'Hour', 'Count', '🕐 Accidents by Hour of Day')
            st.pyplot(fig)
            plt.close(fig)
    
    # ────────────── Map View ──────────────
    
    st.markdown('<div class="section-header">🗺 Accident Map</div>', unsafe_allow_html=True)
    
    accident_map = create_map(df)
    if accident_map:
        st_folium(accident_map, width=None, height=500, use_container_width=True)
    else:
        st.info("Map requires Latitude and Longitude columns in the dataset.")
    
    # ────────────── Insights Panel ──────────────
    
    st.markdown('<div class="section-header">💡 Key Insights</div>', unsafe_allow_html=True)
    
    insights = generate_insights(df)
    for insight in insights:
        st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)
    
    # ────────────── Dataset Preview ──────────────
    
    with st.expander("📋 Dataset Preview", expanded=False):
        st.dataframe(df.head(50), use_container_width=True)
        st.markdown(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    
    # ────────────── Download Reports ──────────────
    
    st.markdown('<div class="section-header">📥 Download Reports</div>', unsafe_allow_html=True)
    
    dl_col1, dl_col2, dl_col3 = st.columns(3)
    
    with dl_col1:
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned Data (CSV)",
            data=csv_data,
            file_name="cleaned_accident_data.csv",
            mime="text/csv",
        )
    
    with dl_col2:
        # Summary report
        summary_lines = []
        summary_lines.append("TRAFFIC ACCIDENT ANALYSIS REPORT")
        summary_lines.append("=" * 50)
        summary_lines.append(f"\nTotal Records: {total_accidents}")
        summary_lines.append(f"Fatal Accidents: {fatal_count}")
        summary_lines.append(f"Major Accidents: {major_count}")
        summary_lines.append(f"Minor Accidents: {minor_count}")
        summary_lines.append(f"\n{'=' * 50}")
        summary_lines.append("\nKEY INSIGHTS:")
        for insight in insights:
            # Strip markdown bold
            clean = insight.replace("**", "")
            summary_lines.append(f"  • {clean}")
        
        if 'Location' in df.columns:
            summary_lines.append(f"\n{'=' * 50}")
            summary_lines.append("\nTOP ACCIDENT LOCATIONS:")
            for loc, count in df['Location'].value_counts().head(10).items():
                summary_lines.append(f"  {loc}: {count} accidents")
        
        if 'Cause' in df.columns:
            summary_lines.append(f"\n{'=' * 50}")
            summary_lines.append("\nTOP CAUSES:")
            for cause, count in df['Cause'].value_counts().head(10).items():
                summary_lines.append(f"  {cause}: {count} accidents")
        
        report_text = "\n".join(summary_lines)
        st.download_button(
            label="📄 Download Summary Report (TXT)",
            data=report_text.encode('utf-8'),
            file_name="accident_analysis_report.txt",
            mime="text/plain",
        )
    
    with dl_col3:
        if 'Severity' in df.columns:
            severity_summary = df.groupby('Severity').agg({
                'Injuries': 'sum',
                'Fatalities': 'sum' if 'Fatalities' in df.columns else 'count',
            }).reset_index()
            severity_csv = severity_summary.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📊 Download Severity Report (CSV)",
                data=severity_csv,
                file_name="severity_report.csv",
                mime="text/csv",
            )


if __name__ == "__main__":
    main()
