from app.settings import JIRA_DOMAINNAME

jira_auth_link = f'{JIRA_DOMAINNAME}/secure/ViewProfile.jspa?' \
                 f'selectedTab=com.atlassian.pats.pats-plugin:jira-user-personal-access-tokens'
jira_auth = f'Необходимо перейти по ' \
            f'<a href="{jira_auth_link}">ссылке</a>, ' \
            f'создать токен доступа (без ограничения по времени) и прислать ответом на сообщение'
