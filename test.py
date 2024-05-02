import grpc
import prediction_service_pb2
import prediction_service_pb2_grpc

channel = grpc.insecure_channel("localhost:51001")
stub = prediction_service_pb2_grpc.PredictorStub(channel)
print('\n ------ ------ ----- test ------ ------ ----- \n')
# tdu-platform-dm 为bucket
# ###为连接符
# datasets/20/versions-snapshots/hashAABQ为具体路劲
request_folder = 'tdu-platform-dm###datasets/20/versions-snapshots/hashAABQ'
result = stub.PredictorPredict(
    prediction_service_pb2.PredictorPredictRequest(
        document=request_folder
    )
)

print(result)
