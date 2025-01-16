import re
import path
from voice import speechRecognize  


if __name__ == "__main__" :
    #语音识别
    text = speechRecognize()
    # 判断文本中是否包含“我要去”
    if "我要去" in text:
        # 截取“我要去”后面的文字
        result = text.split("我要去")[1].strip()
        # 使用正则表达式删除末尾的标点符号
        result = re.sub(r'[^\w\s]', '', result)
        # Debug输出
            #print(result)
        #导航提示
        path.navigationPrompt(result)
    else:
        print("文本中未包含'我要去'短语")

    
