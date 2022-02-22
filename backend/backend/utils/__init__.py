from rest_framework_jwt import utils


def create_jwt(user: object):
    """
    生成json web token
    :param user: 用户模型对象
    :return:
    """

    payload = utils.jwt_payload_handler(user)
    token = utils.jwt_encode_handler(payload)

    return token
