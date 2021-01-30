# grpcio 是启动 gRPC 服务的项目依赖
# pip3 install grpcio
# gPRC tools 包含 protocol buffer 编译器和用于从 .proto 文件生成服务端和客户端代码的插件
# pip3 install grpcio-tools
# 升级protobuf
# pip3 install --upgrade protobuf -i https://pypi.douban.com/simple

import grpc
import time
import schema_pb2
import schema_pb2_grpc
from concurrent import futures
 
 
class GatewayServer(schema_pb2_grpc.GatewayServicer):
 
    def Call(self, request_iterator, context):
        for req in request_iterator:
            yield schema_pb2.Response(num=req.num+1)
            time.sleep(1)
 
 
def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    schema_pb2_grpc.add_GatewayServicer_to_server(GatewayServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)
 
 
if __name__ == "__main__":
    main()