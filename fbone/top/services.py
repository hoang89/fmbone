from datetime import datetime
from ..muser.models import MUser, MUserDetail
class TopService(object):
    @classmethod
    def fb_register(cls, data):
        user = MUser.get_by_email(data['email'])
        if not user:
            user = MUser()
            user.email = data['email']
            user.openid = data['id']
            user.username = data['username']
            detail = MUserDetail()
            detail.first_name = data['first_name']
            detail.last_name = data['last_name']
            detail.bio = data['bio']
            detail.birthday = datetime.strptime(data['birthday'],'%m/%d/%Y')
            user.detail = detail
            user.save()
        return user