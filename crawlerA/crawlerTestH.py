# plot_rating_vs_comments 函数
import unittest
import pandas as pd
import matplotlib.pyplot as plt
from crawlerA import plot_rating_vs_comments


class TestPlotRatingVsComments(unittest.TestCase):
    def test_plot_rating_vs_comments(self):
        # 创建一个简单的 DataFrame 用于测试
        df = pd.DataFrame({
            "评分": [8.5, 7.8, 9.2],
            "电影名称": ["Movie 1", "Movie 2", "Movie 3"]
        })
        try:
            # 调用 plot_rating_vs_comments 函数进行测试
            plot_rating_vs_comments(df)
        except Exception as e:
            self.fail(f"plot_rating_vs_comments 函数引发了异常: {e}")


if __name__ == "__main__":
    unittest.main()