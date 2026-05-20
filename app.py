import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 0. Page Configuration
# ==========================================
st.set_page_config(page_title="BI Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 1. Dark Mode Adaptation CSS
# ==========================================
st.markdown("""
<style>
    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #FAFAFA; 
        border-right: 1px solid #E5E7EB; 
    }
    
    /* Metric Card Styling */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #F3F4F6;
        padding: 20px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-top: 4px solid #1E3A8A; 
        transition: all 0.3s ease;
    }

    /* Dark Mode Adaptation */
    @media (prefers-color-scheme: dark) {
        [data-testid="stSidebar"] {
            background-color: #111827 !important;
            border-right: 1px solid #374151 !important;
        }
        div[data-testid="metric-container"] {
            background-color: #1F2937 !important;
            border: 1px solid #374151 !important;
            border-top: 4px solid #3B82F6 !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        }
        div[data-testid="metric-container"] label, 
        div[data-testid="metric-container"] [data-testid="stMetricValue"],
        div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
            color: #F9FAFB !important;
        }
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    html, body, [class*="css"] { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Data Loading & Palette
# ==========================================
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ Missing Data Source: data.csv")
    st.stop()

corp_colors = ['#1E3A8A', '#059669', '#D97706', '#DC2626', '#9CA3AF']

def apply_corporate_theme(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#374151'),
        xaxis=dict(showgrid=True, gridcolor='#F3F4F6', linecolor='#D1D5DB', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='#F3F4F6', linecolor='#D1D5DB', zeroline=False),
        margin=dict(t=40, b=40, l=40, r=40)
    )
    return fig

# ==========================================
# 3. Sidebar Navigation
# ==========================================
with st.sidebar:
    st.markdown("### 📊 Strategic Analytics")
    st.markdown("---")
    page = st.radio(
        "Index:",
        ["1. Executive Overview", 
         "2. Fulfillment Model", 
         "3. Strategic Group Map", 
         "4. Market Simulation"]
    )
    st.markdown("---")
    st.caption("© 2026 Competitor Intelligence Team of XJTLU")
    st.caption("Data Source: Simulated proxy data based on industry benchmarks. For demonstration purposes only.")

# ==========================================
# Module 1: Overview
# ==========================================
if page == "1. Executive Overview":
    st.title("Executive Overview 🌐")
    st.markdown("KPI benchmarking across four major fresh grocery e-commerce platforms.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    display_df = df[df['Platform'] != 'Others'].reset_index(drop=True)
    
    cols = st.columns(4)
    for i, row in display_df.iterrows():
        if i < 4: 
            with cols[i]:
                st.metric(label=f"🏢 {row['Platform']}", 
                          value=f"{row['Market_Share_Pct']}%", 
                          delta=f"Rating: {row['User_Rating']}",
                          delta_color="normal")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("📚 Methodology & Data Assumptions", expanded=False):
        st.markdown("""
        * **Data Sourcing:** This dashboard utilizes Industry Proxy Data, establishing benchmarks based on the public business models of each platform.
        * **Metric Definitions:** * `Estimated_AOV`: Estimated Average Order Value.
            * `Price_Index`: Weighted index of platform prices relative to the market average (Baseline = 100).
        """)
        
    st.subheader("Raw Dataset")
    st.dataframe(df.style.highlight_max(subset=['Market_Share_Pct', 'User_Rating'], color='#D1FAE5'), use_container_width=True)

# ==========================================
# Module 2: Efficiency
# ==========================================
elif page == "2. Fulfillment Model":
    st.title("Fulfillment vs. Cost 🚚")
    st.markdown("Physical world trade-offs: Analyzing the effect of last-mile delivery speed on platform profitability models.")
    
    y_axis_choice = st.selectbox("🎯 Evaluation Metric:", ["Estimated_AOV", "Free_Delivery_Threshold"])
    
    plot_df = df[df['Platform'] != 'Others']
    
    fig = px.scatter(
        plot_df, x="Delivery_Time_mins", y=y_axis_choice, size="SKU_Count", color="Platform",
        hover_name="Platform", text="Platform",
        color_discrete_sequence=corp_colors[:4], 
        labels={
            "Delivery_Time_mins": "Avg. Latency (mins)", 
            "Estimated_AOV": "Est. AOV (RMB)", 
            "Free_Delivery_Threshold": "Free Delivery Threshold (RMB)"
        }
    )
    fig.update_traces(textposition='top center', marker=dict(line=dict(width=1.5, color='white')))
    fig = apply_corporate_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Module 3: Positioning
# ==========================================
elif page == "3. Strategic Group Map":
    st.title("Strategic Group Map 🎯")
    st.markdown("Multi-dimensional niche mapping: Clustering analysis based on SKU coverage and pricing capability.")
    
    plot_df = df[df['Platform'] != 'Others']
    
    fig2 = px.scatter(
        plot_df, x="SKU_Count", y="Price_Index", size="Market_Share_Pct", color="Platform",
        hover_name="Platform", text="Platform", log_x=True,
        color_discrete_sequence=corp_colors[:4],
        labels={
            "SKU_Count": "SKU Diversity (Log Scale)", 
            "Price_Index": "Price Index"
        }
    )
    fig2.update_traces(textposition='bottom right', marker=dict(line=dict(width=1.5, color='white')))
    fig2 = apply_corporate_theme(fig2)
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# Module 4: Simulation
# ==========================================
elif page == "4. Market Simulation":
    st.title("Market Simulation Engine 🕹️")
    st.markdown("Hypothetical scenario deduction based on the Discrete Utility Model.")
    
    @st.fragment
    def render_simulation_sandbox():
        col1, col2 = st.columns([1.2, 2.8], gap="large")
        
        with col1:
            st.markdown("#### 🎛️ Control Panel")
            st.caption("Adjust variables to reconstruct landscape")
            aldi_sku = st.slider("Aldi: SKU Expansion", 1500, 6000, 1500, 10)
            dingdong_price = st.slider("Dingdong: Price Drop Index", 80, 120, 105, 1)
            freshippo_time = st.slider("Freshippo: Speed-up (mins)", 15, 45, 30, 1)
            
            st.markdown("---")
            st.markdown("#### 🧮 Algorithm")
            st.caption("Market share reallocation is based on utility gravity formula:")
            st.latex(r"U_i = \alpha \left(\frac{SKU_i}{1k}\right) + \beta \left(\frac{100}{Price_i}\right) + \gamma \left(\frac{100}{Time_i}\right)")
            
        with col2:
            sim_df = df.copy()
            sim_df[['SKU_Count', 'Price_Index', 'Delivery_Time_mins']] = sim_df[['SKU_Count', 'Price_Index', 'Delivery_Time_mins']].astype(float)
            
            sim_df.loc[sim_df['Platform'] == 'Aldi', 'SKU_Count'] = aldi_sku
            sim_df.loc[sim_df['Platform'] == 'Dingdong', 'Price_Index'] = dingdong_price
            sim_df.loc[sim_df['Platform'] == 'Freshippo', 'Delivery_Time_mins'] = freshippo_time
            
            sim_df['Utility'] = (sim_df['SKU_Count']/1000.0)*10.0 + (100.0/sim_df['Price_Index'])*60.0 + (100.0/sim_df['Delivery_Time_mins'])*30.0
            sim_df['Simulated_Share'] = (sim_df['Utility'] / sim_df['Utility'].sum()) * 100.0
            
            fig_pie = px.pie(
                sim_df, values='Simulated_Share', names='Platform', hole=0.5,
                color='Platform', color_discrete_sequence=corp_colors,
                title="Simulated Market Share (%)"
            )
            
            fig_pie.update_traces(
                textposition='outside', textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Share: %{percent}<extra></extra>',
                textfont_size=14,
                sort=False
            )
            
            fig_pie.update_layout(
                height=650, margin=dict(t=80, b=40, l=80, r=80),
                showlegend=False, 
                annotations=[dict(text='Market<br>Share', x=0.5, y=0.5, font_size=20, showarrow=False)]
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)
            
            main_players = sim_df[sim_df['Platform'] != 'Others']
            if not main_players.empty:
                top_platform = main_players.loc[main_players['Simulated_Share'].idxmax(), 'Platform']
                top_share = main_players['Simulated_Share'].max()
                others_share = sim_df.loc[sim_df['Platform'] == 'Others', 'Simulated_Share'].values[0]
                
                st.info(f"📌 **Strategic Insight:** \n\nUnder current parameters, **{top_platform}** captures maximum gravity (Expected Share: **{top_share:.1f}%**). Fragmentation (Others) is compressed to **{others_share:.1f}%**.")

    render_simulation_sandbox()
