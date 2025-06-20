import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置页面
st.set_page_config(layout="wide")
st.title('部门数据分析仪表板')

# GitHub文件URL处理
github_url = "https://github.com/gitneoni/st001/blob/main/for%20Tiffany-st.csv"
raw_url = github_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

try:
    # 读取数据
    df = pd.read_csv(raw_url)
    
    # 检查必要列
    required_columns = ['部门', '总计', '第一周', '第二周', '第三周', '第四周', '第五周']
    if not all(col in df.columns for col in required_columns):
        missing_cols = [col for col in required_columns if col not in df.columns]
        st.error(f"数据中缺少必要列: {', '.join(missing_cols)}")
        st.stop()
    
    # 获取总计TOP15部门
    top15_depts = df.nlargest(15, '总计')[['部门'] + required_columns[1:]]
    
    # 显示原始数据
    with st.expander("查看完整数据", expanded=False):
        st.dataframe(df)
    
    # 主界面布局
    tab1, tab2 = st.tabs(["TOP15部门总览", "五周趋势分析"])
    
    with tab1:
        # TOP15部门总表
        st.subheader("总计TOP15部门")
        st.dataframe(
            top15_depts.sort_values('总计', ascending=False),
            height=600,
            use_container_width=True
        )
        
        # 下载按钮
        csv = top15_depts.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="下载TOP15数据",
            data=csv,
            file_name='top15_departments.csv',
            mime='text/csv'
        )
    
    with tab2:
        # 趋势分析图表
        st.subheader("五周变化趋势")
        
        # 转换数据格式为长表
        trend_data = top15_depts.melt(
            id_vars=['部门'],
            value_vars=['第一周', '第二周', '第三周', '第四周', '第五周'],
            var_name='周次',
            value_name='数值'
        )
        
        # 创建折线图
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.lineplot(
            data=trend_data,
            x='周次',
            y='数值',
            hue='部门',
            marker='o',
            linewidth=2.5,
            ax=ax
        )
        
        # 图表美化
        ax.set_title("TOP15部门五周趋势对比", fontsize=16)
        ax.set_xlabel("周次", fontsize=12)
        ax.set_ylabel("数值", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        st.pyplot(fig)
        
        # 添加部门选择器
        selected_depts = st.multiselect(
            "选择要重点关注的部门",
            options=top15_depts['部门'].unique(),
            default=top15_depts['部门'].head(3).tolist()
        )
        
        if selected_depts:
            # 显示选中部门的详细数据
            st.dataframe(
                top15_depts[top15_depts['部门'].isin(selected_depts)],
                use_container_width=True
            )

except Exception as e:
    st.error(f"数据处理出错: {str(e)}")
    st.info("""
        可能原因：
        1. GitHub文件不可访问
        2. 网络连接问题
        3. 文件格式异常
    """)
