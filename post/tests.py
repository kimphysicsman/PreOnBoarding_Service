from django.test import TestCase

from user.models import User as UserModel
from post.models import (
    Post as PostModel,
    Hashtag as HashtagModel,
)
from post.services.post_service import (
    parsing_hashtags,
    check_hashtag,
    create_post,
)

class PostServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        TestCase를 위한 TestDB에 데이터 저장
        """

        user_1 = UserModel.objects.create(
            email="test@email.com",
            username="test",
            password="test"
        )

        post_1 = PostModel.objects.create(
            user=user_1,
            title="title",
            content="content",            
        )


    def test_parsing_hashtags(self):
        """해시태그 파싱 함수 테스트

            Case: #으로 시작하지 않은 단어가 있을 경우
        """

        hashtags = "#게임,#코딩,#일상,테스트"

        hashtag_words = parsing_hashtags(hashtags)

        self.assertEquals(hashtag_words, ["게임", "코딩", "일상"])


    def test_check_hashtag(self):
        """해시태그 체크 함수 테스트

            Case: #으로 시작하는 단어일 경우 / 그렇지 않은 단어일 경우
        """

        word = "#게임"

        self.assertEqual(check_hashtag(word), True)

        word = "게임"

        self.assertEqual(check_hashtag(word), False)


    def test_create_post(self):
        """게시글 생성 함수 테스트

            Case: 정상적으로 생성한 경우
        """

        user_obj = UserModel.objects.get(username="test")
        
        data = {
            "user_obj" : user_obj,
            "title": "title",
            "content": "content",
            "hashtags": "#게임,#코딩"
        }

        post_count_1 = PostModel.objects.all().count() 
        hashtag_count_1 = HashtagModel.objects.all().count()

        new_post_obj = create_post(**data)

        post_count_2 = PostModel.objects.all().count() 
        hashtag_count_2 = HashtagModel.objects.all().count()
        
        self.assertEqual(post_count_1 + 1, post_count_2)
        self.assertEqual(hashtag_count_1 + 2, hashtag_count_2)