import re

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

from web.models import UserSession

from datetime import datetime


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):

        check_path = ['/web/login/', '/web/register/', '/backweb/login/', '/media/']

        path = request.path
        for check in check_path:
            if re.match(check, path):
                return None

        session = request.COOKIES.get('session')
        usersession = UserSession.objects.filter(session=session).first()
        try:
            out_time = usersession.out_time
        except:
            out_time = 0

        pass_path = ['/web/index/', '/web/goodslist/(\d+)/(\d+)/([0\u4e00-\u9fa5]+)/(\d+)/(\d+)/', '/web/goods/', '/web/upshopping/', '/web/shopping/', '/web/addshopping/', '/web/cutshopping/', '/web/delshopping/', '/web/check/', '/web/total/', '/web/check_all/']
        if not session or not usersession or out_time.strftime("%Y%m%d%H%S%M") < datetime.now().strftime("%Y%m%d%H%S%M"):
            for check in pass_path:
                if re.match(check, path):
                    return None
            if 'backweb' in path:
                return HttpResponseRedirect(reverse('backweb:login'))
            return HttpResponseRedirect(reverse('web:login'))

        request.user = usersession.user