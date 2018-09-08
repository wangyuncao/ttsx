from datetime import datetime, timedelta
from urllib.parse import unquote

from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.db.models import Q, Min
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render


from django.urls import reverse

from utils.functions import random_session, random_order
from web.models import User, UserSession, ClassiFication, Carousel, Static, Goods, Shopping, Order, Order_Goods, Browse, \
    UserSite

type = ['fruit', 'seafood', 'meet', 'egg', 'vegetables', 'ice']


def index(request):
    if request.method == 'GET':
        carousels = Carousel.objects.all().order_by('order')
        statics = Static.objects.all().order_by('order')
        classis = ClassiFication.objects.all()
        for i in range(len(classis)):
            classis[i].classlist = classis[i].childtypenames.split('#')
            classis[i].type = type[i]

        user = request.user
        if user.id:
            count = Shopping.objects.filter(user=user).count()
        else:
            shopping_list = request.session.get('shopping_list', [])
            count = len(shopping_list)

        return render(request, 'web/index.html', {'carousels': carousels, 'statics': statics, 'classis': classis, 'count': count})


def login(request):
    if request.method == "GET":
        try:
            username = request.COOKIES['username']
        except:
            username = ''
        return render(request, 'web/login.html', {'username': username})
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        remember = request.POST.get('remember')

        if not all([username, pwd]):
            return render(request, 'web/login.html', {'error': '输入不能为空'})

        user = User.objects.filter(username=username).first()
        if not user:
            return render(request, 'web/login.html', {'error': '用户不存在'})
        if not check_password(pwd, user.password):
            return render(request, 'web/login.html', {'error': '密码不正确'})

        res = HttpResponseRedirect(reverse('web:index'))
        if remember:
            res.set_cookie('username', username, expires=None)

        shoppings = Shopping.objects.filter(user=user)
        shopping_list = request.session.get('shopping_list', [])
        if len(shopping_list):
            for shopping_single in shopping_list:
                try:
                    flag = 1
                    for shopping in shoppings:
                        if shopping.goods_id == int(shopping_single[0]):
                            shopping.goods_num += int(shopping_single[1])
                            shopping.is_select = int(shopping_single[2])
                            shopping.save()
                            flag = 0
                            break
                    if flag:
                        Shopping.objects.create(user=user, goods_id=shopping_single[0],goods_num=shopping_single[1], is_select=shopping_single[2])
                except:
                    Shopping.objects.create(user=user, goods_id=shopping_single[0],goods_num=shopping_single[1], is_select=shopping_single[2])
            del request.session['shopping_list']

        session = random_session()
        out_time = datetime.now() + timedelta(days=1)
        res.set_cookie('session', session, expires=out_time)
        UserSession.objects.create(user=user,
                                   session=session,
                                   out_time=out_time)

        UserSession.objects.filter(Q(user=user) & ~Q(session=session)).delete()
        return res


def register(request):
    if request.method == 'GET':
        return render(request, 'web/register.html')
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        if not all([user_name, pwd, cpwd, email]):
            return render(request, 'web/register.html', {'error': '输入不能为空'})
        if not allow:
            return render(request, 'web/register.html', {'error': '必须勾选使用协议'})

        judge_user = User.objects.filter(username=user_name).exists()
        if judge_user:
            return render(request, 'web/register.html', {'error': '该用户已被注册'})
        if pwd != cpwd:
            return render(request, 'web/register.html', {'error': '两次输入密码不正确'})

        User.objects.create(username=user_name,
                            password=make_password(pwd),
                            email=email)

        return HttpResponseRedirect(reverse('web:login'))


