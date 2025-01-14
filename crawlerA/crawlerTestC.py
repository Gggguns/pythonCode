#测试 plot_yearly_movie_count 函数
import unittest
import pandas as pd
import matplotlib.pyplot as plt
from crawlerA import plot_yearly_movie_count


class TestPlotYearlyMovieCount(unittest.TestCase):
    def test_plot_yearly_movie_count(self):
        df = pd.DataFrame({
            "年份": ["2020", "2020", "2021"]
        })
        try:
            plot_yearly_movie_count(df)
        except Exception as e:
            self.fail(f"plot_yearly_movie_count raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()