### 工具类
class JsonUtil:
    # 去除标签<>
    @staticmethod
    def removeLabel(str_data):
        result = ""
        start = 0
        end = str_data.find('<')
        if end!= -1:
            result = str_data[:end]
        while end!= -1:
            start = str_data.find('>', end) + 1
            end = str_data.find('<', end + 1)
            if end == -1:
                break
            result += str_data[start:end]
        result += str_data[start:]
        return result
    #浮点数转字符串
    def float_to_string(latitude, longitude):
        result = "{},{}".format(latitude, longitude)
        return result
    


