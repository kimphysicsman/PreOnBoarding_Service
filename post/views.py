from xml.dom import ValidationErr
from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response

from post.serializers import (
    PostModelSerializer    
)
from post.services.post_service import (
    create_post,
    check_author,
    delete_post,
    update_post,
    get_post_obj,
    get_post_info,
    increase_views,
    recover_post,
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
            return Response({"success" : "게시글 생성 성공"}, status=status.HTTP_200_OK)
        
        except exceptions.ValidationError:
            return Response({"detial" : "입력값이 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"error" : "게시글 생성 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 게시글 수정
    def put(self, request, post_id):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "서비스를 이용하기 위해 로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        
        post_obj = get_post_obj(post_id)
        if not post_obj or not post_obj.is_active:
            return Response({"detail": "해당 게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        if not check_author(post_obj, user):
            return Response({"detail": "접근 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        try:
            update_post(post_obj, **request.data)
            return Response({"success" : "게시글 수정 성공"}, status=status.HTTP_200_OK)
        
        except exceptions.ValidationError:
            return Response({"detial" : "입력값이 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"error" : "게시글 수정 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    # 게시글 삭제(비활성화)
    def delete(self, request, post_id):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "서비스를 이용하기 위해 로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        
        post_obj = get_post_obj(post_id)
        if not post_obj or not post_obj.is_active:
            return Response({"detail": "해당 게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        if not check_author(post_obj, user):
            return Response({"detail": "접근 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        try:
            delete_post(post_obj)
            return Response({"success": "게시글 삭제 성공"}, status=status.HTTP_200_OK)

        except:
            return Response({"error": "게시글 삭제 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 게시글 상세 조회
    def get(self, request, post_id):
        post_obj = get_post_obj(post_id)
        if not post_obj or not post_obj.is_active:
            return Response({"detail": "해당 게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        try:
            increase_views(post_obj)
            post_info = get_post_info(post_obj, request.user)
            return Response(post_info, status=status.HTTP_200_OK)

        except:
            return Response({"error": "게시글 조회 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 게시글 복구 View
class RecoverPostView(APIView):
    
    # 게시글 복구
    def put(self, request, post_id):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "서비스를 이용하기 위해 로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
                
        post_obj = get_post_obj(post_id)
        if not post_obj or post_obj.is_active:
            return Response({"detail": "해당 게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        if not check_author(post_obj, user):
            return Response({"detail": "접근 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        try:
            recover_post(post_obj)
            return Response({"success": "게시글 복구 성공"}, status=status.HTTP_200_OK)

        except:
            return Response({"error": "게시글 복구 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
