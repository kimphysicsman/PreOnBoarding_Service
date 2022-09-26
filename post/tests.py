from django.test import TestCase

from post.services.post_service import (
    parsing_hashtags,
    check_hashtag
)

class PostServiceTest(TestCase):
    

    def test_parsing_hashtags(self):
        """해시태그 파싱 함수 테스트

            Case: #으로 시작하지 않은 단어가 있을 경우
        """

        hashtags = "#게임,#코딩,#일상,테스트"

        hashtag_words = parsing_hashtags(hashtags)

        print(hashtag_words)

        self.assertEquals(hashtag_words, ["게임", "코딩", "일상"])


    def test_check_hashtag(self):
        """해시태그 체크 함수 테스트

            Case: #으로 시작하는 단어일 경우 / 그렇지 않은 단어일 경우
        """

        word = "#게임"

        self.assertEqual(check_hashtag(word), True)

        word = "게임"

        self.assertEqual(check_hashtag(word), False)
