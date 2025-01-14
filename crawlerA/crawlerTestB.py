#测试 plot_rating_distribution 函数
import unittest
import pandas as pd
import matplotlib.pyplot as plt
from crawlerA import plot_rating_distribution

class TestPlotRatingDistribution(unittest.TestCase):
    def test_plot_rating_distribution(self):
        df = pd.DataFrame({
            "评分": [8.5, 7.8, 9.2]
        })
        try:
            plot_rating_distribution(df)
        except Exception as e:
            self.fail(f"plot_rating_distribution raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()