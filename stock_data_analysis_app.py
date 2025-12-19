import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置页面配置
st.set_page_config(
    page_title="股票数据分析平台",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 高级自定义CSS样式
st.markdown("""
<style>
    /* 全局样式 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* 标题样式 */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 3rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FFEAA7);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 4s ease infinite;
        text-shadow: 0 0 30px rgba(255,255,255,0.3);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* 指标卡片样式 */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.45);
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .sidebar-section {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: all 0.3s ease;
    }
    
    .sidebar-section:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.3);
    }
    
    /* 分隔线样式 */
    .section-divider {
        margin: 3rem 0;
        position: relative;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.8), transparent);
    }
    
    .section-divider::before {
        content: '✨';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 1.2rem;
    }
    
    /* 图表容器样式 */
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.3);
    }
    
    /* 数据表格样式 */
    .data-table {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.18);
        overflow: hidden;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stMultiselect > div > div > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stMultiselect > div > div > div:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* 复选框样式 */
    .stCheckbox > label {
        background: rgba(255, 255, 255, 0.9);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .stCheckbox > label:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: #667eea;
    }
    
    /* 标题样式 */
    h1, h2, h3 {
        color: #2d3748;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* 页脚样式 */
    .footer {
        text-align: center;
        color: white;
        padding: 2rem;
        margin-top: 3rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* 成功/警告/错误消息样式 */
    .stSuccess, .stWarning, .stError, .stInfo {
        border-radius: 15px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* 指标数值样式 */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #718096;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* 动画效果 */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# 数据加载函数
@st.cache_data
def load_data():
    """加载合并后的股票数据"""
    try:
        # 尝试读取Excel文件
        df = pd.read_excel('合并后的文件.xlsx')
    except:
        try:
            # 如果Excel不存在，尝试读取CSV
            df = pd.read_csv('股票数据合并结果.csv', encoding='utf-8-sig')
        except:
            st.error("❌ 无法找到数据文件，请确保 '合并后的文件.xlsx' 或 '股票数据合并结果.csv' 存在于当前目录")
            return None
    
    # 数据清洗
    if df is not None:
        # 处理年份列
        if '年份' in df.columns:
            df['年份'] = pd.to_numeric(df['年份'], errors='coerce')
        
        # 处理数值列
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

# 数据过滤函数
def filter_data(df, selected_stocks, selected_years, selected_industries):
    """根据用户选择过滤数据"""
    filtered_df = df.copy()
    
    if selected_stocks:
        filtered_df = filtered_df[filtered_df['股票代码简称'].isin(selected_stocks)]
    
    if selected_years:
        filtered_df = filtered_df[filtered_df['年份'].isin(selected_years)]
    
    if selected_industries:
        if '行业名称_文件1' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['行业名称_文件1'].isin(selected_industries)]
    
    return filtered_df

# 创建高级图表函数
def create_advanced_trend_chart(df, title, x_col, y_col, color_col=None):
    """创建高级趋势图表"""
    # 创建渐变色
    colors = px.colors.qualitative.Set3
    
    if color_col and color_col in df.columns:
        fig = px.line(df, x=x_col, y=y_col, color=color_col, 
                     title=f'📊 {title}', markers=True, line_shape='spline',
                     color_discrete_sequence=colors)
    else:
        fig = px.line(df, x=x_col, y=y_col, title=f'📊 {title}', 
                     markers=True, line_shape='spline',
                     line=dict(color='#667eea', width=4))
    
    # 高级样式设置
    fig.update_layout(
        height=450,
        showlegend=True,
        font=dict(size=14, family="Arial, sans-serif"),
        title_font=dict(size=20, color='#2d3748', family="Arial, sans-serif"),
        plot_bgcolor='rgba(255, 255, 255, 0.95)',
        paper_bgcolor='rgba(255, 255, 255, 0.95)',
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.95)", 
                       font_size=12, font_family="Arial"),
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0.95)",
            bordercolor="rgba(102, 126, 234, 0.3)",
            borderwidth=2,
            borderradius=10
        ),
        xaxis=dict(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='rgba(102, 126, 234, 0.1)',
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='rgba(102, 126, 234, 0.1)',
            title_font=dict(size=14),
            tickfont=dict(size=12)
        )
    )
    
    # 添加悬停效果
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>" +
                      "X: %{x}<br>" +
                      "Y: %{y:.2f}<br>" +
                      "<extra></extra>",
        marker=dict(size=8, line=dict(width=2, color='white'))
    )
    
    return fig

def create_advanced_bar_chart(df, title, x_col, y_col, color_col=None, top_n=10):
    """创建高级柱状图"""
    if top_n and len(df) > top_n:
        df = df.head(top_n)
    
    # 使用渐变色
    color_scale = [
        [0, '#667eea'],
        [0.5, '#764ba2'],
        [1, '#f093fb']
    ]
    
    fig = px.bar(df, x=x_col, y=y_col, title=f'📊 {title}',
                 color=color_col if color_col else y_col,
                 color_continuous_scale=color_scale,
                 orientation='h' if y_col in ['股票代码简称', '行业名称_文件1'] else 'v')
    
    # 高级样式设置
    fig.update_layout(
        height=450,
        showlegend=False,
        font=dict(size=14, family="Arial, sans-serif"),
        title_font=dict(size=20, color='#2d3748', family="Arial, sans-serif"),
        plot_bgcolor='rgba(255, 255, 255, 0.95)',
        paper_bgcolor='rgba(255, 255, 255, 0.95)',
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.95)", 
                       font_size=12, font_family="Arial"),
        xaxis=dict(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='rgba(102, 126, 234, 0.1)',
            title_font=dict(size=14),
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='rgba(102, 126, 234, 0.1)',
            title_font=dict(size=14),
            tickfont=dict(size=12)
        )
    )
    
    # 添加悬停效果
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>" +
                      "X: %{x}<br>" +
                      "Y: %{y:.2f}<br>" +
                      "<extra></extra>",
        marker=dict(
            line=dict(width=2, color='white'),
            cornerradius=5
        )
    )
    
    return fig

# 主应用
def main():
    # 页面标题
    st.markdown('<h1 class="main-header fade-in-up">📈 股票数据分析平台</h1>', unsafe_allow_html=True)
    
    # 加载数据
    df = load_data()
    
    if df is None:
        st.stop()
    
    # 侧边栏
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown('<h2 style="color: #2d3748; margin-bottom: 1.5rem;">🎛️ 数据筛选</h2>', unsafe_allow_html=True)
    
    # 股票代码筛选
    st.sidebar.markdown('<h3 style="color: #4a5568; margin-bottom: 1rem;">📊 股票选择</h3>', unsafe_allow_html=True)
    
    # 获取股票列表
    if '股票代码简称' in df.columns:
        stock_codes = sorted(df['股票代码简称'].dropna().unique())
        
        # 搜索功能
        search_stock = st.sidebar.text_input("🔍 搜索股票代码", 
                                           placeholder="输入股票代码或名称...",
                                           help="支持模糊搜索")
        
        if search_stock:
            filtered_stocks = [code for code in stock_codes 
                             if search_stock.lower() in str(code).lower()]
            if not filtered_stocks:
                st.sidebar.warning("🔍 未找到匹配的股票")
                filtered_stocks = stock_codes[:20]
        else:
            filtered_stocks = stock_codes
        
        selected_stocks = st.sidebar.multiselect(
            "选择股票代码（最多10只）",
            filtered_stocks,
            default=[],
            max_selections=10,
            help="最多可以选择10只股票进行对比分析"
        )
        
        st.sidebar.info(f"📋 可选股票: {len(filtered_stocks)} 只")
    else:
        selected_stocks = []
        st.sidebar.warning("⚠️ 数据中未找到股票代码列")
    
    # 年份筛选
    st.sidebar.markdown('<h3 style="color: #4a5568; margin: 1.5rem 0 1rem 0;">📅 年份选择</h3>', unsafe_allow_html=True)
    if '年份' in df.columns:
        years = sorted(df['年份'].dropna().unique())
        selected_years = st.sidebar.multiselect(
            "选择年份",
            years,
            default=years[-5:] if len(years) > 5 else years,
            help="选择要分析的年份范围"
        )
    else:
        selected_years = []
        st.sidebar.warning("⚠️ 数据中未找到年份列")
    
    # 行业筛选
    st.sidebar.markdown('<h3 style="color: #4a5568; margin: 1.5rem 0 1rem 0;">🏭 行业选择</h3>', unsafe_allow_html=True)
    if '行业名称_文件1' in df.columns:
        industries = sorted(df['行业名称_文件1'].dropna().unique())
        selected_industries = st.sidebar.multiselect(
            "选择行业",
            industries,
            default=[],
            help="按行业分类筛选数据"
        )
    else:
        selected_industries = []
        st.sidebar.warning("⚠️ 数据中未找到行业列")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # 数据过滤
    filtered_df = filter_data(df, selected_stocks, selected_years, selected_industries)
    
    # 主要内容区域
    if filtered_df.empty:
        st.warning("🔍 没有符合筛选条件的数据，请调整筛选条件")
        return
    
    # 数据概览
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    st.markdown('## 📊 数据概览')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{len(filtered_df):,}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">📝 总记录数</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        unique_stocks = filtered_df['股票代码简称'].nunique() if '股票代码简称' in filtered_df.columns else 0
        st.markdown(f'<div class="metric-value">{unique_stocks:,}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">🏢 股票数量</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        unique_years = filtered_df['年份'].nunique() if '年份' in filtered_df.columns else 0
        st.markdown(f'<div class="metric-value">{unique_years}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">📅 年份跨度</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if '数字化转型指数' in filtered_df.columns:
            avg_transform = filtered_df['数字化转型指数'].mean()
            st.markdown(f'<div class="metric-value">{avg_transform:.2f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">📈 平均转型指数</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="metric-value">{len(filtered_df.columns)}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">📊 数据列数</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # 数据表格
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    st.markdown('## 📋 数据详情')
    
    # 表格控制选项
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        show_table = st.checkbox("📊 显示数据表格", value=True, help="是否显示详细数据表格")
    
    with col2:
        if show_table:
            page_size = st.selectbox("📄 每页行数", [10, 20, 50, 100], index=1, help="每页显示的数据行数")
    
    with col3:
        if show_table:
            show_all_cols = st.checkbox("🔧 显示所有列", value=False, help="是否显示所有数据列")
    
    if show_table:
        if show_all_cols:
            display_df = filtered_df.copy()
        else:
            # 只显示关键列
            key_columns = ['股票代码简称', '企业名称', '年份', '行业名称_文件1']
            if '数字化转型指数' in filtered_df.columns:
                key_columns.append('数字化转型指数')
            
            # 添加一些数值列
            numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if col not in key_columns and '词频' in col:
                    key_columns.append(col)
                    if len(key_columns) >= 10:
                        break
            
            available_columns = [col for col in key_columns if col in filtered_df.columns]
            display_df = filtered_df[available_columns]
        
        # 分页显示
        if len(display_df) > page_size:
            total_pages = (len(display_df) - 1) // page_size + 1
            page = st.number_input("📖 页码", min_value=1, max_value=total_pages, value=1, help="选择要查看的页码")
            
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            page_df = display_df.iloc[start_idx:end_idx]
            
            st.dataframe(page_df, use_container_width=True, hide_index=True)
            st.caption(f"📄 第 {page}/{total_pages} 页 | 显示 {start_idx + 1}-{min(end_idx, len(display_df))} 条，共 {len(display_df)} 条")
        else:
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # 下载按钮
        csv_data = display_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 下载当前数据",
            data=csv_data,
            file_name=f"股票数据_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="下载当前显示的数据为CSV文件"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # 图表分析
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    st.markdown('## 📈 数据分析')
    
    if '数字化转型指数' in filtered_df.columns:
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # 年度趋势图
            yearly_data = filtered_df.groupby('年份')['数字化转型指数'].agg(['mean', 'count']).reset_index()
            fig1 = create_advanced_trend_chart(yearly_data, '年度数字化转型指数趋势', '年份', 'mean')
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with chart_col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # 行业分布图
            if selected_industries and len(selected_industries) > 1:
                industry_data = filtered_df.groupby('行业名称_文件1')['数字化转型指数'].mean().sort_values(ascending=False).head(10)
                industry_df = pd.DataFrame({
                    '行业名称_文件1': industry_data.index,
                    '数字化转型指数': industry_data.values
                })
                fig2 = create_advanced_bar_chart(industry_df, '行业转型指数排名', '数字化转型指数', '行业名称_文件1')
                fig2.update_xaxes(title_text="数字化转型指数")
                fig2.update_yaxes(title_text="行业")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                # 股票排名图
                if selected_stocks and len(selected_stocks) > 1:
                    stock_data = filtered_df.groupby('股票代码简称')['数字化转型指数'].mean().sort_values(ascending=False).head(10)
                    stock_df = pd.DataFrame({
                        '股票代码简称': stock_data.index,
                        '数字化转型指数': stock_data.values
                    })
                    fig2 = create_advanced_bar_chart(stock_df, '股票转型指数排名', '数字化转型指数', '股票代码简称')
                    fig2.update_xaxes(title_text="数字化转型指数")
                    fig2.update_yaxes(title_text="股票代码")
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("📊 请选择多个股票或行业查看详细排名")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 多股票对比图
        if len(selected_stocks) > 1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('### 📊 股票对比分析')
            
            comparison_data = filtered_df.groupby(['股票代码简称', '年份'])['数字化转型指数'].mean().reset_index()
            fig3 = create_advanced_trend_chart(comparison_data, '选中股票转型指数对比', '年份', '数字化转型指数', '股票代码简称')
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 其他数值列的分析
    numeric_columns = filtered_df.select_dtypes(include=[np.number]).columns
    other_numeric_cols = [col for col in numeric_columns if col != '数字化转型指数' and col != '年份']
    
    if other_numeric_cols:
        st.markdown('### 📊 其他指标分析')
        
        selected_metric = st.selectbox("📈 选择分析指标", other_numeric_cols, help="选择要分析的其他数值指标")
        
        if selected_metric:
            metric_col1, metric_col2 = st.columns(2)
            
            with metric_col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                # 指标年度趋势
                metric_yearly = filtered_df.groupby('年份')[selected_metric].mean().reset_index()
                fig4 = create_advanced_trend_chart(metric_yearly, f'{selected_metric}年度趋势', '年份', selected_metric)
                st.plotly_chart(fig4, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with metric_col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                # 指标排名
                if selected_stocks:
                    metric_stock = filtered_df.groupby('股票代码简称')[selected_metric].mean().sort_values(ascending=False).head(10)
                    metric_df = pd.DataFrame({
                        '股票代码简称': metric_stock.index,
                        selected_metric: metric_stock.values
                    })
                    fig5 = create_advanced_bar_chart(metric_df, f'{selected_metric}股票排名', selected_metric, '股票代码简称')
                    fig5.update_xaxes(title_text=selected_metric)
                    fig5.update_yaxes(title_text="股票代码")
                    st.plotly_chart(fig5, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 数据统计信息
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    st.markdown('## 📊 数据统计')
    
    if st.checkbox("📊 显示详细统计信息", help="显示数据的详细统计信息"):
        # 选择要统计的列
        stat_columns = st.multiselect("📋 选择要统计的列", filtered_df.columns.tolist(), 
                                    default=['数字化转型指数'] if '数字化转型指数' in filtered_df.columns else [],
                                    help="选择要显示统计信息的列")
        
        if stat_columns:
            stats_df = filtered_df[stat_columns].describe()
            st.markdown('<div class="data-table">', unsafe_allow_html=True)
            st.dataframe(stats_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 相关性分析
            if len(stat_columns) > 1:
                st.markdown('### 🔗 相关性分析')
                correlation_matrix = filtered_df[stat_columns].corr()
                
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                fig = px.imshow(correlation_matrix, 
                              text_auto=True, 
                              aspect="auto",
                              title="指标相关性热力图",
                              color_continuous_scale='RdBu_r',
                              color_continuous_midpoint=0)
                fig.update_layout(
                    height=500,
                    title_font=dict(size=18, color='#2d3748'),
                    font=dict(size=12)
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 页脚
    st.markdown('<div class="footer">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align: center; color: white; padding: 1rem;'>
        <h3 style='margin-bottom: 1rem;'>📈 股票数据分析平台</h3>
        <p style='margin: 0.5rem 0;'>基于Streamlit构建 | 现代化UI设计</p>
        <p style='margin: 0.5rem 0;'>数据更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p style='margin-top: 1rem;'>✨ 专业的股票数据分析工具</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 运行主应用
if __name__ == "__main__":
    main()