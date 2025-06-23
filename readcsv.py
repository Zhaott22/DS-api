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

# 检查列名是否存在（假设第三列名为「总计（W）」）
if len(df.columns) >= 4:
    target_column = df.columns[3]  # 获取第三列列名
    st.write(f"当前按第三列 **{target_column}** 排序")

    # 按第三列降序排序并取前15行
    sorted_df = df.sort_values(by=target_column, ascending=False).head(15)
    
    # 高亮最大值并显示结果
    st.dataframe(
        sorted_df.style.highlight_max(axis=0, subset=[target_column], color='lightgreen'),
        use_container_width=True
    )
else:
    st.error("数据列数不足3列，无法排序。现有列名为：")
    st.write(df.columns.tolist())
