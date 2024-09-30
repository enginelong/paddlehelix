"""
API客户端
"""

from api.api_common import CommonClient
from api.api_helixfold3 import HelixFold3Client
from config import auth_config_manager

_auth_config = auth_config_manager.load_config()
_ak, _sk = auth_config_manager.parse_api_ak_sk_from_auth_config(_auth_config)


class APIClient:
    Common = CommonClient(_ak, _sk)
    HelixFold3 = HelixFold3Client(_ak, _sk)


