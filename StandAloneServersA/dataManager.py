import networkx as nx
from math import radians, cos, sin, sqrt, atan2
import time
from rtree import index  # 引入 rtree 空间索引库


# ClientDataManager 类负责管理客户端数据并计算客户端之间的距离
class ClientDataManager:
    def __init__(self):
        # 初始化一个图来存储客户端信息
        self.graph = nx.Graph()
        # 记录每个客户端的最后心跳时间
        self.last_heartbeat_times = {}
        # 心跳超时时间，单位为秒
        self.heartbeat_timeout = 60
        # 初始化空间索引
        self.idx = index.Index()
        # 用于将 client_id 映射到整数索引
        self.client_id_to_index = {}
        # 整数索引计数器
        self.index_counter = 0

    def update_client(self, client_id, latitude, longitude, random_number):
        """
        更新或插入客户端数据到图和空间索引中
        
        :param client_id: 客户端唯一标识符
        :param latitude: 客户端的纬度
        :param longitude: 客户端的经度
        :param random_number: 客户端的随机数
        """
        if client_id in self.graph:
            # 如果客户端已经存在，更新其节点属性
            self.graph.nodes[client_id]['latitude'] = latitude
            self.graph.nodes[client_id]['longitude'] = longitude
            self.graph.nodes[client_id]['random_number'] = random_number
            
            # 更新空间索引
            index_id = self.client_id_to_index[client_id]
            old_bounds = (self.graph.nodes[client_id]['latitude'], self.graph.nodes[client_id]['longitude'],
                          self.graph.nodes[client_id]['latitude'], self.graph.nodes[client_id]['longitude'])
            self.idx.delete(index_id, old_bounds)  # 假设 delete() 方法已经实现
            new_bounds = (latitude, longitude, latitude, longitude)
            self.idx.insert(index_id, new_bounds)  # 假设 insert() 方法已经实现
        else:
            # 如果客户端不存在，新增节点到图中
            self.graph.add_node(client_id, latitude=latitude, longitude=longitude, random_number=random_number)
            
            # 为客户端生成新的索引
            index_id = self.index_counter
            self.client_id_to_index[client_id] = index_id
            self.index_counter += 1
            
            # 添加到空间索引
            bounds = (latitude, longitude, latitude, longitude)
            self.idx.insert(index_id, bounds)  # 假设 insert() 方法已经实现
        
        # 更新客户端的最后心跳时间
        self.last_heartbeat_times[client_id] = time.time()

    def get_nearest_clients(self, client_id):
        """
        获取指定客户端的最近 10 个客户端。返回一个列表，包含每个最近客户端的距离、ID 和随机数。

        :param client_id: 客户端的唯一标识符
        :return: 一个包含最近客户端信息的列表 [(距离, 客户端 ID, 随机数), ...]
        """
        if client_id not in self.graph.nodes:
            return []

        # 获取指定客户端的纬度和经度
        lat1 = self.graph.nodes[client_id]['latitude']
        lon1 = self.graph.nodes[client_id]['longitude']
        distances = []
        index_id_set = set()  # 用于记录已经处理过的 index_id，避免重复

        # 使用空间索引查找附近的客户端
        nearby_clients = list(self.idx.nearest((lat1, lon1, lat1, lon1), 10))
        # print(f"Nearby clients count: {len(nearby_clients)}")  # 打印附近客户端数量

        for index_id in nearby_clients:
            if index_id in index_id_set:
                continue  # 如果已经处理过这个 index_id，跳过
            index_id_set.add(index_id)  # 记录这个 index_id

            for cid, idx in self.client_id_to_index.items():
                if idx == index_id and cid != client_id:  # 排除自己与自己的比较
                    lat2 = self.graph.nodes[cid]['latitude']
                    lon2 = self.graph.nodes[cid]['longitude']
                    random_number = self.graph.nodes[cid]['random_number']
                    # 计算两点间的地理距离
                    distance = self.calculate_distance(lat1, lon1, lat2, lon2)
                    # 将距离、客户端 ID 和随机数存储到列表中
                    distances.append((distance, cid, random_number))
                    if len(distances) >= 10:  # 当达到 10 个时提前退出
                        break
            if len(distances) >= 10:  # 当达到 10 个时提前退出
                break

        # 如果不足 10 个，继续扩大搜索范围
        if len(distances) < 10:
            additional_clients = list(self.idx.nearest((lat1, lon1, lat1, lon1), 21))  # 扩大搜索范围
            for index_id in additional_clients:
                if index_id in index_id_set:
                    continue  # 如果已经处理过这个 index_id，跳过
                index_id_set.add(index_id)  # 记录这个 index_id

                for cid, idx in self.client_id_to_index.items():
                    if idx == index_id and cid != client_id:  # 排除自己与自己的比较
                        lat2 = self.graph.nodes[cid]['latitude']
                        lon2 = self.graph.nodes[cid]['longitude']
                        random_number = self.graph.nodes[cid]['random_number']
                        # 计算两点间的地理距离
                        distance = self.calculate_distance(lat1, lon1, lat2, lon2)
                        # 将距离、客户端 ID 和随机数存储到列表中
                        distances.append((distance, cid, random_number))
                        if len(distances) >= 10:  # 当达到 10 个时提前退出
                            break
                if len(distances) >= 10:  # 当达到 10 个时提前退出
                    break

        # print(f"Distances list count: {len(distances)}")  # 打印距离列表长度
        # 按照距离进行排序，返回距离最近的前 10 个客户端
        return sorted(distances, key=lambda x: x[0])[:10]

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        计算两地球坐标点之间的距离，单位为公里。

        :param lat1: 第一个地点的纬度
        :param lon1: 第一个地点的经度
        :param lat2: 第二个地点的纬度
        :param lon2: 第二个地点的经度
        :return: 两个地点之间的距离（公里）
        """
        R = 6371  # 地球的平均半径，单位为千米

        # 将纬度和经度从度转换为弧度
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)

        # Haversine 公式来计算球面距离
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # 计算并返回两点间的距离
        return R * c

    def clean_inactive_clients(self, aggressive=False):
        """
        清理超时的客户端信息
        """
        current_time = time.time()
        clients_to_remove = []
        for client_id, last_heartbeat_time in self.last_heartbeat_times.items():
            if aggressive:
                # 激进模式下，清理掉更长时间没有心跳的客户端
                if current_time - last_heartbeat_time > self.heartbeat_timeout * 2:
                    clients_to_remove.append(client_id)
            else:
                if current_time - last_heartbeat_time > self.heartbeat_timeout:
                    clients_to_remove.append(client_id)

        for client_id in clients_to_remove:
            if client_id in self.graph.nodes:
                index_id = self.client_id_to_index[client_id]
                self.graph.remove_node(client_id)
                # 从空间索引中删除
                bounds = (self.graph.nodes[client_id]['latitude'], self.graph.nodes[client_id]['longitude'],
                        self.graph.nodes[client_id]['latitude'], self.graph.nodes[client_id]['longitude'])
                self.idx.delete(index_id, bounds)
                del self.client_id_to_index[client_id]
            del self.last_heartbeat_times[client_id]

    def get_client_data(self, client_id):
        """
        根据客户端ID获取客户端数据

        :param client_id: 客户端的唯一标识符
        :return: 客户端数据字典，如果客户端不存在则返回 None
        """
        if client_id in self.graph.nodes:
            return self.graph.nodes[client_id]
        return None

    def get_client_weight(self, client_id):
        """
        根据客户端ID获取客户端权重（这里假设权重就是随机数）

        :param client_id: 客户端的唯一标识符
        :return: 客户端权重，如果客户端不存在则返回 None
        """
        client_data = self.get_client_data(client_id)
        if client_data:
            return client_data.get('random_number')
        return None