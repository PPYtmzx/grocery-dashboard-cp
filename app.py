import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 0. 核心网页配置 / Page Configuration
# ==========================================
st.set_page_config(page_title="商业分析仪表板 / BI Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 1. 响应式深色模式 CSS (保留原生 UI)
# ==========================================
st.markdown("""
<style>
    /* 侧边栏样式 / Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #FAFAFA; 
        border-right: 1px solid #E5E7EB; 
    }
    
    /* 数据卡片样式 / Metric Card Styling */
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
# 2. 数据读取与配色 / Data & Palette
# ==========================================
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ 未检测到数据源 (Missing Data Source): data.csv")
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
# 3. 侧边栏导航 / Sidebar Navigation
# ==========================================
with st.sidebar:
    st.markdown("### 📊 战略分析面板 / Strategic Analytics")
    st.markdown("---")
    page = st.radio(
        "分析模块索引 / Index：",
        ["1. 宏观概览 (Executive Overview)", 
         "2. 履约模型 (Fulfillment Model)", 
         "3. 战略定位 (Strategic Group Map)", 
         "4. 动态推演 (Market Simulation)"]
    )
    st.markdown("---")
    st.caption("© 2026 Competitor Intelligence Team of XJTLU")
    st.caption("数据说明：基于行业基准的模拟估算数据。仅作演示用途。 / Data Source: Simulated proxy data based on industry benchmarks. For demonstration purposes only.")

# ==========================================
# 模块 1：宏观概览 / Module 1: Overview
# ==========================================
if page == "1. 宏观概览 (Executive Overview)":
    st.title("宏观市场概览 / Executive Overview 🌐")
    st.markdown("四大核心生鲜电商平台的关键商业指标基准测试。 / KPI benchmarking across major fresh grocery e-commerce platforms.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    display_df = df[df['Platform'] != 'Others'].reset_index(drop=True)
    
    cols = st.columns(4)
    for i, row in display_df.iterrows():
        if i < 4: 
            with cols[i]:
                st.metric(label=f"🏢 {row['Platform']}", 
                          value=f"{row['Market_Share_Pct']}%", 
                          delta=f"综合评分 / Rating: {row['User_Rating']}",
                          delta_color="normal")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("📚 研究方法论与数据假设 / Methodology & Data Assumptions", expanded=False):
        st.markdown("""
        * **数据来源 (Data Sourcing):** 本仪表板采用行业替代数据 (Proxy Data)，基于各平台公开商业模式建立基准。 / This dashboard utilizes Industry Proxy Data, establishing benchmarks based on the public business models of each platform.
        * **指标定义 (Metric Definitions):** * `Estimated_AOV`: 预估单笔订单的平均交易金额 / Estimated Average Order Value.
            * `Price_Index`: 平台商品价格相对于市场平均水平的加权指数 (基准值 = 100) / Weighted index of platform prices relative to the market average (Baseline = 100).
        """)
        
    st.subheader("底层数据明细 / Raw Dataset")
    st.dataframe(df.style.highlight_max(subset=['Market_Share_Pct', 'User_Rating'], color='#D1FAE5'), use_container_width=True)

# ==========================================
# 模块 2：履约与成本分析 / Module 2: Efficiency
# ==========================================
elif page == "2. 履约模型 (Fulfillment Model)":
    st.title("履约时效 vs. 成本结构 / Fulfillment vs. Cost 🚚")
    st.markdown("物理世界的商业权衡：分析末端配送速度对平台盈利模型的影响。 / Physical world trade-offs: Analyzing the effect of last-mile delivery speed on platform profitability models.")
    
    y_axis_choice = st.selectbox("🎯 评估维度 / Evaluation Metric:", ["Estimated_AOV", "Free_Delivery_Threshold"])
    
    plot_df = df[df['Platform'] != 'Others']
    
    fig = px.scatter(
        plot_df, x="Delivery_Time_mins", y=y_axis_choice, size="SKU_Count", color="Platform",
        hover_name="Platform", text="Platform",
        color_discrete_sequence=corp_colors[:4], 
        labels={
            "Delivery_Time_mins": "平均配送时效 / Avg. Latency (mins)", 
            "Estimated_AOV": "预估客单价 / Est. AOV (RMB)", 
            "Free_Delivery_Threshold": "免邮门槛 / Free Delivery Threshold (RMB)"
        }
    )
    fig.update_traces(textposition='top center', marker=dict(line=dict(width=1.5, color='white')))
    fig = apply_corporate_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 模块 3：战略群体定位 / Module 3: Positioning
# ==========================================
elif page == "3. 战略定位 (Strategic Group Map)":
    st.title("市场战略群体图 / Strategic Group Map 🎯")
    st.markdown("多维生态位映射：基于 SKU 覆盖广度与溢价能力的聚类分析。 / Multi-dimensional niche mapping: Clustering analysis based on SKU coverage and pricing capability.")
    
    plot_df = df[df['Platform'] != 'Others']
    
    fig2 = px.scatter(
        plot_df, x="SKU_Count", y="Price_Index", size="Market_Share_Pct", color="Platform",
        hover_name="Platform", text="Platform", log_x=True,
        color_discrete_sequence=corp_colors[:4],
        labels={
            "SKU_Count": "供给复杂度 / SKU Diversity (Log Scale)", 
            "Price_Index": "溢价指数 / Price Index"
        }
    )
    fig2.update_traces(textposition='bottom right', marker=dict(line=dict(width=1.5, color='white')))
    fig2 = apply_corporate_theme(fig2)
    st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# 模块 4：机会与矩阵模拟 / Module 4: Simulation
# ==========================================
elif page == "4. 动态推演 (Market Simulation)":
    st.title("动态市场份额模拟沙盘 / Market Simulation Engine 🕹️")
    st.markdown("基于离散效用模型的假设性情景推演。 / Hypothetical scenario deduction based on the Discrete Utility Model.")
    
    # 启用局部渲染加速
    @st.fragment
    def render_simulation_sandbox():
        col1, col2 = st.columns([1.2, 2.8], gap="large")
        
        with col1:
            st.markdown("#### 🎛️ 参数控制台 / Control Panel")
            st.caption("调整变量以重构竞争状态 / Adjust variables to reconstruct landscape")
            aldi_sku = st.slider("Aldi: SKU 规模扩张 / SKU Expansion", 1500, 6000, 1500, 10)
            dingdong_price = st.slider("Dingdong: 价格下探指数 / Price Drop Index", 80, 120, 105, 1)
            freshippo_time = st.slider("Freshippo: 配送提速(分钟) / Speed-up (mins)", 15, 45, 30, 1)
            
            st.markdown("---")
            st.markdown("#### 🧮 底层算法 / Algorithm")
            st.caption("市场份额重分配基于效用引力公式： / Market share reallocation is based on utility gravity formula:")
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
                title="沙盘预测：全市场占有率 / Simulated Market Share (%)"
            )
            
            fig_pie.update_traces(
                textposition='outside', textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Share: %{percent}<extra></extra>',
                textfont_size=14,
                sort=False  # 核心修复：关闭自动排序，死死固定扇区物理位置
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
                
                st.info(f"📌 **洞察结论 / Strategic Insight:** \n\n当前参数情境下，**{top_platform}** 获取了核心阵营中的最大引力 (预期份额 **{top_share:.1f}%**)。此外，因行业内卷加剧，传统零散市场 (Others) 的生存空间被压缩至 **{others_share:.1f}%**。 \n\n Under current parameters, **{top_platform}** captures maximum gravity (Expected Share: **{top_share:.1f}%**). Fragmentation (Others) is compressed to **{others_share:.1f}%**.")

    # 激活渲染模块
    render_simulation_sandbox()
