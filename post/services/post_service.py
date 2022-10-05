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
        "user" : user_obj.id,
        "title": title,
        "content": content,
        "views": 0,
        "is_active": True
    }

    serializer = PostModelSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    post_obj = serializer.instance

    hashtag_words = parsing_hashtags(hashtags)
    hashtag_objs = [get_hashtag(word) for word in hashtag_words]

    for obj in hashtag_objs:
        PostHashtagModel.objects.get_or_create(hashtag=obj, post=post_obj)

    return post_obj


def update_post(post_id, title=None, content=None, hashtags=None):
    """게시글 수정 함수

    Args:
        post_id (int): 수정할 게시글 오브젝트 id
        title (str, optional): 수정할 제목. Defaults to None.
        content (str, optional): 수정할 내용. Defaults to None.
        hashtags (str, optional): 수정할 해시태그. Defaults to None.

    Returns:
        PostModel: 수정된 게시글 오브젝트
    """
    
    
    post_obj = PostModel.objects.get(id=post_id)

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