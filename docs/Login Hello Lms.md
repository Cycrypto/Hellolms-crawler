# 로그인 하는 방법
```python
import lms.session as session
login = session.GetSession()    #세션이 생성됨
```
로그인이 완료되었는지 확인할 방법이 없어서 `status_code`로만 구분되게 되었습니다.  
따라서, 정확한 확인을 위해선, `user info` 확인을 추가적으로 할 수도 있습니다.  
<br>
```python
import lms.session as session
session.GetUserInfo(login.session).getInfo()
```
출력값으로 이름, 이메일등이 출력됩니다.  
로그인에 실패한경우 실패 메시지가 출력됩니다.