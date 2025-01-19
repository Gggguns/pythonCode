import threading
import random
from client import run

# 服务器地址
SERVER_ADDRESS = 'localhost:50051'


def main():
    num_clients = 2000
    threads = []

    # 创建并启动线程
    for i in range(num_clients):
        client_id = f"client_{i}"
        thread = threading.Thread(target=run, args=(client_id,))
        threads.append(thread)
        # 启动线程
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("All clients have finished requesting services.")

if __name__ == '__main__':
    main()