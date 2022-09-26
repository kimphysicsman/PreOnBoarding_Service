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

