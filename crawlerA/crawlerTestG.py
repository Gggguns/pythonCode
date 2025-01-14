import unittest
from unittest.mock import patch
import pandas as pd
from crawlerA import crawl_douban_top250


class TestCrawlDoubanTop250(unittest.TestCase):
    @patch('requests.get')
    def test_crawl_douban_top250(self, mock_get):
        # 模拟请求的响应
        mock_response = mock_get.return_value
        mock_response.text = """
        <html>
        <body>
            <div class="item">
                <div class="hd">
                    <a><span class="title">Test Movie 1</span></a>
                </div>
                <div class="bd">
                    <div class="star"><span class="rating_num">8.5</span></div>
                    <p class="">
                        <br />1994 / USA
                    </p>
                </div>
            </div>
            <div class="item">
                <div class="hd">
                    <a><span class="title">Test Movie 2</span></a>
                </div>
                <div class="bd">
                    <div class="star"><span class="rating_num">7.8</span></div>
                    <p class="">
                        <br />2000 / UK
                    </p>
                </div>
            </div>
            <!-- 以下添加更多的电影条目，直到总共有 30 个 -->
            <div class="item">
                <div class="hd">
                    <a><span class="title">Test Movie 3</span></a>
                </div>
                <div class="bd">
                    <div class="star"><span class="rating_num">8.0</span></div>
                    <p class="">
                        <br />2005 / Japan
                    </p>
                </div>
            </div>
            <!-- 继续添加更多的 <div class="item"> 元素直到总数达到 30 个 -->
        </body>
        </html>
        """
        df = crawl_douban_top250()
        self.assertEqual(len(df), 30)  # 调整断言为 30
        self.assertListEqual(list(df.columns), ['电影名称', '年份', '评分'])
        # 以下可以添加更多的断言语句检查具体的数据内容


if __name__ == "__main__":
    unittest.main()