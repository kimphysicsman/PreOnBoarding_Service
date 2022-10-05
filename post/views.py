from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from post.serializers import (
    PostModelSerializer    
)
from post.services.post_service import (
    create_post
)

# 게시글 View
class PostView(APIView):
    # 게시글 생성
    def post(self, request):
        user_obj = request.user
        try:
            create_post(user_obj=user_obj, **request.data)
            return Response({"seccess" : "게시글 생성 성공"}, status=status.HTTP_200_OK)
        except:
            return Response({"error" : "게시글 생성 실패"}, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 수정
    def put(self, request, post_id):
        print(post_id)
        return Response({}, status=status.HTTP_200_OK)