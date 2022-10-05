from post.models import (
    Post as PostModel,
    Hashtag as HashtagModel,
    PostHashtag as PostHashtagModel
)
from post.serializers import PostModelSerializer

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
        viewer (UserModel): 조회 유저 오브젝트

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