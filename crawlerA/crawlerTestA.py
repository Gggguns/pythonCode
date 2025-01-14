# 测试 save_to_csv 和 load_from_csv 函数
import unittest
import pandas as pd
from crawlerA import save_to_csv, load_from_csv


class TestSaveAndLoadCSV(unittest.TestCase):
    def test_save_and_load_csv(self):
        df = pd.DataFrame({
            "电影名称": ["Test Movie 1", "Test Movie 2"],
            "年份": ["2020", "2021"],
            "评分": [8.5, 7.8]
        })
        # 将年份列的数据类型显式转换为字符串
        df['年份'] = df['年份'].astype(str)
        save_to_csv(df, 'test.csv')
        # 加载 CSV 时，显式指定数据类型
        loaded_df = load_from_csv('test.csv')
        loaded_df['年份'] = loaded_df['年份'].astype(str)
        pd.testing.assert_frame_equal(df, loaded_df)


if __name__ == "__main__":
    unittest.main()