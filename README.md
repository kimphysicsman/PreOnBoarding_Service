# PreOnBoarding_Service
게시글 작성 및 조회 서비스

<br /><br />

> ## **🧾 요구 사항**
- 참여기업 : **원티드**
- 기업과제 : **프리온보딩 과제**
	- SNS(Social Networking Service) 구현

<br /><br />

> ## 🔑 MVP
사용자는 본 서비스에 접속하여, 게시물을 업로드 하거나 다른 사람의 게시물을 확인하고, 좋아요를 누를 수 있다.

<br /><br />

> ## 💻 기술 스택
`Python` `Django` `DRF`

<br /><br />

> ## 💡 핵심 구현

> ### 1. service / view layer 분리

- `view` : 요청 및 응답 데이터 처리  

  - [대표코드 보기 (게시글 생성 - view)](https://github.com/kimphysicsman/PreOnBoarding_Service/blob/0178315dfe9786095dd59317ec9f263c1f4a24d0/post/views.py#L26)
 
- `service` : 기능별 함수 구현

  - [대표코드 보기 (게시글 생성 - service)](https://github.com/kimphysicsman/PreOnBoarding_Service/blob/0178315dfe9786095dd59317ec9f263c1f4a24d0/post/services/post_service.py#L61)  

<br />

> ### 2. 테스트 코드 작성

`django.test.TestCase`를 이용한 service 함수별 테스트 코드 작성   

[대표코드 보기 (게시글 생성 - test)](https://github.com/kimphysicsman/PreOnBoarding_Service/blob/0178315dfe9786095dd59317ec9f263c1f4a24d0/post/tests.py#L77)

<br />

> ### 3. 게시글 목록 조회 필터링 구현

- `view` : 쿼리파라미터를 이용한 필터 데이터 처리

  - [대표 코드보기 (게시글 목록 조회 - view)](https://github.com/kimphysicsman/PreOnBoarding_Service/blob/0178315dfe9786095dd59317ec9f263c1f4a24d0/post/views.py#L126)
 
- `service` : `Q 객체`를 통한 쿼리 표현

  - [대표 코드보기 (게시글 목록 조회 - service)](https://github.com/kimphysicsman/PreOnBoarding_Service/blob/0178315dfe9786095dd59317ec9f263c1f4a24d0/post/services/post_service.py#L258)


<br /><br />

> ## 📖 과제 해석

> #### 1. 유저
`유저`는 이메일을 ID로 사용하며 JWT 토큰을 통해 사용자 인증을 할 수 있다.
- `유저` 정보
    - 이메일
    - 유저이름
    - 패스워드
- 주요 기능
    - 회원가입
    - 로그인

> #### 2. 게시글
`게시글` 은 모든 사용자가 조회할 수 있지만 생성/수정/삭제/복구는 로그인한 사용자만 가능하다.
- `게시글` 정보
    - `유저` - FK
    - 제목
    - 내용
    - 해시태그
    - 작성일
    - 수정일
    - 활성화 여부
    - 조회수
- 주요 기능
    - 게시글 목록 조회
    - 게시글 상세 조회
    - 게시글 생성
    - 게시글 수정
    - 게시글 삭제
    - 게시글 복구

> #### 3. 좋아요
`유저`는 `게시글`을 `좋아요` 등록 또는 취소할 수 있다.
- `좋아요` 정보
    - `유저` - FK
    - `게시글` - FK
- 주요기능
    - 게시글 좋아요 등록/취소

<br /><br />

> ## 🔍 고려항목

> ### 1. 유저 - 이메일과 유저이름
요구사항에는 이메일을 ID로 사용해야한다고만 나와있지만 게시글 조회 기능에서 작성자 정보를 나타낼 때 사용할 유저이름을 필드로 포함한다.
Instagram처럼 로그인은 이메일로하지만 서비스 이용에는 개인정보로 노출되지않도록하고 유저이름을 사용할 수 있다.

<br />

> ### 2. 게시글 목록 조회 - 쿼리파라미터
게시글 목록 조회시 쿼리파라미터를 사용하여 각종 옵션을 설정할 수 있다.
`orderby` : 정렬할 기준 - 작성일(default)/조회수/좋아요수
`reverse` : 정렬시 오름차순, 내림차순(default) 여부 
`search` : 검색할 단어 - 검색단어가 포함된 모든 게시글
`hashtags` : 검색할 해시태그 - 해당 해시태그를 포함한 게시글
`page` : 현재 페이지 위치
`page_size` : 한 페이지당 게시글 수
`is_active` : 게시글 활성화 여부 - 활성화(default)/비활성화 게시글 조회 여부

<br />

> ### 3. 게시글 목록 조회 - 페이지 기능
게시글 목록 조회시 쿼리파라미터로 `page`(현재 페이지 위치)와 `page_size`(한 페이지당 게시글 수)를 받아서 해당되는 게시글 목록만 응답 데이터에 포함한다.
>
ex) 게시글 수 = 100개 / page = 2, page_size = 30 일 경우
⇒ 페이지당 게시글 수는 30개씩이고 2번째 페이지이기 때문에 100개 중에서 30~59번째 게시글 - 총 30개의 게시글을 응답 데이터로 반환   

<br />

> ### 4. 게시글 상세 조회 - 좋아요 여부
게시글 상세 조회시 유저가 해당 게시글의 좋아요를 누른상태인지 아닌지 확인할 수 있도록 `is_liked` 속성에 게시글 좋아요 여부를 응답데이터에 포함시킨다.
>
로그인하지않은 사용자의 요청시 `False` 로 응답한다.

<br />

> ### 5. 게시글 생성 - 해시태그
게시글 생성시 해시태그를 여러개 포함할 수 있으므로 게시글 모델과 ManyToMany 관계를 가지는 해시태그 모델을 생성한다. 

<br />

> ### 6. 게시글 삭제 & 복구
게시글 삭제시 복구될 수 있도록 실제로 DB에서 삭제되지않고 게시글에 `is_active` 라는 필드를 통해 비활성화 시킨다.
>
게시글 복구시 유저는 게시글 목록 조회 기능에서 `is_active` 쿼리파라미터를 통해 삭제된 게시글 목록을 확인할 수 있고 (사용자 인증 필요) 다시 복구할 수 있다.

<br />

> ### 7. 게시글 좋아요 등록/취소
좋아요 등록/취소 기능은 각각 따로 요청되지않고 **좋아요 클릭 이벤트**시 요청되어 유저와 게시글의 정보를 받아
>
- 좋아요를 누른 상태이면 좋아요 취소
- 좋아요를 누르지않은 상태이면 좋아요 등록
>
기능을 수행한다.

<br /><br />

> ## 👉 ERD
![](https://velog.velcdn.com/images/kimphysicsman/post/b8c09c2a-5ae5-46e0-af3c-d05103ab8a50/image.png)

<br /><br />

> ## 🙏 API 명세서
![](https://velog.velcdn.com/images/kimphysicsman/post/8c30a014-886b-41ba-a9c7-e26a28139e42/image.png)

[**상세보기**](https://www.notion.so/kimphysicsman/a9d687f0195f42fc8fa6956fe838397d?v=f09a2d1955a4437a9009cef7d5d84865)

<br /><br />

> ## 📌 컨벤션
### ❓ Commit Message
- feat/ : 새로운 기능 추가/수정/삭제
- enhan/ : 기존 코드에 기능을 추가하거나 기능을 강화할 때
- refac/ : 코드 리팩토링,버그 수정
- test/ : 테스트 코드/기능 추가
- edit/ : 파일을 수정한 경우(파일위치변경, 파일이름 변경, 삭제)

> ### ❓ Naming
- Class : Pascal
- Variable : Snake
- Function : Snake
- Constant : Pascal + Snake

> ### ❓ 주석
- Docstring을 활용하여 클래스와 함수단위에 설명을 적어주도록 하자.
- input/output을 명시하여 문서 없이 코드만으로 어떠한 결과가 나오는지 알 수 있도록 하자.

> ### 🚷 벼락치기의 규칙
- 컨벤션 지키기
- Commit 단위 지키기
- 말 이쁘게하기
- 문제를 마주하여 트러블을 겪었다면, 어떻게 해결을 했는지 공유를 해주기
- 각자의 작업을 미리 작성을 하여서 각자의 작업을 공유하기

<br />

> ## 기획문서
[**노션 - 원티드 프리온보딩**](https://www.notion.so/kimphysicsman/cc95d371cc1548e7ac3594fb10802684)
