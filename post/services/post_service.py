from django.db.models.query_utils import Q

from post.models import (
    Post as PostModel,
    Hashtag as HashtagModel,
    PostHashtag as PostHashtagModel,
    Like as LikeModel
)
from post.serializers import (
    PostModelSerializer,
    PostModelListSerializer,
    )

def parsing_hashtags(hashtags):
    """해시태그 문자열을 리스트로 파싱하는 함수

    Args:
        hashtags (str): 해시태그 문자열 ex) "#게임,#코딩,#일상"

    Returns:
        list: 해시태그 단어 리스트 ex) ["게임", "코딩", "일상"]
    """

    hashtag_list = hashtags.split(",")

    hashtag_words = [ word[1:] for word in hashtag_list if check_hashtag(word) ]

    return hashtag_words


def check_hashtag(word):
    """해시태그인지 검사하는 함수
       첫번째 문자가 #이면 True, 아니면 False

    Args:
        word (str): 검사할 단어 ex) "#게임" / "게임"

    Returns:
        bool: 해시태그 여부 ex) True / False
    """

    return word.startswith('#')


def get_hashtag(hashtag_word):
    """해시태그 단어로 해시태그 오브젝트를 반환하는 함수
       해당 해시태그 오브젝트가 없으면 새롭게 생성

    Args:
        hashtag_word (str): 해시태그 단어

    Returns:
        HashtagModel: 해시태그 오브젝트
    """

    hashtag_obj, created = HashtagModel.objects.get_or_create(name=hashtag_word)

    return hashtag_obj


def create_post(user_obj, title, content, hashtags):
    """게시글 생성 함수

    Args:
        user_obj (UserModel): 작성자(유저) 오브젝트
        title (str): 제목
        content (str): 내용
        hashtags (str): 해시태그 문자열

    Returns:
        PostModel: 생성된 게시글 오브젝트
    """

    data = {
        "title": title,
        "content": content,
        "views": 0,
        "is_active": True
    }

    serializer = PostModelSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=user_obj)
    
    post_obj = serializer.instance

    hashtag_words = parsing_hashtags(hashtags)
    hashtag_objs = [get_hashtag(word) for word in hashtag_words]

    for obj in hashtag_objs:
        PostHashtagModel.objects.get_or_create(hashtag=obj, post=post_obj)

    return post_obj


def get_post_obj(post_id):
    """게시글 오브젝트 반환 함수

    Args:
        post_id (int): 게시글 id

    Returns:
        PostModel: 게시글 오브젝트
                    해당 게시글이 없으면 None 반환
    """

    try:
        post_obj = PostModel.objects.get(id=post_id)
        return post_obj
    except:
        return None


def check_author(post_obj, user_obj):
    """해당 유저가 게시글의 작성자가 맞는지 확인하는 함수

    Args:
        post_obj (PostModel): 게시글 오브젝트
        user_obj (UserModel): 확인할 유저

    Returns:
        bool: 일치 여부
    """

    return post_obj.user == user_obj


