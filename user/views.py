from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from user.services.user_service import create_user


# 유저 View
class UserView(APIView):
    # 유저 생성
    def post(self, request):
        user_obj = create_user(**request.data)
        if user_obj:
            return Response({"sucess": "유저 생성 성공"}, status=status.HTTP_200_OK)
        return Response({"error" : "유저 생성 실패"}, status=status.HTTP_400_BAD_REQUEST)