#测试 plot_top_movies 函数
import unittest
import pandas as pd
import os
from crawlerA import plot_top_movies


class TestPlotTopMovies(unittest.TestCase):
    def test_plot_top_movies(self):
        df = pd.DataFrame({
            "电影名称": ["Test Movie 1", "Test Movie 2"],
            "评分": [8.5, 7.8]
        })
        plot_top_movies(df, top_n=1)
        self.assertTrue(os.path.exists('top_movies.html'))


if __name__ == "__main__":
    unittest.main()