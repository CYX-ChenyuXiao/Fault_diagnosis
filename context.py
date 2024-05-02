from core.settings import TrainingConfig, PredictConfig


class TrainingContext:
    def __init__(self):
        self.config = TrainingConfig()
        self.algorithm_name = self.config.ALGORITHM_NAME
        self.model_inputs_folder = './train_inputs'
        self.model_outputs_folder = './train_outputs'
        self.history_model_folder = './model_data'

    def set_inputs(self, bucket, path):
        self.config.TRAINING_DATA_BUCKET = bucket
        self.config.TRAINING_DATA_PATH = path

    def set_task_id(self, task_id):
        self.config.JOB_ID = task_id

    def is_prod(self):
        return self.config.ENV and "PROD".__eq__(self.config.ENV.upper())

    def get_model_bucket(self):
        return self.config.MODEL_BUCKET

    def get_model_path(self):
        # todo: how to get history task
        return f'run_{self.config.JOB_ID}'

    def get_history_model_path(self):
        return f'run_{self.config.JOB_ID}'


class PredictContext:

    def __init__(self):
        self.config = PredictConfig()
        self.model_bucket = self.config.MODEL_BUCKET
        self.model_path = self.config.MODEL_PATH
        self.inputs_folder = './requests'
        self.outputs_folder = './responses'
        self.model_folder = './model_data'

    def is_prod(self):
        return self.config.ENV and "PROD".__eq__(self.config.ENV.upper())
