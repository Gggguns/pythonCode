#测试 plot_comments_vs_year_bokeh 函数
import unittest
import pandas as pd
import os
from crawlerA import plot_comments_vs_year_bokeh


class TestPlotCommentsVsYearBokeh(unittest.TestCase):
    def test_plot_comments_vs_year_bokeh(self):
        df = pd.DataFrame({
            "年份": ["2020", "2021"],
            "评分": [8.5, 7.8]
        })
        try:
            plot_comments_vs_year_bokeh(df)
        except Exception as e:
            self.fail(f"plot_comments_vs_year_bokeh raised an exception: {e}")
        self.assertTrue(os.path.exists('comments_vs_year_bokeh.html'))


if __name__ == "__main__":
    unittest.main()