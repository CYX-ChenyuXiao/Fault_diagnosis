from datetime import datetime
from typing import Dict

import grpc

import metadata_store_pb2_grpc
import data_management_pb2
import metadata_store_pb2


class ModelTrainingHandler:
    def __init__(self, metadata_store_url: str, job_id: str, rank: int, dataset_id: str, version_hash: str,
                 code_version: str, model_name: str):
        channel = grpc.insecure_channel(metadata_store_url)
        self.stub = metadata_store_pb2_grpc.MetadataStoreServiceStub(channel)
        self.run_id = job_id
        self.rank = rank
        self.tracing = metadata_store_pb2.TracingInformation(
            dataset_id=dataset_id,
            version_hash=version_hash,
            code_version=code_version
        )
        self.model_name = model_name

    def log_run_start(self):
        return self.stub.LogRunStart(metadata_store_pb2.LogRunStartRequest(
            start_time=datetime.now().isoformat(),
            run_id=self.run_id,
            run_name="training job {}".format(self.run_id),
            tracing=self.tracing
        ))

    def log_run_end(self, is_success: bool, message: str):
        return self.stub.LogRunEnd(metadata_store_pb2.LogRunEndRequest(
            run_id=self.run_id,
            end_time=datetime.now().isoformat(),
            success=is_success,
            message=message,
        ))

    def log_epoch(self, started: str, epoch_id: int, metrics: Dict[str, str]):
        return self.stub.LogEpoch(metadata_store_pb2.LogEpochRequest(
            epoch_info=metadata_store_pb2.EpochInfo(
                start_time=started,
                end_time=datetime.now().isoformat(),
                run_id=self.run_id,
                epoch_id="{}-{}".format(self.rank, epoch_id),
                metrics=metrics
            )))

    def create_artifact(self, model_bucket: str, model_object_name: str, algorithm: str):
        return self.stub.CreateArtifact(metadata_store_pb2.CreateArtifactRequest(
            artifact=data_management_pb2.FileInfo(
                name=self.model_name,
                bucket=model_bucket,
                path=model_object_name,
            ),
            run_id=self.run_id,
            algorithm=algorithm,
        ))
