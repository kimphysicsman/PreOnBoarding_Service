
from user.serializers import UserModelSerializer

def create_user(email, username, password):
    """유저 오브젝트 생성 함수

    Args:
        email (str): 유저 이메일
        username (str): 유저 이름
        password (str): 유저 비밀번호

    Returns:
        UserModel: 생성된 유저 오브젝트 
    """
    
    user_info = {
        "email": email,
        "username" : username,
        "password" : password,
    }

    serializer = UserModelSerializer(data=user_info)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.instance