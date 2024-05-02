import os
import glob
from minio import Minio


class Repository:
    def __init__(self, host, user, password):
        self.client = Minio(
            host,
            access_key=user,
            secret_key=password,
            secure=False
        )

    def download_input_paths(self, bucket, path, inputs_path):
        # print('start download inputs')
        data_files = self.client.list_objects(bucket, path, recursive=True)
        for item in data_files:
            self.client.fget_object(bucket, item.object_name,
                                    "{0}/{1}".format(inputs_path, os.path.relpath(item.object_name, path)))
        # print('success to download inputs: {0}'.format(inputs_path))
        return inputs_path

    def upload_local_folder_to_minio(self, local_path, bucket_name, minio_path):
        if not os.path.isfile(local_path):
            # hidden files (files starting with .) will not be found when use glob.glob
            for local_file in glob.glob(local_path + '/**'):
                local_file = local_file.replace(os.sep, "/")
                relative_path = os.path.dirname(local_file).replace(local_path, "")
                if relative_path == "":
                    self.upload_local_folder_to_minio(local_file, bucket_name, minio_path)
                else:
                    self.upload_local_folder_to_minio(
                        local_file, bucket_name, minio_path + "/" + relative_path)
        else:
            remote_path = os.path.join(minio_path, os.path.basename(local_path))
            self.client.fput_object(bucket_name, remote_path, local_path)
