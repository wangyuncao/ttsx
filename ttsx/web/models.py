from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)
    is_root = models.BooleanField(default=0)  # 是否管理员

    class Meta:
        db_table = 'user'


class ClassiFication(models.Model):
    classimg = models.ImageField(upload_to='class')  # 分类图片
    typename = models.CharField(max_length=16)  # 商品分类名称
    childtypenames = models.CharField(max_length=200)  # 商品子分类名称

    class Meta:
        db_table = 'classification'


class Goods(models.Model):
    goodsname = models.CharField(max_length=50, unique=True)  # 商品名字
    goodsimg = models.ImageField(upload_to='goods')  # 图片
    price = models.FloatField()  # 价格
    norms = models.CharField(max_length=20)  # 规格
    abstract = models.CharField(max_length=100)  # 简要说明
    commodity = models.TextField()  # 商品详情
    classify = models.CharField(max_length=16)  # 分类名称
    class_f = models.ForeignKey(ClassiFication)
    subclass = models.CharField(max_length=16)  # 子分类名称
    is_recommend = models.BooleanField(default=0)  # 是否推荐
    is_new = models.BooleanField(default=0)  # 是否新品
    popularity = models.IntegerField(default=0)  # 销量

    class Meta:
        db_table = 'goods'


class UserSite(models.Model):
    user = models.ForeignKey(User)  # 用户
    addressee = models.CharField(max_length=20)  # 收件人
    site = models.CharField(max_length=50)  # 详细地址
    postcode = models.CharField(max_length=20)  # 邮政编码
    mobile = models.CharField(max_length=20)  # 手机
    default_site = models.BooleanField(default=True)  # 默认地址

    class Meta:
        db_table = 'usersite'


class Shopping(models.Model):
    user = models.ForeignKey(User)  # 关联用户
    goods = models.ForeignKey(Goods)  # 关联商品
    goods_num = models.IntegerField(default=1)  # 商品个数
    is_select = models.BooleanField(default=True)  # 是否选择商品

    class Meta:
        db_table = 'shopping'


class Pattern(models.Model):
    pattname = models.CharField(max_length=30)  # 支付名字
    pattimg = models.ImageField(null=True, upload_to='pattern')  # 图片
    describe = models.CharField(max_length=1000)  # 简介

    class Meta:
        db_table = 'pattern'


class Distribution(models.Model):
    distname = models.CharField(max_length=30)  # 配送名字
    distimg = models.ImageField(upload_to='dist')  # 图片
    describe = models.CharField(max_length=1000)  # 简介

    class Meta:
        db_table = 'distribution'


class Order(models.Model):
    order_number = models.CharField(max_length=50)  # 订单号
    user = models.ForeignKey(User)  # 关联用户
    # 0 已下单，未付款， 1 已付款, 未发货,  2 已付款，已发货
    status = models.IntegerField(default=0)  # 状态
    pattern = models.ForeignKey(Pattern, null=True)
    distribution = models.ForeignKey(Distribution, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    usersite = models.ForeignKey(UserSite, null=True)

    class Meta:
        db_table = 'order'


class Order_Goods(models.Model):
    goods = models.ForeignKey(Goods)  # 关联的商品
    order = models.ForeignKey(Order)  # 关联的订单
    goods_num = models.IntegerField(default=1)  # 商品的个数

    class Meta:
        db_table = 'order_goods'


class UserSession(models.Model):
    user = models.ForeignKey(User)  # 关联用户
    session = models.CharField(max_length=256)  # Session
    out_time = models.DateTimeField()  # 过期时间

    class Meta:
        db_table = 'usersession'


class Carousel(models.Model):
    img = models.ImageField(upload_to='carousel')  # 图片
    classi = models.ForeignKey(ClassiFication)  # 名称
    order = models.IntegerField(unique=True)  # 播放顺序

    class Meta:
        db_table = 'carousel'


class Static(models.Model):
    img = models.ImageField(upload_to='carousel')  # 图片
    classi = models.ForeignKey(ClassiFication)  # 名称
    order = models.IntegerField(unique=True)  # 播放顺序

    class Meta:
        db_table = 'static'


class Browse(models.Model):
    user = models.ForeignKey(User)  # 用户
    goods = models.OneToOneField(Goods)  # 商品
    browse_time = models.DateTimeField(auto_now_add=True)  # 浏览时间

    class Meta:
        db_table = 'browse'