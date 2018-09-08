from datetime import datetime, timedelta

from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from django.urls import reverse

from utils.functions import random_session
from web.models import User, UserSession, ClassiFication, Goods, Carousel, Static, Pattern, Order, Distribution


def login(request):
    if request.method == 'GET':
        return render(request, 'backweb/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not all([username, password]):
            return render(request, 'backweb/login.html', {'error': '输入不能为空'})

        user = User.objects.filter(username=username).first()
        if not user:
            return render(request, 'backweb/login.html', {'error': '用户不存在'})
        if not check_password(password, user.password):
            return render(request, 'backweb/login.html', {'error': '密码不正确'})
        if not user.is_root:
            return render(request, 'backweb/login.html', {'error': '该用户不是管理员'})

        res = HttpResponseRedirect(reverse('backweb:index'))
        session = random_session()
        out_time = datetime.now() + timedelta(days=1)
        res.set_cookie('session', session, expires=out_time)
        UserSession.objects.create(user=user,
                                   session=session,
                                   out_time=out_time)

        UserSession.objects.filter(Q(user=user) & ~Q(session=session)).delete()
        return res


def index(request):
    if request.method == 'GET':
        return render(request, 'backweb/index.html')


def logout(request):
    if request.method == 'GET':
        user = request.user
        UserSession.objects.filter(user=user).delete()

        res = HttpResponseRedirect(reverse('backweb:login'))
        res.delete_cookie('session')
        return res


def addclassify(request):
    if request.method == 'GET':
        return render(request, 'backweb/addclassify.html')
    if request.method == 'POST':
        typename = request.POST.get('typename')
        childtypenames = request.POST.get('childtypenames')
        classimg = request.FILES.get('classimg')

        if not all([typename, childtypenames, classimg]):
            return render(request, 'backweb/addclassify.html', {'error': '输入不能为空'})
        ClassiFication.objects.create(typename=typename,
                                      childtypenames=childtypenames,
                                      classimg=classimg)
        return HttpResponseRedirect(reverse('backweb:addclassify'))


def goods(request):
    if request.method == 'GET':
        page_num = int(request.GET.get('page', 1))
        goods = Goods.objects.all()
        paginator = Paginator(goods, 10)
        goods_page = paginator.page(page_num)

        return render(request, 'backweb/goods.html', {'goods_page': goods_page})


def addgoods(request):
    if request.method == 'GET':
        goods_id = request.GET.get('goods_id', False)
        if goods_id:
            goods = Goods.objects.get(id=goods_id)
        else:
            goods = goods_id
        return render(request, 'backweb/addgoods.html', {'goods': goods})
    if request.method == 'POST':
        id = request.POST.get('id')
        goodsname = request.POST.get('goodsname')
        price = request.POST.get('price')
        norms = request.POST.get('norms')
        classify = request.POST.get('classify')
        subclass = request.POST.get('subclass')
        abstract = request.POST.get('abstract')
        commodity = request.POST.get('commodity')
        is_recommend = request.POST.get('is_recommend')
        is_new = request.POST.get('is_new')
        goodsimg = request.FILES.get('goodsimg')

        try:
            price = float(price)
        except:
            return render(request, 'backweb/addgoods.html', {'error': '填写价格不正确，请输入数字'})

        if not is_recommend:
            is_recommend = False
        else:
            is_recommend = True

        if not is_new:
            is_new = False
        else:
            is_new = True

        if id:
            if not all([goodsname, price, norms, classify, subclass, abstract, commodity]):
                return render(request, 'backweb/addgoods.html', {'error': '填写不完整'})

            class_f_id = ClassiFication.objects.get(typename=classify).id

            Goods.objects.filter(id=id).update(goodsname=goodsname,
                                               price=price,
                                               norms=norms,
                                               classify=classify,
                                               subclass=subclass,
                                               abstract=abstract,
                                               commodity=commodity,
                                               is_recommend=is_recommend,
                                               class_f_id=class_f_id,
                                               is_new=is_new)
            if goodsimg:
                Goods.objects.filter(id=id).update(goodsimg=goodsimg)
            return HttpResponseRedirect(reverse('backweb:goods'))
        else:
            if not all([goodsname, price, norms, classify, subclass, abstract, commodity, goodsimg]):
                return render(request, 'backweb/addgoods.html', {'error': '填写不完整'})

            class_f_id = ClassiFication.objects.get(typename=classify).id

            Goods.objects.create(goodsname=goodsname,
                                 price=price,
                                 norms=norms,
                                 classify=classify,
                                 subclass=subclass,
                                 abstract=abstract,
                                 commodity=commodity,
                                 is_recommend=is_recommend,
                                 goodsimg=goodsimg,
                                 class_f_id=class_f_id,
                                 is_new=is_new)
            return HttpResponseRedirect(reverse('backweb:addgoods'))


def upclassification(request):
    if request.method == 'GET':
        classi = ClassiFication.objects.all()
        data = {
            'classiname': [cla.typename for cla in classi]
        }
        return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})
    if request.method == 'POST':
        classiname = request.POST.get('classi_name')
        classi = ClassiFication.objects.filter(typename=classiname).first()
        data = {
            'child': classi.childtypenames.split('#')
        }
        return JsonResponse({'code': 200, 'msg': '请求成功', 'data': data})


