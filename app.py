import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 0. 核心网页配置 / Page Configuration
# ==========================================
st.set_page_config(page_title="商业分析仪表板 / Business Analytics Dashboard", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 1. 样式美化 / Custom CSS
# ==========================================
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #f8f9fa; }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #2e7d32;
        transition: transform 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
    html, body, [class*="css"]  { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 数据读取与配色配置 / Data Loading & Colors
# ==========================================
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("找不到 data.csv 文件！请确保它和 app.py 在同一目录下。 / Cannot find data.csv!")
    st.stop()

brand_colors = ['#2e7d32', '#fbc02d', '#1565c0', '#c62828', '#9e9e9e']

# ==========================================
# 3. 侧边栏导航 / Sidebar Navigation
# ==========================================
with st.sidebar:
    st.markdown("### 📊 导航面板 / Navigation")
    st.markdown("---")
    page = st.radio(
        "请选择分析模块 / Select Module：",
        ["1. 概览大屏 (Overview)", 
         "2. 履约与成本分析 (Efficiency)", 
         "3. 战略群体定位 (Positioning)", 
         "4. 机会与矩阵模拟 (Simulation)"]
    )
    st.markdown("---")
    # 项目信息 / Project Info
    st.caption("竞争对手情报分析小组 / Competitor Intelligence Team")
    # 按照要求添加的注脚 / Footnote as requested
    st.markdown("<br><br>", unsafe_allow_html=True) # 增加一些间距推到底部
    st.caption("ℹ️ **数据说明 / Data Note:**")
    st.caption("Data Source: Simulated proxy data based on industry benchmarks. For demonstration purposes only.")
    st.caption("数据来源：基于行业基准的模拟估算数据。仅作演示用途。")

# ==========================================
# 模块 1：概览大屏 / Module 1: Overview
# ==========================================
if page == "1. 概览大屏 (Overview)":
    st.title("宏观市场概览 / Macro Market Overview 🌐")
    st.markdown("快速对比四大核心生鲜平台的关键业绩指标。 / Quick comparison of KPIs across four major platforms.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    display_df = df[df['Platform'] != 'Others'].reset_index(drop=True)
    
    cols = st.columns(4)
    for i, row in display_df.iterrows():
        if i < 4: 
            with cols[i]:
                st.metric(label=row['Platform'], 
                          value=f"{row['Market_Share_Pct']}% 份额 / Share", 
                          delta=f"综合评分 / Rating: {row['User_Rating']}",
                          delta_color="normal")
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.subheader("底层数据明细表 / Underlying Data Table")
    st.dataframe(df.style.highlight_max(subset=['Market_Share_Pct', 'User_Rating'], color='lightgreen'), use_container_width=True)

# ==========================================
# 模块 2：履约与成本分析 / Module 2: Efficiency
# ==========================================
elif page == "2. 履约与成本分析 (Efficiency)":
    st.title("履约时效 vs. 成本结构 / Delivery Time vs. Cost Structure 🚚")
    st.markdown("分析配送速度如何影响平台的客单价与免邮门槛。 / Analyze how delivery speed impacts AOV and free delivery thresholds.")
    
    y_axis_choice = st.selectbox("🎯 选择 Y 轴指标对比 / Select Y-Axis Metric:", ["Estimated_AOV", "Free_Delivery_Threshold"])
    
    plot_df = df[df['Platform'] != 'Others']
    
    fig = px.scatter(
        plot_df, x="Delivery_Time_mins", y=y_axis_choice, size="SKU_Count", color="Platform",
        hover_name="Platform", text="Platform",
        color_discrete_sequence=brand_colors[:4], 
        labels={
            "Delivery_Time_mins": "平均配送时效 / Avg. Delivery Time (mins)", 
            "Estimated_AOV": "预估客单价 / Est. AOV (RMB)", 
            "Free_Delivery_Threshold": "免邮门槛 / Free Delivery Threshold (RMB)"
        }
    )
    fig.update_traces(textposition='top center', marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', yaxis=(dict(showgrid=True, gridcolor='#e0e0e0')), xaxis=(dict(showgrid=True, gridcolor='#e0e0e0')))
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 模块 3：战略群体定位 / Module 3: Positioning
# ==========================================
elif page == "3. 战略群体定位 (Positioning)":
    st.title("市场战略群体图 / Strategic Group Map 🎯")
    st.markdown("通过 SKU 丰富度与价格指数，寻找平台的市场生态位。 / Identify market niches through SKU diversity and price indices.")
    
    plot_df = df[df['Platform'] != 'Others']
    
    fig2 = px.scatter(
        plot_df, x="SKU_Count", y="Price_Index", size="Market_Share_Pct", color="Platform",
        hover_name="Platform", text="Platform", log_x=True,
        color_discrete_sequence=brand_colors[:4],
        labels={
            "SKU_Count": "SKU 丰富度 / SKU Diversity (Log Scale)", 
            "Price_Index": "价格指数 / Price Index (Premium Level)"
        }
    )
    fig2.update_traces(textposition='bottom right', marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', yaxis=(dict(showgrid=True, gridcolor='#e0e0e0')), xaxis=(dict(showgrid=True, gridcolor='#e0e0e0')))
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# 模块 4：机会与矩阵模拟 / Module 4: Simulation
# ==========================================
elif page == "4. 机会与矩阵模拟 (Simulation)":
    st.title("动态市场份额模拟沙盘 / Dynamic Market Simulation 🕹️")
    st.markdown("通过调整核心平台的参数，观察其对市场的动态影响。 / Adjust platform parameters to observe dynamic market impacts.")
    
    col1, col2 = st.columns([1, 2.5])
    
    with col1:
        st.info("💡 **变量调节 / Parameters**")
        aldi_sku = st.slider("奥乐齐 (Aldi) SKU 规模 / SKU Scale", 1500, 6000, 1500, 500)
        dingdong_price = st.slider("叮咚买菜 价格吸引力 / Dingdong Price Index (Lower is cheaper)", 80, 120, 105, 5)
        freshippo_time = st.slider("盒马 配送时效 / Freshippo Time (mins)", 15, 45, 30, 5)
        
    with col2:
        sim_df = df.copy()
        sim_df[['SKU_Count', 'Price_Index', 'Delivery_Time_mins']] = sim_df[['SKU_Count', 'Price_Index', 'Delivery_Time_mins']].astype(float)
        
        sim_df.loc[sim_df['Platform'] == 'Aldi', 'SKU_Count'] = aldi_sku
        sim_df.loc[sim_df['Platform'] == 'Dingdong', 'Price_Index'] = dingdong_price
        sim_df.loc[sim_df['Platform'] == 'Freshippo', 'Delivery_Time_mins'] = freshippo_time
        
        sim_df['Utility'] = (sim_df['SKU_Count']/1000)*10 + (100/sim_df['Price_Index'])*60 + (100/sim_df['Delivery_Time_mins'])*30
        sim_df['Simulated_Share'] = (sim_df['Utility'] / sim_df['Utility'].sum()) * 100
        
        fig_pie = px.pie(
            sim_df, 
            values='Simulated_Share', 
            names='Platform',
            hole=0.45,
            color='Platform',
            color_discrete_sequence=brand_colors,
            title="实时预测：全市场占有率分布 / Real-time Forecast: Market Share (%)"
        )
        
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        
        main_players = sim_df[sim_df['Platform'] != 'Others']
        if not main_players.empty:
            top_platform = main_players.loc[main_players['Simulated_Share'].idxmax(), 'Platform']
            top_share = main_players['Simulated_Share'].max()
            
            st.success(f"🏆 **结论 / Conclusion:** \n\n当前参数配置下，**{top_platform}** 将以 **{top_share:.1f}%** 的预期份额，在核心竞争平台中占据绝对优势地位。 \n\nUnder the current parameter configuration, **{top_platform}** will occupy a dominant position among the core competitors with an expected market share of **{top_share:.1f}%**.")