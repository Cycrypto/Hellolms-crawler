### SITE ###
MAIN_URL = 'http://eclass.kpu.ac.kr/ilos/main/main_form.acl'
AUTH_CHECK_URL = 'http://eclass.kpu.ac.kr/ilos/co/st_session_room_auth_check.acl'

### SESSION ###
LOGIN_URL = 'https://eclass.kpu.ac.kr/ilos/lo/login.acl'
USER_INFO_URL = 'http://eclass.kpu.ac.kr/ilos/mp/myinfo_form.acl'

USER_INFO = {
    'usr_id': None,
    'usr_pwd': None
}

### LECTURE ###
AUTH_FORM = lambda uid, lc_key: {
            'ud': uid,
            'ky': lc_key
}

HEADER = lambda referer: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'Referer': referer
}

INFORM_URL = 'http://eclass.kpu.ac.kr/ilos/st/course/notice_list.acl'