def update_post(post_obj, title=None, content=None, hashtags=None):
    """게시글 수정 함수

    Args:
        post_obj (PostModel): 수정할 게시글 오브젝트
        title (str, optional): 수정할 제목. Defaults to None.
        content (str, optional): 수정할 내용. Defaults to None.
        hashtags (str, optional): 수정할 해시태그. Defaults to None.

    Returns:
        PostModel: 수정된 게시글 오브젝트
    """
    
    if not(title or content or hashtags):
        return  post_obj

    if title or content:
        data = {}
        if title:
            data["title"] = title

        if content:
            data["content"] = content

        serializer = PostModelSerializer(post_obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    if not hashtags:
        return post_obj

    hashtag_words = parsing_hashtags(hashtags)
    new_hashtag_objs = [get_hashtag(word) for word in hashtag_words]

    old_hashtag_objs = HashtagModel.objects.filter(post=post_obj)

    for old_hashtag_obj in old_hashtag_objs:
        if old_hashtag_obj in new_hashtag_objs:  
            continue
        old_hashtag_obj.delete()

    for new_hashtag_obj in new_hashtag_objs:
        if new_hashtag_obj in old_hashtag_objs:
            continue
        PostHashtagModel.objects.get_or_create(hashtag=new_hashtag_obj, post=post_obj)
    
    return post_obj


def delete_post(post_obj):
    """게시글 삭제(비활성화) 함수

    Args:
        post_obj (PostModel): 게시글 오브젝트
    """

    post_obj.is_active = False
    post_obj.save(update_fields=["is_active"])


def get_post_info(post_obj, viewer):
    """게시글 정보 반환 함수

    Args:
        post_obj (PostModel): 게시글 오브젝트
        viewer (UserModel): 조회한 유저 오브젝트

    Returns:
        dict: 게시글 정보
    """

    return PostModelSerializer(post_obj, context={"viewer": viewer}).data


def increase_views(post_obj):
    """게시글 조회수 증가 함수

    Args:
        post_obj (PostModel): 게시글 오브젝트
    """

    post_obj.views += 1
    post_obj.save(update_fields=["views"])


def recover_post(post_obj):
    """게시글 복구 함수

    Args:
        post_obj (PostModel): 게시글 오브젝트
    """

    post_obj.is_active = True
    post_obj.save(update_fields=["is_active"])


def like_post_event(post_obj, user_obj):
    """좋아요 등록/취소 함수

    Args:
        post_obj (PostModel): 게시글 오브젝트
        user_obj (UserModel): 좋아요 등록/취소한 유저 오브젝트

    Returns:
        bool: 좋아요 등록 - True / 좋아요 취소 - False
    """

    like_obj, created = LikeModel.objects.get_or_create(post=post_obj, user=user_obj)

    if not created:
        like_obj.delete()
        return False

    return True


def get_post_list_deactive(user_obj):
    """삭제(비활성화)된 게시글 정보 리스트 조회 함수

    Args:
        user_obj (UserModel): 조회한 유저 오브젝트

    Returns:
        dict: 삭제(비활성화)된 게시글 정보 리스트
    """

    post_obj_list_deactive = PostModel.objects.filter(user=user_obj, is_active=False)
    return PostModelListSerializer(post_obj_list_deactive, many=True).data


def get_post_list(orderby="created_date", reverse=0, search=None, hashtags=None, page=1, page_size=10):
    """게시글 목록 조회 함수

    Args:
        orderby (str, optional): 정렬 기준. Defaults to "created_date".
        reverse (int, optional):  1 - 오름차순,  0 - 내림차순. Defaults to 0.
        search (str, optional): 검색단어. Defaults to None.
        hashtags (str, optional): 해시태그 문자열 ex) '게임,코딩'. Defaults to None.
        page (int, optional): 페이지. Defaults to 1.
        page_size (int, optional): 1페이당 게시글 개수. Defaults to 10.

    Returns:
        list: 게시글 정보 리스트
    """

    # 검색단어
    query = Q()
    if search:
        query = query & (Q(title__contains=search) | Q(content__contains=search))

    post_obj_list = PostModel.objects.filter(query).all()
    
    # 해시태그
    if hashtags:
        hashtag_words = hashtags.split(",")
        hashtag_obj_list = [ get_hashtag(word) for word in hashtag_words ]

        for obj in hashtag_obj_list:
            post_obj_list = post_obj_list.filter(Q(hashtag=obj))

    post_info_list = PostModelListSerializer(post_obj_list, many=True).data

    # 정렬
    post_info_list.sort(key=choices_sort_func(orderby), reverse=reverse)
    
    # 페이징 
    page -= 1
    start_idx = page * page_size
    end_idx = start_idx + page_size

    # 페이지가 최대 또는 최소로 넘어갈 경우 1페이지로 반환
    if len(post_info_list) < start_idx or page < 0:
        post_info_list = post_info_list[:page_size]
    else :
        post_info_list = post_info_list[start_idx:end_idx]

    return post_info_list


def choices_sort_func(orderby):
    """정렬 기준 선택 함수

    Args:
        orderby (str): 정렬 기준

    Returns:
        func: 정렬 기준 반환 함수
    """

    if orderby == "like_count":
        return get_post_like_count
    
    if orderby == "views":
        return get_post_views
    
    return get_post_created_date


def get_post_created_date(post_info):
    return post_info['created_date']

def get_post_like_count(post_info):
    return post_info['like_count']

def get_post_views(post_info):
    return post_info['views']
