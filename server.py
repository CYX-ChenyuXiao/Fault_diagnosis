from concurrent import futures
import grpc
from grpc import ServicerContext
import os
import prediction_service_pb2
import prediction_service_pb2_grpc as prediction_service
from grpc_health.v1 import health_pb2_grpc, health

from context import PredictContext
from predict import ModelPredict
from store import Repository
from pathlib import Path
from utils.file_utils import remove_directory, mkdir_directory
from datetime import datetime


class ModelLoadingError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class PredictorServicer(prediction_service.PredictorServicer):

    def __init__(self, context, repository, predict_service):
        self.context = context
        self.repository = repository
        self.predict_service = predict_service

    def PredictorPredict(self, request, context: ServicerContext):
        try:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'request to predict')
            mkdir_directory(Path(self.context.inputs_folder))
            mkdir_directory(Path(self.context.outputs_folder))
            if self.context.is_prod():
                contact = "###"
                data_info = request.document.split(contact)
                bucket = data_info[0]
                path = data_info[1]
                # 1. remove history request
                remove_directory(Path(self.context.inputs_folder))
                print(f'remove history request in {self.context.inputs_folder}')
                remove_directory(Path(self.context.outputs_folder))
                print(f'remove history result in {self.context.outputs_folder}')
                # 2 download current request
                self.repository.download_input_paths(bucket, path, self.context.inputs_folder)
                print(f'download request from {bucket}/{path}')
                # 3. predict by model
                self.predict_service.predict()
                # 4. upload result to minio
                minio_path = f'{path}/outputs'
                self.repository.upload_local_folder_to_minio(local_path=self.context.outputs_folder, bucket_name=bucket,
                                                             minio_path=minio_path)
                print(f'upload result to {bucket}/{minio_path}')
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'finish\n')
                return prediction_service_pb2.PredictorPredictResponse(
                    response=f'{bucket}{contact}{minio_path}')
            # develop environment
            self.predict_service.predict()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'finish\n')
            return prediction_service_pb2.PredictorPredictResponse(
                response=f'success to store result in {self.context.outputs_folder}')
        except ModelLoadingError as ex:
            context.abort(ex.status_code, ex.message)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    context = PredictContext()
    print('\n ------ ------ ----- context initial ------ ------ ----- \n')
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), context.config)
    repository = Repository(context.config.MINIO_SERVER, context.config.MINIO_SERVER_ACCESS_KEY,
                            context.config.MINIO_SERVER_SECRET_KEY)
    # download model
    print('\n ------ ------ ----- model loading ------ ------ ----- \n')
    mkdir_directory(Path(context.model_folder))
    if context.is_prod() and context.model_bucket and context.model_path:
        remove_directory(Path(context.model_folder))
        print(f'remove history result in {context.model_folder}')
        repository.download_input_paths(context.model_bucket, context.model_path, context.model_folder)
        print(f'download model from {context.model_bucket}/{context.model_path}')
    print(f'load model in {context.model_folder}')
    print('\n ------ ------ ----- serving ------ ------ ----- \n')
    predict_model = ModelPredict(context.inputs_folder, context.outputs_folder, context.model_folder)
    prediction_service.add_PredictorServicer_to_server(
        PredictorServicer(context, repository, predict_model), server)
    health_servicer = health.HealthServicer(
        experimental_non_blocking=True,
        experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=10))
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    server.add_insecure_port('0.0.0.0:51001')
    server.start()
    print("server is running\n\n")
    server.wait_for_termination()


if __name__ == "__main__":
    main()
