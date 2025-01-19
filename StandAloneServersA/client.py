import grpc
import heartbeat_pb2  
import heartbeat_pb2_grpc  
import random  
import time

# 单例模式实现连接池
class GrpcConnectionPool:
    _instance = None
    _channel = None
    _stub = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._channel = grpc.insecure_channel('localhost:50051')
            cls._stub = heartbeat_pb2_grpc.HeartbeatServiceStub(cls._channel)
        return cls._instance

    @property
    def channel(self):
        return self._channel

    @property
    def stub(self):
        return self._stub

# 发送心跳信息的函数
def send_heartbeat(client_id, latitude, longitude):
    # 这里应该生成一个随机数，模拟用户等级
    random_number = random.randint(0, 100)  # 示例，生成 0 到 100 之间的随机整数
    # 获取连接池实例
    connection_pool = GrpcConnectionPool()
    stub = connection_pool.stub
    # 构建请求
    request = heartbeat_pb2.HeartbeatRequest(client_id=client_id, latitude=latitude, longitude=longitude, random_number=random_number)
    # 发送请求
    response = stub.Heartbeat(request)
    # 打印发送心跳请求后的状态
    print("Sent heartbeat for client {}: {}".format(client_id, response.status))
    return response

# 查询最近的客户端信息的函数
def query_nearest_clients(client_id):
    try:
        # 获取连接池实例
        connection_pool = GrpcConnectionPool()
        stub = connection_pool.stub
        # 构建 ClientLocationRequest 消息，只需包含当前客户端的 ID
        request = heartbeat_pb2.ClientLocationRequest(client_id=client_id)
        
        # 调用服务端的 GetNearestClients 方法获取响应
        response = stub.GetNearestClients(request)
        
        print(f"Received {len(response.clients)} nearest clients for client {client_id}")  # Debug

        # 遍历响应中的每个客户端信息，并打印出客户端的 ID、与当前客户端的距离和随机数
        for client in response.clients:
            print(f"Client {client.client_id} - Distance: {client.distance} km, Random Number: {client.random_number}")
    except Exception as e:
        print(f"Error querying nearest clients: {e}")

# 建立连接
def run(client_id):
    # 无限循环，不断发送心跳信息
    while True:
        # 随机生成经纬度
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        
        # 发送心跳请求
        send_heartbeat(client_id, latitude, longitude)
        
        # 查询最近的客户端并打印信息
        query_nearest_clients(client_id)
        
        # 每 30 秒执行一次循环（发送心跳并查询客户端）
        time.sleep(30)

# 关闭通道
def close_channel():
    connection_pool = GrpcConnectionPool()
    connection_pool.channel.close()

# 程序入口，检查是否为主模块运行
if __name__ == '__main__':
    try:
        # 运行函数
        run('client_1')
    finally:
        # 关闭通道
        close_channel()