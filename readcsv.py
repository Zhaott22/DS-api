import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 设置页面
st.set_page_config(layout="wide")
st.title('GitHub CSV文件读取器')

# 原始GitHub URL
github_url = "https://github.com/gitneoni/st001/blob/main/for%20Tiffany-st.csv"

# 转换为raw.githubusercontent.com格式
raw_url = github_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

try:
    # 方法1：直接使用pandas读取
    df = pd.read_csv(raw_url)
    
    # 显示成功信息和数据
    st.success("文件加载成功！")
    st.write(f"文件URL: {raw_url}")
    
    # 显示数据预览
    st.subheader("数据预览")
    st.dataframe(df)
    
    # 检查是否存在"总计(W)"列
    if '总计' in df.columns:
        # 显示总计数量最多的15个公司
        st.subheader("总计TOP15公司")
        top15 = df.nlargest(15, '总计(W)')
        
        # 创建两列布局
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # 显示表格数据
            st.dataframe(top15, height=600)
        
        with col2:
            # 添加下载按钮
            csv = top15.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="下载TOP15数据",
                data=csv,
                file_name='top15_companies.csv',
                mime='text/csv'
            )
    else:
        st.warning("数据中未找到'总计(W)'列，无法进行TOP15分析")
        st.subheader("基本统计")
        st.write(df.describe())
    
    
    # 添加下载按钮
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="下载CSV文件",
        data=csv,
        file_name='github_data.csv',
        mime='text/csv'
    )

except Exception as e:
    st.error(f"加载文件失败: {str(e)}")
    st.info("""
        可能原因：
        1. 文件不存在或不是公开可访问
        2. 网络连接问题
        3. 文件不是标准CSV格式
    """)
