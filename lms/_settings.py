### SITE ###
MAIN_URL = r'http://eclass.kpu.ac.kr/ilos/main/main_form.acl'
AUTH_CHECK_URL = r'http://eclass.kpu.ac.kr/ilos/st/course/eclass_room2.acl'
SUBMAIN_URL = r'http://eclass.kpu.ac.kr/ilos/st/course/submain_form.acl'
CURRENT = SUBMAIN_URL

### SESSION ###
LOGIN_URL = r'https://eclass.kpu.ac.kr/ilos/lo/login.acl'
USER_INFO_URL = r'http://eclass.kpu.ac.kr/ilos/mp/myinfo_form.acl'

USER_INFO = {
    'usr_id': None,
    'usr_pwd': None
}

### LECTURE ###
AUTH_FORM = lambda KJKEY: {
             'KJKEY': KJKEY,
             'returnData': "json",
             'returnURI': "/ilos/st/course/submain_form.acl",
             'encoding': "utf-8"
}

HEADER = lambda referer: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'Referer': referer
}

FILE_DOWNLOAD_FORM = lambda ud, ky, seq: {
    'ud': ud,
    'ky': ky,
    'CONTENT_SEQ': seq,
    'pf_st_flag': 2,
    'encoding': 'UTF-8'
}

# About Lecture URL #
INFORM_URL = r'http://eclass.kpu.ac.kr/ilos/st/course/notice_list.acl'
CLASS_URL = r'http://eclass.kpu.ac.kr/ilos/st/course/online_list_form.acl'
PLANNER_URL = r'http://eclass.kpu.ac.kr/ilos/st/course/plan_form.acl'
METERIAL_URL = r'http://eclass.kpu.ac.kr/ilos/st/course/lecture_material_list.acl'
HOMEWORK_URL = r'http://eclass.kpu.ac.kr/ilos/st/course/report_list.acl'
TEAMPJ_URL = r'http://eclass.kpu.ac.kr/ilos/st/course/project_list.acl'

# About Calendar URL #
MAIN_SCHEDULE_URL = r'http://eclass.kpu.ac.kr/ilos/main/main_schedule_view.acl'
INSERT_SCHEDULE_URL = r'http://eclass.kpu.ac.kr/ilos/main/schedule_insert.acl'
DELETE_SCHEDULE_URL = r'http://eclass.kpu.ac.kr/ilos/main/schedule_delete.acl'

#About DB Path
OWN_LOGIN_INFO_DB = r"C:\Users\jh01l\Desktop\Hellolms\__own\LOGIN_INFO.db"