def goodslist(request, page, class_f, subclass, price_state, popularity_state):
    if request.method == 'GET':
        goods_name = request.GET.get('goods_name', '')

        classis = ClassiFication.objects.all()

        if class_f == '0':
            goodslook = Goods.objects.all()
        else:
            goodslook = Goods.objects.filter(class_f_id=class_f)

        if class_f == '0':
            if goods_name:
                goodall = Goods.objects.filter(goodsname__contains=unquote(goods_name, encoding="GBK"))
            else:
                goodall = Goods.objects.all()
        else:
            if subclass == '0':
                goodall = Goods.objects.filter(class_f_id=class_f)
            else:
                goodall = Goods.objects.filter(class_f_id=class_f, subclass=unquote(subclass, encoding="GBK"))

        alt_price_state = 1
        if popularity_state == '0':
            if price_state == '0':
                alt_price_state = 1
            elif price_state == '1':
                goodall = goodall.order_by('-price')
                alt_price_state = 2
            elif price_state == '2':
                goodall = goodall.order_by('price')
                alt_price_state = 1

        alt_popularity_state = 1
        if price_state == '0':
            if popularity_state == '0':
                alt_popularity_state = 1
            elif popularity_state == '1':
                goodall = goodall.order_by('-popularity')
                alt_popularity_state = 2
            elif popularity_state == '2':
                goodall = goodall.order_by('popularity')
                alt_popularity_state = 1

        paginator = Paginator(goodall, 10)
        goods = paginator.page(page)

        for i in range(len(classis)):
            classis[i].type = type[i]

        user = request.user
        if user.id:
            count = Shopping.objects.filter(user=user).count()
        else:
            shopping_list = request.session.get('shopping_list', [])
            count = len(shopping_list)

        return render(request, 'web/goodslist.html', {'classis': classis,
                                                         'goodslook': goodslook,
                                                         'goodall': goodall,
                                                         'goods': goods,
                                                         'class_f': class_f,
                                                         'subclass': subclass,
                                                         'price_state': price_state,
                                                         'alt_price_state': alt_price_state,
                                                         'popularity_state': popularity_state,
                                                         'alt_popularity_state': alt_popularity_state,
                                                         'count': count})


def goods(request):
    if request.method == 'GET':
        id = request.GET.get('goods_id')
        goods = Goods.objects.get(id=id)
        classis = ClassiFication.objects.all()
        goodslook = goods.class_f.goods_set.all()

        user = request.user
        if user.id:
            count = Shopping.objects.filter(user=user).count()
        else:
            shopping_list = request.session.get('shopping_list', [])
            count = len(shopping_list)

        try:
            Browse.objects.filter(user=user, goods=goods).update(browse_time=datetime.now())
        except:
            pass

        try:
            browse = Browse.objects.filter(user=user)
            if browse.count() == 6:
                b_time = browse.aggregate(b_time=Min('browse_time'))['b_time']
                Browse.objects.filter(user=user, browse_time=b_time).delete()
        except:
            pass

        for i in range(len(classis)):
            classis[i].type = type[i]

        return render(request, 'web/goods.html', {'classis': classis,
                                                    'goods': goods,
                                                    'goodslook': goodslook,
                                                    'count': count})


def upshopping(request):
    if request.method == 'POST':
        user = request.user
        goods_id = int(request.POST.get('goods_id'))
        goods_num = int(request.POST.get('goods_num'))

        if user.id:
            if Shopping.objects.filter(user=user, goods_id=goods_id).exists():
                shopping = Shopping.objects.filter(user=user, goods_id=goods_id)
                shopping.update(goods_num=goods_num + shopping.first().goods_num)
            else:
                Shopping.objects.create(user=user,
                                        goods_id=goods_id,
                                        goods_num=goods_num)

            count = Shopping.objects.filter(user=user).count()
        else:
            goodsid_num = [goods_id, goods_num, 1]
            shopping_list = request.session.get('shopping_list', [])
            flag = 1
            for shopping_single in shopping_list:
                if shopping_single[0] == goods_id:
                    shopping_single[1] = int(shopping_single[1]) + int(goods_num)
                    flag = 0
                    break
            if flag:
                shopping_list.append(goodsid_num)
            request.session['shopping_list'] = shopping_list
            count = len(shopping_list)

        return JsonResponse({'code': 200,
                             'msg': '请求成功',
                             'count': count})


