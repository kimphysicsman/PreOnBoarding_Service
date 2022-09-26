from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# 게시글 View
class PostView(APIView):
    # 게시글 생성
    def post(self, request):
        return Response({}, status=status.HTTP_200_OK)