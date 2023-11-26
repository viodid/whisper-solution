from azure.storage.blob import BlobServiceClient


# try:
#     print("Azure Blob Storage Python quickstart sample")
#     connect_str = Config.AZURE_STORAGE_CONNECTION_STRING
#
#     # Create the BlobServiceClient object
#     blob_service_client = BlobServiceClient.from_connection_string(connect_str)
#     blob_service_client.get_container_client(Config.BLOB_STORAGE_CONTAINER_NAME).list_blobs()
#
#     # Quickstart code goes here
#
#
# except Exception as ex:
#     print('Exception:')
#     print(ex)


class BlobStorage:
    def __init__(self, conn: str, container: str):
        self.conn = conn
        self.container = container
        self.blob_service_client = BlobServiceClient.from_connection_string(self.conn)
        self.container_client = self.blob_service_client.get_container_client(self.container)

    def list_blobs(self):
        blobs_list = self.container_client.list_blobs()
        return blobs_list

    def download_blob(self, blob_name, local_path):
        with open(file=local_path, mode="wb") as download_file:
            download_file.write(self.container_client.download_blob(blob_name).readall())

    def remove_blob(self, blob_name):
        self.container_client.delete_blob(blob_name)
