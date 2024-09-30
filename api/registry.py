"""
PaddleHelix API集合
"""


class APIConfig:
    def __init__(self, name: str, uri):
        self.name = name
        self.uri = uri


class ServerAPIRegistry:
    class HelixFold3:
        name = "helixfold3"
        submit = APIConfig("submit", "/api/submit/helixfold3")
        batch_submit = APIConfig("batch_submit", "/api/submit/helixfold3")

    class Common:
        query_task_info = APIConfig("query_task_info", "/api/task/info")


class ClientAPIRepository:
    download_result = APIConfig("download_result", "")