def shopping(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            shoppings = Shopping.objects.filter(user=user)

            if Shopping.objects.filter(user=user, is_select=False).exists():
                state = 0
            else:
                state = 1
            return render(request, 'web/shopping.html', {'shoppings': shoppings,
                                                            'state': state})
        else:
            shopping_list = request.session.get('shopping_list', [])
            shoppings_id = []
            state = 1
            if len(shopping_list):
                for shopping_single in shopping_list:
                    shoppings_id.append(shopping_single[0])
                    if not shopping_single[2]:
                        state = 0
            else:
                state = 0
            goods_list = [Goods.objects.get(id=id) for id in shoppings_id]
            goods = [good for good in goods_list]
            shopping_count = len(shopping_list)
            for i in range(len(shopping_list)):
                goods[i].num = shopping_list[i][1]
                goods[i].state = shopping_list[i][2]
            return render(request, 'web/shopping.html', {'goods': goods,
                                                            'state': state,
                                                            'shopping_count': shopping_count})


def addshopping(request):
    if request.method == 'POST':
        shopping_id = request.POST.get('shopping_id')
        goods_num = 0
        user = request.user
        if user.id:
            shopping = Shopping.objects.get(id=shopping_id)
            shopping.goods_num = shopping.goods_num + 1
            shopping.save()
            goods_num = shopping.goods_num
        else:
            shopping_list = request.session.get('shopping_list', [])
            for goods in shopping_list:
                if goods[0] == int(shopping_id):
                    goods[1] = goods[1] + 1
                    goods_num = goods[1]
                    del request.session['shopping_list']
                    request.session['shopping_list'] = shopping_list
                    break

        return JsonResponse({'code': 200,
                             'msg': '请求成功',
                             'goods_num': goods_num})


def cutshopping(request):
    if request.method == 'POST':
        shopping_id = request.POST.get('shopping_id')
        goods_num = 0
        user = request.user
        if user.id:
            shopping = Shopping.objects.get(id=shopping_id)
            if shopping.goods_num != 1:
                shopping.goods_num = shopping.goods_num - 1
                shopping.save()
                goods_num = shopping.goods_num
            else:
                shopping.delete()

                return JsonResponse({'code': 400,
                                     'msg': '已经删除'})
        else:
            shopping_list = request.session.get('shopping_list', [])
            flag = 1
            for goods in shopping_list:
                if goods[0] == int(shopping_id):
                    goods[1] = goods[1] - 1
                    goods_num = goods[1]

                    if goods_num == 0:
                        shopping_list.remove(goods)
                        flag = 0
                    del request.session['shopping_list']
                    request.session['shopping_list'] = shopping_list
                    break
            if not flag:
                return JsonResponse({'code': 400,
                                     'msg': '已经删除'})
        return JsonResponse({'code': 200,
                             'msg': '请求成功',
                             'goods_num': goods_num})


def delshopping(request):
    if request.method == 'POST':
        shopping_id = request.POST.get('shopping_id')
        if request.user.id:
            Shopping.objects.filter(id=shopping_id).delete()
        else:
            shopping_list = request.session.get('shopping_list', [])
            for goods in shopping_list:
                if goods[0] == int(shopping_id):
                    shopping_list.remove(goods)
                    del request.session['shopping_list']
                    request.session['shopping_list'] = shopping_list

        return JsonResponse({'code': 200,
                             'msg': '请求成功'})


def check(request):
    if request.method == 'POST':
        shopping_id = request.POST.get('shopping_id')
        user = request.user
        if user.id:
            shopping = Shopping.objects.get(id=shopping_id)
            if shopping.is_select:
                shopping.is_select = False
                shopping.save()
            else:
                shopping.is_select = True
                shopping.save()

            if Shopping.objects.filter(user=user, is_select=False).exists():
                state = 0
            else:
                state = 1
        else:
            shopping_list = request.session.get('shopping_list', [])
            state = 1
            for goods in shopping_list:
                if goods[0] == int(shopping_id):
                    if goods[2]:
                        goods[2] = 0
                    else:
                        goods[2] = 1
                    del request.session['shopping_list']
                    request.session['shopping_list'] = shopping_list
                if goods[2] == 0:
                    state = 0

        return JsonResponse({'code': 200,
                             'msg': '请求成功',
                             'state': state})


def total(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            shoppings = Shopping.objects.filter(user=user, is_select=True)
            s = 0
            for shopping in shoppings:
                s += shopping.goods.price * shopping.goods_num

            total = '%.2f' % s
            counts = shoppings.count()

        else:
            shopping_list = request.session.get('shopping_list', [])
            goods_id_list = []
            goods_num_list = []
            counts = 0
            for goods in shopping_list:
                if goods[2] == 1:
                    goods_id_list.append(goods[0])
                    goods_num_list.append(goods[1])
                    counts += 1
            goods_in = [Goods.objects.get(id=goods_id) for goods_id in goods_id_list]
            goods_price = [goods.price for goods in goods_in]
            s = 0
            for i in range(len(goods_num_list)):
                s += goods_num_list[i] * goods_price[i]
            total = '%.2f' % s
        data = {
            'total': total,
            'counts': counts,
        }
        return JsonResponse({'code': 200,
                             'msg': '请求成功',
                             'data': data})


def check_all(request):
    if request.method == 'POST':
        state = request.POST.get('state')
        user = request.user
        if user.id:
            if state == '1':
                Shopping.objects.filter(user=user).update(is_select=False)
            if state == '0':
                Shopping.objects.filter(user=user).update(is_select=True)
        else:
            shopping_list = request.session.get('shopping_list', [])
            for goods in shopping_list:
                if state == '1':
                    goods[2] = 0
                if state == '0':
                    goods[2] = 1
            del request.session['shopping_list']
            request.session['shopping_list'] = shopping_list

        return JsonResponse({'code': 200,
                             'msg': '请求成功'})


def dispose_order(request):
    if request.method == 'GET':
        user = request.user
        shoppings = Shopping.objects.filter(user=user, is_select=True)
        order_number = random_order() + datetime.now().strftime("%Y%m%d%H%S%M")
        Order.objects.create(order_number=order_number, user=user)
        order = Order.objects.get(order_number=order_number)
        for shopping in shoppings:
            Order_Goods.objects.create(goods=shopping.goods,
                                       order=order,
                                       goods_num=shopping.goods_num)
        shoppings.delete()

        return JsonResponse({'code': 200,
                             'msg': '请求成功',
                             'order_number': order_number})


def order(request):
    if request.method == 'GET':
        order_number = request.GET.get('order_number')
        order = Order.objects.get(order_number=order_number)
        user = request.user
        usersites = UserSite.objects.filter(user=user)
        for usersite in usersites:
            mobile = usersite.mobile
            usersite.secrecy = mobile[0:3] + '*****' + mobile[7:11]

        return render(request, 'web/order.html', {'order': order, 'usersites': usersites})


def uporder(request):
    if request.method == 'POST':
        usersite_id = request.POST.get('usersite_id')
        order_id = request.POST.get('order_id')
        pattern_id = request.POST.get('pattern_id')
        order = Order.objects.filter(id=order_id)
        if not usersite_id:
            return JsonResponse({'code': 400,
                                 'msg': '请求失败'})

        order.update(status=1, pattern_id=pattern_id, usersite_id=usersite_id)

        for order_good in order.first().order_goods_set.all():
            order_good.goods.popularity = order_good.goods.popularity + order_good.goods_num
            order_good.goods.save()

        return JsonResponse({'code': 200,
                             'msg': '请求成功'})


def user_center_info(request):
    if request.method == 'GET':
        user = request.user
        browses = Browse.objects.filter(user=user).order_by('-browse_time')
        return render(request, 'web/user_center_info.html', {'browses': browses})


def user_center_order(request):
    if request.method == 'GET':
        user = request.user
        orders_all = Order.objects.filter(Q(user=user) & (Q(status=0) | Q(status=1)))

        page_num = int(request.GET.get('page', 1))
        paginator = Paginator(orders_all, 2)
        orders = paginator.page(page_num)
        return render(request, 'web/user_center_order.html', {'orders': orders})


def user_center_site(request):
    if request.method == 'GET':
        return render(request, 'web/user_center_site.html')
    if request.method == 'POST':
        user = request.user
        usersite_id = request.POST.get('usersite_id')
        addressee = request.POST.get('addressee')
        site = request.POST.get('site')
        postcode = request.POST.get('postcode')
        mobile = request.POST.get('mobile')

        UserSite.objects.all().update(default_site=False)

        if not usersite_id:
            UserSite.objects.create(user=user, addressee=addressee, site=site, postcode=postcode, mobile=mobile)
        else:
            UserSite.objects.filter(id=usersite_id).update(user=user, addressee=addressee, site=site, postcode=postcode, mobile=mobile, default_site=True)
        return JsonResponse({'code': 200,
                             'msg': '请求成功'})


def show_site(request):
    if request.method == 'GET':
        user = request.user
        usersites = UserSite.objects.filter(user=user)
        for usersite in usersites:
            mobile = usersite.mobile
            usersite.secrecy = mobile[0:3] + '*****' + mobile[7:11]
        usersites_list = []
        for usersite in usersites:
            usersites_dict = usersite.__dict__
            usersites_dict.pop('_state')
            usersites_list.append(usersites_dict)
        data = {
            'usersites': usersites_list,
        }
        return JsonResponse({'code': 200,
                             'msg': '请求成功',
                             'data': data})


def check_address(request):
    if request.method == 'POST':
        usersite_id = request.POST.get('usersite_id')
        usersite = UserSite.objects.get(id=usersite_id)
        data = {
            'addressee': usersite.addressee,
            'site': usersite.site,
            'postcode': usersite.postcode,
            'mobile': usersite.mobile
        }
        return JsonResponse({'code': 200,
                             'msg': '请求成功',
                             'data': data})


def del_site(request):
    if request.method == 'POST':
        user = request.user
        usersite_id = request.POST.get('usersite_id')
        UserSite.objects.filter(id=usersite_id).delete()

        if not UserSite.objects.filter(user=user, default_site=True).exists():
            usersite = UserSite.objects.filter(user=user).first()
            usersite.default_site = True
            usersite.save()
        return JsonResponse({'code': 200,
                             'msg': '请求成功'})


def logout(request):
    if request.method == 'GET':
        user = request.user
        UserSession.objects.filter(user=user).delete()

        res = HttpResponseRedirect(reverse('web:index'))
        res.delete_cookie('session')
        return res