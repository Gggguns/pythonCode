# 测试crawl_douban_top250函数
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
import webbrowser


# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def crawl_douban_top250():
    # 设置请求头，模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }
    # 基础 URL
    base_url = "https://movie.douban.com/top250?start={}&filter="
    # 用于存储电影名、评分、年份的列表
    movie_names = []
    ratings = []
    years = []
    # 循环爬取多页数据
    for page in range(0, 250, 25):
        response = requests.get(base_url.format(page), headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_items = soup.find_all('div', class_='item')
        for movie_item in movie_items:
            # 提取电影名
            name = movie_item.find('div', class_='hd').find('a').find('span', class_='title').text
            movie_names.append(name)
            # 提取评分
            rating = movie_item.find('div', class_='bd').find('div', class_='star').find('span', class_='rating_num').text
            ratings.append(float(rating))
            # 提取年份
            info_text = movie_item.find('div', class_='bd').find('p', class_='').text.strip().split('\n')
            if len(info_text) >= 2:  # 增加长度检查
                year = info_text[1].split('/')[0].strip()
            else:
                year = None  # 当信息不完整时使用 None 作为占位符
            years.append(year)
    df = pd.DataFrame({
        "电影名称": movie_names,
        "年份": years,
        "评分": ratings,
    })
    return df


def save_to_csv(df, filename):
    df.to_csv(filename, index=False, encoding='utf-8-sig')


def load_from_csv(filename):
    return pd.read_csv(filename)


def plot_rating_distribution(df):
    plt.figure(figsize=(10, 6))
    df['评分'].hist(bins=10, edgecolor='black')
    plt.xlabel('评分')
    plt.ylabel('电影数量')
    plt.title('电影评分分布直方图')
    plt.show()


def plot_yearly_movie_count(df):
    # 使用正则表达式提取年份中的数字
    df['年份'] = df['年份'].astype(str).apply(lambda x: int(re.search(r'\d+', x).group()))
    yearly_counts = df['年份'].value_counts().sort_index()
    plt.figure(figsize=(15, 6))
    yearly_counts.plot(kind='bar', color='skyblue')
    plt.xlabel('年份')
    plt.ylabel('电影数量')
    plt.title('不同年份上映电影的数量')
    plt.show()


def plot_rating_vs_comments(df):
    plt.figure(figsize=(10, 6))
    plt.scatter(df['评分'], df.index, alpha=0.5)
    plt.xlabel('评分')
    plt.ylabel('电影索引')
    plt.title('评分与电影索引的关系')
    plt.show()


def plot_top_movies(df, top_n=10):
    top_movies = df.nlargest(top_n, '评分')
    bar = (
        Bar()
    .add_xaxis(top_movies['电影名称'].tolist())
    .add_yaxis("评分", top_movies['评分'].tolist())
    .set_global_opts(
            title_opts=opts.TitleOpts(title=f"评分最高的{top_n}部电影"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            yaxis_opts=opts.AxisOpts(name="评分")
        )
    )
    bar.render('top_movies.html')
    return bar


def plot_comments_vs_year_bokeh(df):
    # 检查数据是否包含必要的列
    if '年份' not in df.columns or '评分' not in df.columns:
        raise ValueError("DataFrame must contain '年份' and '评分' columns.")
    # 数据预处理：处理缺失值和异常值
    df.dropna(subset=['年份', '评分'], inplace=True)
    df = df[df['评分'] >= 0]  # 假设评分不能为负数
    df.sort_values(by='年份', inplace=True)
    # 创建 Bokeh 图形
    output_file("comments_vs_year_bokeh.html")
    source = ColumnDataSource(df)
    # 使用 width 属性调整图形的宽度
    p = figure(title="不同年份电影评分总和的变化趋势", x_axis_label='年份', y_axis_label='评分总和',
              width=1000, height=500,
              tools="pan,wheel_zoom,box_zoom,reset")  # 添加缩放和平移工具
    p.line(x='年份', y='评分', source=source, line_width=2)
    show(p)


if __name__ == "__main__":
    # 爬取数据
    #df = crawl_douban_top250()
    #save_to_csv(df, 'douban_top250.csv')
    # 加载数据
    df = load_from_csv('douban_top250.csv')
    # 可视化
    plot_rating_distribution(df)
    plot_yearly_movie_count(df)
    plot_rating_vs_comments(df)
    top_movies_chart = plot_top_movies(df, top_n=10)
    # 调用 plot_comments_vs_year_bokeh 函数
    plot_comments_vs_year_bokeh(df)
    # 自动打开生成的网页
    webbrowser.open('top_movies.html')