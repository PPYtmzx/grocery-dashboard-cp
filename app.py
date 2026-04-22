import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 0. 核心网页配置 / Page Configuration
# ==========================================
st.set_page_config(page_title="商业分析仪表板 / BI Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 1. 响应式深色模式 & UI 优化 / Dark-Mode & UI CSS
# ==========================================
st.markdown("""
<style>
    /* 默认浅色模式 / Light Mode */
    [data-testid="stSidebar"] { background-color: #FAFAFA; border-right: 1px solid #E5E7EB; }
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #F3F4F6;
        padding: 20px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-top: 4px solid #1E3A8A; 
        transition: all 0.3s ease;
    }

    /* 深色模式适配 / Dark Mode Adaptation */
    @media (prefers-color-scheme: dark) {
        [data-testid="stSidebar"] {
            background-color: #111827 !important;
            border-right: 1px solid #374151 !important;
        }
        div[data-testid="metric-container"] {
            background-color: #1F2937 !important;
            border: 1px solid #374151 !important;
            border-top: 4px solid #3B82F6 !important;
        }
        div[data-testid="metric-container"] label, 
        div[data-testid="metric-container"] [data-testid="stMetricValue"],
        div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
            color: #F9FAFB !important;
        }
    }

    /* 悬浮动效 / Hover Effect */
    div[data-testid="metric-container"]:hover { transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    html, body, [class*="css"] { font-family: 'Inter', -apple-system, sans-serif; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 数据读取 / Data Loading
# ==========================================
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ 未检测到数据源: data.csv")
    st.stop()

corp_colors = ['#1E3A8A', '#059669', '#D97706', '#DC2626', '#9CA3AF']

# ==========================================
# 3. 侧边栏 / Sidebar
# ==========================================
with st.sidebar:
    st.markdown("### 📊 战略分析面板 \n **Strategic Analytics**")
    st.markdown("---")
    page = st.radio("分析模块索引 / Index：",
        ["1. 宏观概览 (Executive Overview)", "2. 履约模型 (Fulfillment Model)", 
         "3. 战略定位 (Strategic Group Map)", "4. 动态推演 (Market Simulation)"])
    st.markdown("---")
    st.caption("© 2026 Competitor Intelligence Team of XJTLU")
    st.caption("数据说明：基于行业基准的模拟估算数据。 / Data Source: Simulated proxy data based on industry benchmarks.")

# ==========================================
# 模块 1：概览大屏 / Module 1: Overview
# ==========================================
if page == "1. 概览大屏 (Executive Overview)":
    st.title("宏观市场概览 / Executive Overview 🌐")
    st.markdown("四大核心生鲜电商平台的关键商业指标。 / KPI benchmarking across major platforms.")
    st.markdown("<br>", unsafe_allow_html=True)
    display_df = df[df['Platform'] != 'Others'].reset_index(drop=True)
    cols = st.columns(4)
    for i, row in display_df.iterrows():
        if i < 4: 
            with cols[i]:
                st.metric(label=f"🏢 {row['Platform']}", value=f"{row['Market_Share_Pct']}%", 
                          delta=f"NPS 评分: {row['User_Rating']}")
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📚 研究方法论与数据假设 / Methodology & Data Assumptions"):
        st.markdown("* **数据来源:** 行业替代数据 (Proxy Data)。\n* **指标定义:** `Price_Index` 代表平台溢价水平 (100 为基准)。")
    st.dataframe(df.style.highlight_max(subset=['Market_Share_Pct', 'User_Rating'], color='#D1FAE5'), use_container_width=True)

# ==========================================
# 模块 2：履约模型 / Module 2: Efficiency
# ==========================================
elif page == "2. 履约模型 (Fulfillment Model)":
    st.title("履约时效 vs. 成本结构 / Fulfillment vs. Cost 🚚")
    y_choice = st.selectbox("🎯 评估维度 / Evaluation Metric:", ["Estimated_AOV", "Free_Delivery_Threshold"])
    fig = px.scatter(df[df['Platform'] != 'Others'], x="Delivery_Time_mins", y=y_choice, size="SKU_Count", 
                     color="Platform", text="Platform", color_discrete_sequence=corp_colors[:4])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=40, b=40, l=40, r=40))
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 模块 3：战略定位 / Module 3: Positioning
# ==========================================
elif page == "3. 战略定位 (Strategic Group Map)":
    st.title("市场战略群体图 / Strategic Group Map 🎯")
    fig2 = px.scatter(df[df['Platform'] != 'Others'], x="SKU_Count", y="Price_Index", size="Market_Share_Pct", 
                      color="Platform", text="Platform", log_x=True, color_discrete_sequence=corp_colors[:4])
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# 模块 4：动态推演 / Module 4: Simulation
# ==========================================
elif page == "4. 动态推演 (Market Simulation)":
    st.title("动态市场份额模拟沙盘 / Market Simulation Engine 🕹️")
    st.markdown("滑动下方滑块，实时观察市场占有率的动态分配。 / Adjust parameters to observe real-time market share reallocation.")
    
    col1, col2 = st.columns([1.2, 2.8], gap="large")
    with col1:
        st.info("#### 🎛️ 参数控制台 / Control Panel")
        a_sku = st.slider("Aldi: SKU 规模扩张 / SKU Expansion", 1500, 6000, 1500, 500)
        d_price = st.slider("Dingdong: 价格下探指数 / Price Drop", 80, 120, 105, 5)
        f_time = st.slider("Freshippo: 配送提速 / Speed-up (min)", 15, 45, 30, 5)
        st.markdown("---")
        st.latex(r"U_i = 10\left(\frac{SKU}{1k}\right) + 60\left(\frac{100}{Price}\right) + 30\left(\frac{100}{Time}\right)")

    with col2:
        sim_df = df.copy()
        sim_df[['SKU_Count', 'Price_Index', 'Delivery_Time_mins']] = sim_df[['SKU_Count', 'Price_Index', 'Delivery_Time_mins']].astype(float)
        sim_df.loc[sim_df['Platform'] == 'Aldi', 'SKU_Count'] = a_sku
        sim_df.loc[sim_df['Platform'] == 'Dingdong', 'Price_Index'] = d_price
        sim_df.loc[sim_df['Platform'] == 'Freshippo', 'Delivery_Time_mins'] = f_time
        
        # 实时计算效用 / Real-time calculation
        sim_df['Utility'] = (sim_df['SKU_Count']/1000.0)*10.0 + (100.0/sim_df['Price_Index'])*60.0 + (100.0/sim_df['Delivery_Time_mins'])*30.0
        sim_df['Simulated_Share'] = (sim_df['Utility'] / sim_df['Utility'].sum()) * 100.0
        
        # 大尺寸实时饼图 / Large Real-time Pie Chart
        fig_pie = px.pie(sim_df, values='Simulated_Share', names='Platform', hole=0.5,
                         color='Platform', color_discrete_sequence=corp_colors)
        fig_pie.update_traces(textposition='outside', textinfo='percent+label', textfont_size=15)
        fig_pie.update_layout(height=600, margin=dict(t=60, b=40, l=80, r=80), showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # 增加物理间隔防止文本挡住 / Add spacing to avoid occlusion
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        main_p = sim_df[sim_df['Platform'] != 'Others']
        top_p = main_p.loc[main_p['Simulated_Share'].idxmax(), 'Platform']
        top_s = main_p['Simulated_Share'].max()
        oth_s = sim_df.loc[sim_df['Platform'] == 'Others', 'Simulated_Share'].values[0]
        
        st.success(f"🏆 **结论 / Conclusion:** \n\n当前推演下，**{top_p}** 占据主导地位 (份额 **{top_s:.1f}%**)。碎片化市场空间被压缩至 **{oth_s:.1f}%**。 \n\n **{top_p}** dominates with **{top_s:.1f}%** share. Others compressed to **{oth_s:.1f}%**.")
