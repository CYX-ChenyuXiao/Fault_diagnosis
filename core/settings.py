import os
import sys


class TrainingConfig:
    @staticmethod
    def int_or_default(variable, default):
        if variable is None:
            return default
        else:
            return int(variable)

    def __str__(self) -> str:
        if not "PROD".__eq__(self.ENV.upper()):
            return "model training settings"

        results = [
            "'{}' training settings".format(self.MODEL_NAME),
            "\nbackend service settings:",
            "{}={}".format("JOB_ID", self.JOB_ID),
            "{}={}".format("ALGORITHM_NAME", self.ALGORITHM_NAME),
            "{}={}".format("TRAINING_DATA_BUCKET", self.TRAINING_DATA_BUCKET),
            "{}={}".format("TRAINING_DATA_PATH", self.TRAINING_DATA_PATH),
            "{}={}".format("TRAINING_DATASET_ID", self.TRAINING_DATASET_ID),
            "{}={}".format("TRAINING_DATASET_VERSION_HASH", self.TRAINING_DATASET_VERSION_HASH),
            "{}={}".format("METADATA_STORE_SERVER", self.METADATA_STORE_SERVER),
            "{}={}".format("MINIO_SERVER", self.MINIO_SERVER),
            "{}={}".format("MINIO_SERVER_ACCESS_KEY", self.MINIO_SERVER_ACCESS_KEY),
            "{}={}".format("MINIO_SERVER_SECRET_KEY", self.MINIO_SERVER_SECRET_KEY),
            "{}={}".format("MODEL_BUCKET", self.MODEL_BUCKET),
            "\nuser settings:",
            "{}={}".format("EPOCHS", self.EPOCHS), "{}={}".format("LR", self.LR),
            "{}={}".format("BATCH_SIZE", self.BATCH_SIZE),
            "{}={}".format("FC_SIZE", self.FC_SIZE),
            "\nalgorithms settings:",
            "{}={}".format("ENV", self.ENV),
            "{}={}".format("MODEL_VERSION", self.MODEL_VERSION),
            "{}={}".format("MODEL_SERVING_VERSION", self.MODEL_SERVING_VERSION),
            "{}={}".format("WORLD_SIZE", self.WORLD_SIZE),
            "{}={}".format("RANK", self.RANK),
            "{}={}".format("MASTER_ADDR", self.MASTER_ADDR),
            "{}={}".format("MASTER_PORT", self.MASTER_PORT),
        ]
        return "\n".join(results)

    def __init__(self):
        ######################## define in the backend services ###########################
        self.JOB_ID = os.getenv('JOB_ID') or "12"
        self.ALGORITHM_NAME = os.getenv('ALGORITHM_NAME') or "test-1"
        self.METADATA_STORE_SERVER = os.getenv('METADATA_STORE_SERVER') or "127.0.0.1:6002"
        self.DATA_MANAGEMENT_SERVER = os.getenv('DATA_MANAGEMENT_SERVER') or "127.0.0.1:6000"
        self.TRAINING_DATASET_ID = os.getenv('TRAINING_DATASET_ID') or "20"
        self.TRAINING_DATASET_VERSION_HASH = os.getenv('TRAINING_DATASET_VERSION_HASH') or "hashDg=="
        self.MODEL_BUCKET = os.getenv('MODEL_BUCKET') or "tdu-platform-ms"
        self.MODEL_NAME = os.getenv('MODEL_NAME') or "test"
        # docker: minio:9000, local: 127.0.0.1:9000
        self.MINIO_SERVER = os.getenv('MINIO_SERVER') or "127.0.0.1:9000"
        self.MINIO_SERVER_ACCESS_KEY = os.getenv('MINIO_SERVER_ACCESS_KEY') or "foooo"
        self.MINIO_SERVER_SECRET_KEY = os.getenv('MINIO_SERVER_SECRET_KEY') or "barbarbar"
        self.TRAINING_DATA_BUCKET = os.getenv('TRAINING_DATA_BUCKET') or "tdu-platform-dm"
        self.TRAINING_DATA_PATH = os.getenv('TRAINING_DATA_PATH') or "datasets/20/versions-snapshots/hashAABQ"
        ######################## define in the frontend of UI ###########################
        self.EPOCHS = self.int_or_default(os.getenv('EPOCHS'), 1)
        self.LR = self.int_or_default(os.getenv('LR'), 5)
        self.BATCH_SIZE = self.int_or_default(os.getenv('BATCH_SIZE'), 64)
        self.FC_SIZE = self.int_or_default(os.getenv('FC_SIZE'), 128)
        ######################## define in the algorithm side ###########################
        self.MODEL_VERSION = "1.0"
        self.MODEL_SERVING_VERSION = os.getenv('MODEL_SERVING_VERSION') or "1.0"
        self.MODEL_OBJECT_NAME = "model"
        self.ENV = os.environ.get('ENV') or "dev"
        ######################## static values that haven't defined in the platform ###########################
        # distributed training related settings
        self.WORLD_SIZE = self.int_or_default(os.getenv('WORLD_SIZE'), 1)
        self.RANK = self.int_or_default(os.getenv('RANK'), 0)
        self.MASTER_ADDR = os.getenv('MASTER_ADDR') or "localhost"
        os.environ['MASTER_ADDR'] = self.MASTER_ADDR
        self.MASTER_PORT = os.getenv('MASTER_PORT') or "12356"
        os.environ['MASTER_PORT'] = self.MASTER_PORT
        if len(sys.argv) == 3:
            self.RANK = int(sys.argv[1])
            self.WORLD_SIZE = int(sys.argv[2])


class PredictConfig:

    def __str__(self) -> str:
        if not "PROD".__eq__(self.ENV.upper()):
            return "predict service settings"

        results = [
            "predict service settings",
            "{}={}".format("ENV", self.ENV),
            "{}={}".format("MINIO_SERVER", self.MINIO_SERVER),
            "{}={}".format("MINIO_SERVER_ACCESS_KEY", self.MINIO_SERVER_ACCESS_KEY),
            "{}={}".format("MINIO_SERVER_SECRET_KEY", self.MINIO_SERVER_SECRET_KEY),
            "{}={}".format("MODEL_BUCKET", self.MODEL_BUCKET),
            "{}={}".format("MODEL_PATH", self.MODEL_PATH),
        ]

        return "\n".join(results)

    def __init__(self):
        self.ENV = os.environ.get('ENV') or "dev"
        # docker: minio:9000, local: 127.0.0.1:9000
        self.MINIO_SERVER = os.getenv('MINIO_SERVER') or "127.0.0.1:9000"
        self.MINIO_SERVER_ACCESS_KEY = os.getenv('MINIO_SERVER_ACCESS_KEY') or "foooo"
        self.MINIO_SERVER_SECRET_KEY = os.getenv('MINIO_SERVER_SECRET_KEY') or "barbarbar"
        self.MODEL_BUCKET = os.getenv('MODEL_BUCKET') or "tdu-platform-ms"
        self.MODEL_PATH = os.getenv('MODEL_PATH') or "artifacts/intent-classification-test-0918"
