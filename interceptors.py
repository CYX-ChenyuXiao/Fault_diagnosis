from utils.orca3_utils import ModelTrainingHandler


class TrainingInterceptor:
    def __init__(self, context):
        self.context = context
        self.interceptor = ModelTrainingHandler(context.config.METADATA_STORE_SERVER, context.config.JOB_ID,
                                                context.config.RANK,
                                                context.config.TRAINING_DATASET_ID,
                                                context.config.TRAINING_DATASET_VERSION_HASH,
                                                context.config.MODEL_VERSION,
                                                context.config.MODEL_NAME)

    def starting(self):
        self.interceptor.log_run_start()

    def failure(self):
        self.interceptor.log_run_end(False, 'fail to complete training job.')

    def success(self):
        self.interceptor.log_run_end(True, 'success to complete training job.')
        return self.interceptor.create_artifact(self.context.get_model_bucket(), self.context.get_model_path(),
                                                self.context.algorithm_name)