def carousel(request):
    if request.method == 'GET':
        classs = ClassiFication.objects.all()
        return render(request, 'backweb/carousel.html', {'classs': classs})
    if request.method == 'POST':
        classi_id = request.POST.get('classi_id')
        order = request.POST.get('order')
        img = request.FILES.get('img')
        if not all([classi_id, order, img]):
            return render(request, 'backweb/carousel.html', {'error': '填写不能为空'})

        Carousel.objects.create(classi_id=classi_id, img=img, order=order)
        return HttpResponseRedirect(reverse('backweb:carousel'))


def static(request):
    if request.method == 'GET':
        classs = ClassiFication.objects.all()
        return render(request, 'backweb/static.html', {'classs': classs})
    if request.method == 'POST':
        classi_id = request.POST.get('classi_id')
        order = request.POST.get('order')
        img = request.FILES.get('img')
        if not all([classi_id, order, img]):
            return render(request, 'backweb/carousel.html', {'error': '填写不能为空'})

        Static.objects.create(classi_id=classi_id, img=img, order=order)
        return HttpResponseRedirect(reverse('backweb:static'))


def pattern(request):
    if request.method == 'GET':
        return render(request, 'backweb/pattern.html')


def addpattern(request):
    if request.method == 'GET':
        return render(request, 'backweb/addpattern.html')
    if request.method == 'POST':
        pattname = request.POST.get('pattname')
        describe = request.POST.get('describe')
        if not all([pattname, describe]):
            return render(request, 'backweb/addpattern.html', {'error': '填写不能为空'})

        Pattern.objects.create(pattname=pattname, describe=describe)
        return HttpResponseRedirect(reverse('backweb:addpattern'))


def goods_recommend(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        goods = Goods.objects.get(id=goods_id)
        judge = goods.is_recommend
        if judge:
            judge = goods.is_recommend = False
        else:
            judge = goods.is_recommend = True
        goods.save()
        return JsonResponse({'code': 200, 'msg': '请求成功', 'judge': judge})


def goods_new(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        goods = Goods.objects.get(id=goods_id)
        judge = goods.is_new
        if judge:
            judge = goods.is_new = False
        else:
            judge = goods.is_new = True
        goods.save()
        return JsonResponse({'code': 200, 'msg': '请求成功', 'judge': judge})


def goods_del(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        Goods.objects.get(id=goods_id).delete()

        return JsonResponse({'code': 200, 'msg': '请求成功'})


def order(request):
    if request.method == 'GET':
        page_num = int(request.GET.get('page', 1))
        orders_all = Order.objects.filter(status=1)
        # Paginator给对象分一页多少个
        paginator = Paginator(orders_all, 5)
        # .page赋哪一页
        orders = paginator.page(page_num)

        return render(request, 'backweb/order.html', {'orders': orders})


def uporder(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')

        order = Order.objects.get(id=order_id)
        order.status = 2
        order.save()
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def user_show(request):
    if request.method == 'GET':
        page_num = int(request.GET.get('page', 1))
        users_all = User.objects.exclude(id=1)
        # Paginator给对象分一页多少个
        paginator = Paginator(users_all, 2)
        # .page赋哪一页
        users = paginator.page(page_num)

        return render(request, 'backweb/user_show.html', {'users': users})


def is_root(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        user = User.objects.get(id=user_id)
        if user.is_root:
            user.is_root = False
        else:
            user.is_root = True
        user.save()

        return JsonResponse({'code': 200, 'msg': '请求成功', 'is_root': user.is_root, 'user_id': user_id})


def distribution(request):
    if request.method == 'GET':
        return render(request, 'backweb/distribution.html')


def adddistribution(request):
    if request.method == 'GET':
        return render(request, 'backweb/adddistribution.html')
    if request.method == 'POST':
        distname = request.POST.get('distname')
        describe = request.POST.get('describe')
        if not all([distname, describe]):
            return render(request, 'backweb/adddistribution.html', {'error': '填写不能为空'})

        Distribution.objects.create(distname=distname, describe=describe)
        return HttpResponseRedirect(reverse('backweb:adddistribution'))