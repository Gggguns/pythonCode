import grpc
from dataManager import ClientDataManager
import heartbeat_pb2
import heartbeat_pb2_grpc
import time
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor  # 导入 ThreadPoolExecutor
import threading

# 创建一个清理锁
cleanup_lock = threading.Lock()
# 创建一个锁
connection_lock = threading.Lock()
#最大连接数
max_connections = 0

# HeartbeatServiceServicer 类继承自 gRPC 生成的 HeartbeatServiceServicer 基类
# 这是服务端的实现，处理客户端发来的请求
class HeartbeatServiceServicer(heartbeat_pb2_grpc.HeartbeatServiceServicer):
    def __init__(self):
        # 初始化一个 ClientDataManager 实例，用来管理客户端数据
        self.data_manager = ClientDataManager()
        # 初始化一个本地变量来存储连接数
        self.current_connections = 0

    # Heartbeat 方法用于处理客户端的心跳请求
    def Heartbeat(self, request, context):
        global max_connections
        # 获取锁
        with connection_lock:
            # 连接数加1
            self.current_connections += 1
            if self.current_connections > max_connections:
                max_connections = self.current_connections
        print(f"Max current connections: {max_connections}")
        # Debug
        #time.sleep(10)
        
        # 从请求中提取客户端信息
        client_id = request.client_id
        latitude = request.latitude
        longitude = request.longitude
        random_number = request.random_number

        print(f"Received heartbeat from client {client_id}")  # Debug

        # 调用数据管理器的 update_client 方法更新客户端的状态
        with cleanup_lock:
            self.data_manager.update_client(client_id, latitude, longitude, random_number)

        try:
            # 返回响应
            return heartbeat_pb2.HeartbeatResponse(status="OK")
        finally:
            # 获取锁
            with connection_lock:
                # 连接数减1
                self.current_connections -= 1
            #print(f"Current connections: {self.current_connections}")
    
    # GetNearestClients 方法用于处理获取最近客户端信息的请求
    def GetNearestClients(self, request, context):
        global max_connections
        # 获取锁
        with connection_lock:
            # 连接数加1
            self.current_connections += 1
            if self.current_connections > max_connections:
                max_connections = self.current_connections
        print(f"Max current connections: {max_connections}")
        # Debug
        time.sleep(10)
        # 从请求中提取客户端的唯一标识符
        client_id = request.client_id

        # 记录查询开始时间
        start_time = time.time()

        # 获取与指定客户端最近的客户端列表
        with cleanup_lock:
            nearest_clients = self.data_manager.get_nearest_clients(client_id)

        # 记录查询结束时间
        end_time = time.time()

        # 计算并输出查询时间
        query_time = end_time - start_time
        print(f"Query time for client {client_id}: {query_time} seconds")

        # 创建一个响应对象，用于返回给客户端
        response = heartbeat_pb2.ClientLocationResponse()

        # 遍历最近客户端数据，将其加入到响应的 clients 列表中
        for dist, cid, random_number in nearest_clients:
            # 向响应中添加一个客户端信息
            response.clients.add(client_id=cid, random_number=random_number, distance=dist)

        try:
            # 返回响应
            return response
        finally:
            # 获取锁
            with connection_lock:
                # 连接数减1
                self.current_connections -= 1
            #print(f"Current connections: {self.current_connections}")

# serve 函数用于启动 gRPC 服务器并提供服务
def serve():
    # 创建一个线程池
    thread_pool = ThreadPoolExecutor(max_workers=2000)  # 可以根据需要调整最大工作线程数

    # 创建一个 gRPC 服务器实例，使用最大工作线程数
    max_concurrent_streams = 2000  # 调整为更合适的值
    server = grpc.server(thread_pool, options=[
        ('grpc.max_concurrent_streams', max_concurrent_streams),  # 设置最大并发流数
        ('grpc.max_send_message_length', 1024 * 1024 * 10),  # 设置最大发送消息长度
        ('grpc.max_receive_message_length', 1024 * 1024 * 10)  # 设置最大接收消息长度
    ])

    # 输出最大连接数（这里近似为最大并发流数）
    print(f"Max connections (approximate, based on max concurrent streams): {max_concurrent_streams}")

    # 将 HeartbeatServiceServicer 实例添加到服务器
    heartbeat_pb2_grpc.add_HeartbeatServiceServicer_to_server(HeartbeatServiceServicer(), server)

    # 设置服务器监听端口为 50051
    server.add_insecure_port('[::]:50051')

    # 启动服务器
    server.start()

    # 打印服务器启动的消息
    print("Server started on port 50051")

    # 启动一个任务来定期清理无效客户端
    def clean_inactive_clients_periodically():
        servicer = HeartbeatServiceServicer()
        while True:
            with cleanup_lock:
                servicer.data_manager.clean_inactive_clients()
            time.sleep(10)  # 每 10 秒清理一次

    # 启动一个任务来监控内存使用情况
    def monitor_memory_usage():
        memory_threshold = 80  # 内存使用阈值，单位为百分比
        servicer = HeartbeatServiceServicer()
        while True:
            # 获取当前内存使用百分比
            memory_percent = psutil.virtual_memory().percent
            if memory_percent > memory_threshold:
                print(f"Memory usage is high ({memory_percent}%), performing aggressive cleanup...")
                with cleanup_lock:
                    # 进行更激进的清理，例如清理掉长时间没有心跳的客户端
                    servicer.data_manager.clean_inactive_clients(aggressive=True)
            time.sleep(60)  # 每 60 秒检查一次

    # 创建并启动清理任务
    threading.Thread(target=clean_inactive_clients_periodically, daemon=True).start()
    # 创建并启动内存监控任务
    threading.Thread(target=monitor_memory_usage, daemon=True).start()

    # 阻塞等待服务器的终止
    server.wait_for_termination()

# 入口点，调用 serve 函数启动服务器
if __name__ == '__main__':
    serve()

# 入口点，调用 serve 函数启动服务器
if __name__ == '__main__':
    serve()