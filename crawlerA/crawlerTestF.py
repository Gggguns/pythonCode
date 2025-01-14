#端到端测试
import unittest
import os
import pandas as pd
from crawlerA import crawl_douban_top250, save_to_csv, load_from_csv, plot_rating_distribution, plot_yearly_movie_count, plot_rating_vs_comments, plot_top_movies, plot_comments_vs_year_bokeh


class TestEndToEnd(unittest.TestCase):
    def test_end_to_end(self):
        # 爬取数据
        df = crawl_douban_top250()
        save_to_csv(df, 'test_end_to_end.csv')
        loaded_df = load_from_csv('test_end_to_end.csv')
        self.assertEqual(len(loaded_df), 250)  # 假设应该有 250 条记录
        plot_rating_distribution(loaded_df)
        plot_yearly_movie_count(loaded_df)
        plot_rating_vs_comments(loaded_df)
        plot_top_movies(loaded_df, top_n=10)
        plot_comments_vs_year_bokeh(loaded_df)
        self.assertTrue(os.path.exists('top_movies.html'))
        self.assertTrue(os.path.exists('comments_vs_year_bokeh.html'))


if __name__ == "__main__":
    unittest.main()