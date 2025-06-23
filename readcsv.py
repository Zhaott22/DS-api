mport streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns

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