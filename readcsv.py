import streamlit as st
import pandas as pd

# 设置页面
#st.set_page_config(layout="wide")
st.title('部门数据分析')

# GitHub文件URL处理
github_url = "https://github.com/gitneoni/st001/blob/main/for%20Tiffany-st.csv"
raw_url = github_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

#读取数据
df = pd.read_csv(raw_url)

#输出数据
st.dataframe(df)

# 检查列名是否存在（避免大小写或空格问题）
if '总计（W）' in df.columns:
    # 按「总计（W）」降序排序并取前15行
    top_15 = df.sort_values(by='总计（W）', ascending=False).head(15)
    
    # 显示结果（带高亮最大值）
    st.subheader("总计（W）最大的前15行数据")
    st.dataframe(
        top_15.style.highlight_max(axis=0, subset=['总计（W）'], color='lightgreen'),
        use_container_width=True
    )
else:
    st.error("未找到列名「总计（W）」，请检查数据列名是否为以下之一：")
    st.write(df.columns.tolist())
