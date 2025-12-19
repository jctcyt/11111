import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# 设置页面配置
st.set_page_config(
    page_title="企业数字化转型指数查询系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用标题
st.title("📊 企业数字化转型指数查询系统")
st.markdown("---")

# 侧边栏
st.sidebar.header("查询设置")

# 数据加载函数
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('合并后的文件.xlsx')
        return df
    except Exception as e:
        st.error(f"数据加载失败: {e}")
        return None

# 主程序
def main():
    # 加载数据
    df = load_data()
    
    if df is None:
        st.error("无法加载数据文件，请确保 '合并后的文件.xlsx' 文件存在于当前目录")
        return
    
    # 显示数据基本信息
    st.subheader("📋 数据概览")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("数据行数", df.shape[0])
    with col2:
        st.metric("数据列数", df.shape[1])
    with col3:
        st.metric("文件大小", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    
    # 显示列名
    with st.expander("查看数据列名"):
        st.write("数据列名列表:")
        for i, col in enumerate(df.columns):
            st.write(f"{i+1}. {col}")
    
    # 智能识别列
    def identify_columns(df):
        stock_cols = []
        year_cols = []
        index_cols = []
        
        for col in df.columns:
            col_lower = str(col).lower()
            # 识别股票代码列
            if any(keyword in col_lower for keyword in ['股票', '代码', 'code', 'stock', 'symbol']):
                stock_cols.append(col)
            # 识别年份列
            elif any(keyword in col_lower for keyword in ['年', 'year', '时间', 'time', '日期', 'date']):
                year_cols.append(col)
            # 识别数字化转型指数列
            elif any(keyword in col_lower for keyword in ['转型', '数字化', '指数', 'index', 'digital', 'transform']):
                index_cols.append(col)
        
        return stock_cols, year_cols, index_cols
    
    stock_cols, year_cols, index_cols = identify_columns(df)
    
    # 自动选择列（优先使用识别到的列，否则使用前几列）
    all_cols = df.columns.tolist()
    
    # 自动选择股票代码列
    if stock_cols:
        selected_stock_col = stock_cols[0]
    else:
        selected_stock_col = all_cols[0]
        st.warning(f"⚠️ 未自动识别到股票代码列，使用第一列: {selected_stock_col}")
    
    # 自动选择年份列
    if year_cols:
        selected_year_col = year_cols[0]
    else:
        selected_year_col = all_cols[1] if len(all_cols) > 1 else all_cols[0]
        st.warning(f"⚠️ 未自动识别到年份列，使用第二列: {selected_year_col}")
    
    # 自动选择数字化转型指数列
    if index_cols:
        selected_index_col = index_cols[0]
    else:
        selected_index_col = all_cols[2] if len(all_cols) > 2 else all_cols[0]
        st.warning(f"⚠️ 未自动识别到数字化转型指数列，使用第三列: {selected_index_col}")
    
    # 显示自动选择的列信息
    st.info(f"📌 已自动选择列 - 股票代码: **{selected_stock_col}** | 年份: **{selected_year_col}** | 指数: **{selected_index_col}**")
    
    # 数据预处理
    try:
        # 清理数据
        df_clean = df.copy()
        df_clean = df_clean.dropna(subset=[selected_stock_col, selected_year_col, selected_index_col])
        
        # 转换数据类型
        df_clean[selected_year_col] = pd.to_numeric(df_clean[selected_year_col], errors='coerce')
        df_clean[selected_index_col] = pd.to_numeric(df_clean[selected_index_col], errors='coerce')
        # 格式化股票代码为6位
        df_clean[selected_stock_col] = df_clean[selected_stock_col].astype(str).apply(lambda x: x.zfill(6) if x.isdigit() else str(x))
        
        # 去除无效数据
        df_clean = df_clean.dropna()
        
        # 获取唯一的股票代码和年份
        unique_stocks = sorted(df_clean[selected_stock_col].unique())
        unique_years = sorted(df_clean[selected_year_col].unique())
        
        # 侧边栏查询控件
        st.sidebar.subheader("🔍 查询条件")
        
        # 股票代码选择
        selected_stock = st.sidebar.selectbox(
            "选择股票代码:",
            options=unique_stocks,
            help="选择要查询的企业股票代码"
        )
        
        # 年份输入选择 - 限制在2019-2020年
        selected_year = st.sidebar.number_input(
            "选择年份:",
            min_value=2019,
            max_value=2020,
            value=2020,
            step=1,
            help="选择2019或2020年进行查询"
        )
        
        # 查询按钮
        if st.sidebar.button("🚀 开始查询", type="primary"):
            # 筛选该股票的所有年份数据
            stock_data = df_clean[
                (df_clean[selected_stock_col] == selected_stock)
            ].sort_values(selected_year_col)
            
            # 筛选特定年份的数据用于高亮显示
            year_data = df_clean[
                (df_clean[selected_stock_col] == selected_stock) &
                (df_clean[selected_year_col] == selected_year)
            ]
            
            if stock_data.empty:
                st.warning("没有找到该股票的数据，请检查股票代码")
            else:
                # 显示查询结果
                st.subheader(f"📈 {selected_stock} 数字化转型指数趋势分析")
                
                # 显示查询年份信息
                if not year_data.empty:
                    st.info(f"🎯 查询年份 {selected_year} 的指数值: {year_data[selected_index_col].iloc[0]:.2f}")
                else:
                    st.warning(f"⚠️ 该股票在 {selected_year} 年没有数据")
                
                # 完整数据表格
                with st.expander("查看该股票所有年份数据"):
                    st.dataframe(stock_data, use_container_width=True)
                
                # 完整趋势折线图
                fig = go.Figure()
                
                # 添加趋势线
                fig.add_trace(go.Scatter(
                    x=stock_data[selected_year_col],
                    y=stock_data[selected_index_col],
                    mode='lines+markers',
                    name='数字化转型指数',
                    line=dict(color='#1f77b4', width=3),
                    marker=dict(size=8, color='#1f77b4')
                ))
                
                # 高亮显示查询年份的点
                if not year_data.empty:
                    fig.add_trace(go.Scatter(
                        x=[selected_year],
                        y=[year_data[selected_index_col].iloc[0]],
                        mode='markers',
                        name=f'{selected_year}年查询点',
                        marker=dict(size=15, color='#ff7f0e', symbol='diamond', line=dict(width=2, color='white'))
                    ))
                
                fig.update_layout(
                    title=f"{selected_stock} 数字化转型指数趋势图 (查询年份: {selected_year})",
                    xaxis_title="年份",
                    yaxis_title="数字化转型指数",
                    hovermode='x unified',
                    template='plotly_white',
                    height=500,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 统计分析
                st.subheader("📊 统计分析")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("最高指数", f"{stock_data[selected_index_col].max():.2f}")
                with col2:
                    st.metric("最低指数", f"{stock_data[selected_index_col].min():.2f}")
                with col3:
                    st.metric("平均指数", f"{stock_data[selected_index_col].mean():.2f}")
                with col4:
                    st.metric("数据年数", len(stock_data))
                
                # 趋势分析
                if len(stock_data) >= 2:
                    first_value = stock_data.iloc[0][selected_index_col]
                    last_value = stock_data.iloc[-1][selected_index_col]
                    change = last_value - first_value
                    change_rate = (change / first_value) * 100 if first_value != 0 else 0
                    
                    st.subheader("📈 整体趋势分析")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if change > 0:
                            st.success(f"📈 总体上升: {change:+.2f} ({change_rate:+.1f}%)")
                        elif change < 0:
                            st.error(f"📉 总体下降: {change:+.2f} ({change_rate:+.1f}%)")
                        else:
                            st.info("➡️ 指数保持不变")
                    
                    with col2:
                        first_year = stock_data.iloc[0][selected_year_col]
                        last_year = stock_data.iloc[-1][selected_year_col]
                        st.write(f"起始年份 ({first_year}): {first_value:.2f}")
                        st.write(f"结束年份 ({last_year}): {last_value:.2f}")
                
                # 查询年份详情
                if not year_data.empty:
                    st.subheader("🎯 查询年份详情")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        year_value = year_data[selected_index_col].iloc[0]
                        st.metric(f"{selected_year}年指数", f"{year_value:.2f}")
                    
                    with col2:
                        # 计算该年份在历史中的位置
                        rank = stock_data[stock_data[selected_index_col] <= year_value].shape[0]
                        total = len(stock_data)
                        percentile = (rank / total) * 100
                        st.metric("历史排名", f"第{rank}名 ({percentile:.1f}%)")
                    
                    with col3:
                        # 与平均值的比较
                        avg_value = stock_data[selected_index_col].mean()
                        diff = year_value - avg_value
                        diff_pct = (diff / avg_value) * 100 if avg_value != 0 else 0
                        if diff > 0:
                            st.success(f"高于平均: {diff:+.2f} ({diff_pct:+.1f}%)")
                        elif diff < 0:
                            st.error(f"低于平均: {diff:+.2f} ({diff_pct:+.1f}%)")
                        else:
                            st.info("等于平均值")
                
                # 数据表格
                st.subheader("📋 详细数据")
                st.dataframe(stock_data, use_container_width=True)
        
        # 应用说明
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📋 使用说明")
        st.sidebar.info("1. 选择股票代码\n2. 输入查询年份\n3. 查看完整趋势")
    
    except Exception as e:
        st.error(f"数据处理过程中出现错误: {e}")
        st.write("请检查数据格式是否正确，或尝试选择其他列")

if __name__ == "__main__":
    main()