from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from post.serializers import (
    PostModelSerializer    
)
from post.services.post_service import (
    create_post,
    check_author,
    update_post,
)

# 게시글 View
class PostView(APIView):
    # 게시글 생성
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "서비스를 이용하기 위해 로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            create_post(user_obj=user, **request.data)
            return Response({"seccess" : "게시글 생성 성공"}, status=status.HTTP_200_OK)
        except:
            return Response({"error" : "게시글 생성 실패"}, status=status.HTTP_400_BAD_REQUEST)

    # 게시글 수정
    def put(self, request, post_id):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "서비스를 이용하기 위해 로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not check_author(post_id, user):
            return Response({"detail": "본인의 게시글만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        try:
            update_post(post_id, **request.data)
            return Response({"seccess" : "게시글 수정 성공"}, status=status.HTTP_200_OK)
        
        except:
            return Response({"error" : "게시글 수정 실패"}, status=status.HTTP_400_BAD_REQUEST)

        