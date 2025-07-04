import streamlit as st
import pandas as pd
import plotly.express as px

# 设置页面
st.title('部门数据分析')
st.write('总表')

# GitHub文件URL处理
github_url = "https://github.com/gitneoni/st001/blob/main/for%20Tiffany-st.csv"
raw_url = github_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

# 读取数据
df = pd.read_csv(raw_url)
st.dataframe(df)

# 检查列名是否存在
if len(df.columns) >= 4:
    target_column = df.columns[3]  # 获取第四列列名
    st.write(f"当前按第四列 **{target_column}** 排序")

    # 按第四列降序排序并取前15行
    sorted_df = df.sort_values(by=target_column, ascending=False).head(15)
    
    # 高亮最大值并显示结果
    st.dataframe(
        sorted_df.style.highlight_max(axis=0, subset=[target_column], color='lightgreen'),
        use_container_width=True
    )

    # 检查后五列是否存在
    if len(sorted_df.columns) >= 5:
        last_five_columns = sorted_df.columns[-5:]  # 获取后五列列名
        
        # 创建15张折线图（每行对应一张图）
        st.subheader("前15名的五周趋势分析")
        
        for idx, row in sorted_df.iterrows():
            with st.expander(f"客户0{row.iloc[0]} 的五周指标趋势 ", expanded=False):
                # 提取当前行的后五列数据
                row_data = row[last_five_columns].reset_index()
                row_data.columns = ['时间（周）', '数值']
                
                # 使用Plotly绘制折线图
                fig = px.line(
                    row_data,
                    x='时间（周）',
                    y='数值',
                    title=f"客户0{row.iloc[0]} 的五周指标趋势",
                    markers=True,
                    height=300
                )
                fig.update_traces(line=dict(width=3))
                fig.update_layout(
                    xaxis_title='时间（周）',
                    yaxis_title='数值',
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("数据列数不足，无法绘制后五列趋势图。现有列名为：")
        st.write(sorted_df.columns.tolist())
else:
    st.error("数据列数不足4列，无法排序。现有列名为：")
    st.write(df.columns.tolist())
