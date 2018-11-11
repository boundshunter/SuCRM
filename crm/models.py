from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    '''客户表'''
    name = models.CharField(max_length=32, blank=True, null=True)
    qq = models.CharField(max_length=64, unique=True)
    qq_name = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    source_choices = (
        (0, '官网'),
        (1, 'QQ'),
        (2, '微信'),
        (3, '百度推广'),
        (4, '51CTO'),
        (5, '知乎'),
        (6, '市场推广'),
                      )

    source = models.IntegerField(choices=source_choices)
    # 转介绍人信息
    referral_from = models.CharField(max_length=64, verbose_name='介绍人QQ', blank=True, null=True)
    # 咨询的课程
    consult_course = models.ForeignKey("Course", on_delete=True, verbose_name="咨询课程")
    # 咨询详情
    content = models.TextField(verbose_name="咨询详情")
    # 课程顾问，关联到user表
    consultant = models.ForeignKey("UserProfile", on_delete=True)
    # 日期 自增
    date = models.DateTimeField(auto_now_add=True)
    # 备注
    note = models.TextField(blank=True, null=True, verbose_name="备注")
    # 标签
    tag = models.ManyToManyField("Tag")

    def __str__(self):
        return self.qq

    class Meta:
        # 后台显示中文
        verbose_name = "客户表"
        # 去掉后面显示的s
        verbose_name_plural = "客户表"


class Tag(models.Model):
    '''标签,标签和客户是多对多关系'''
    name = models.CharField(unique=True, max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        # 后台显示中文
        # verbose_name = "标签"
        # 去掉后面显示的s
        verbose_name_plural = "标签"


class CustomerFollowUp(models.Model):
    '''客户跟进记录表'''
    customer = models.ForeignKey("Customer", on_delete=True)
    content = models.TextField(verbose_name="跟进内容")
    # 跟进人
    consultant = models.ForeignKey("UserProfile", on_delete=True)
    # 跟进时间
    date = models.DateTimeField(auto_now_add=True)
    # 报名意向
    intension_choices = (
        (0, '2周内报名'),
        (1, '1个月内报名'),
        (2, '近期无报名计划'),
        (3, '已在其他机构报名'),
        (4, '已报名'),
        (5, '已拉黑'),
                         )
    intension = models.IntegerField(choices=intension_choices)

    def __str__(self):
        '''返回跟进的用户qq和意向'''
        return "%s : %s" % (self.customer.qq, self.intension)

    class Meta:
        # 后台显示中文
        verbose_name = "客户跟进记录"
        # 去掉后面显示的s
        verbose_name_plural = "客户跟进记录"


class Course(models.Model):
    '''课程表'''
    name = models.CharField(max_length=64, unique=True)
    # 学费正整数
    price = models.PositiveIntegerField()
    # 周期
    period = models.PositiveIntegerField(verbose_name="周期")

    def __str__(self):
        return self.name

    class Meta:
        # 后台显示中文
        verbose_name = "课程"
        # 去掉后面显示的s
        verbose_name_plural = "课程"


class ClassList(models.Model):
    '''班级表'''
    branch = models.ForeignKey("Branch", verbose_name="分校", on_delete=True)
    course = models.ForeignKey("Course", verbose_name="课程", on_delete=True)
    # 学期
    semester = models.PositiveIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField("UserProfile")
    # 班级类型
    class_type_choices = ((0, "面授(脱产班)"),
                          (1, "面授(周末班)"),
                          (2, "网络班"),
                          )
    class_type = models.IntegerField(choices=class_type_choices, verbose_name="班级类型")
    start_date = models.DateField(verbose_name="开班日期")
    end_date = models.DateField(verbose_name="结业日期", blank=True, null=True)

    def __str__(self):
        return "%s %s %s" % (self.branch, self.course, self.semester)

    class Meta:
        '''校区，课程，学期的联合唯一'''
        unique_together = ('branch', 'course', 'semester')
        # 后台显示中文
        verbose_name = "班级"
        # 去掉后面显示的s
        verbose_name_plural = "班级"


class Branch(models.Model):
    '''校区'''
    name = models.CharField(max_length=128, unique=True)
    addr = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        # 后台显示中文
        verbose_name = "校区"
        # 去掉后面显示的s
        verbose_name_plural = "校区"


class CourseRecord(models.Model):
    '''上课记录'''
    from_class = models.ForeignKey("ClassList", verbose_name="来自的班级", on_delete=True)
    day_num = models.PositiveIntegerField(verbose_name="第几节(天)")
    teacher = models.ForeignKey("UserProfile", verbose_name="老师", on_delete=True)
    has_homework = models.BooleanField(default=True, verbose_name="是否有作业(布尔值)")
    homework_title = models.CharField(max_length=128, blank=True, null=True)
    homework_content = models.TextField(blank=True, null=True)
    outline = models.TextField(verbose_name="本节课程大纲")
    date = models.DateField(auto_now_add=True,verbose_name="上课日期")
    # 联合唯一
    class Meta:
        unique_together = ("from_class", "day_num")
        # 后台显示中文
        verbose_name = "上课记录"
        # 去掉后面显示的s
        verbose_name_plural = "上课记录"
    def __str__(self):
        return "%s %s" % (self.from_class, self.day_num)


class StudyRecord(models.Model):
    '''学习记录'''
    student = models.ForeignKey("Enrollment", on_delete=True)
    course_record = models.ForeignKey("CourseRecord", on_delete=True)
    attendence_choices = ((0, "已签到"),
                          (1, "迟到"),
                          (2, "缺勤"),
                          (3, "早退")
                          )
    attendance = models.IntegerField(choices=attendence_choices, default=0)

    score_choices = ((100, "A+"),
                     (90, "A"),
                     (85, "B+"),
                     (80, "B"),
                     (75, "B-"),
                     (70, "C+"),
                     (60, "C"),
                     (40, "C-"),
                     (-50, "D"),
                     (-100, "COPY"),
                     (0, "N/A"),
                     )
    score = models.IntegerField(choices=score_choices, default=0)
    #备注
    memo = models.TextField(blank=True, null=True, verbose_name="备注")
    date = models.DateField(auto_now_add=True)
    # 联合唯一
    class Meta:
        unique_together = ("student", "course_record")
        verbose_name_plural = "学习记录"

    def __str__(self):
        return "%s %s %s" % (self.student, self.course_record, self.score)


class Enrollment(models.Model):
    '''报名表，合同等'''
    customer = models.ForeignKey("Customer", on_delete=True)
    # 报名哪个班级的课程
    enrolled_class = models.ForeignKey("ClassList", verbose_name="所报班级", on_delete=True)
    # 签单的销售
    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问", on_delete=True)
    # 学员同意合同条款，点击同意
    contract_agreed = models.BooleanField(default=False, verbose_name="学员同意条款")
    contract_approved = models.BooleanField(default=False, verbose_name="合同已审核")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.customer, self.enrolled_class)

    class Meta:
        unique_together = ("customer", "enrolled_class")
        verbose_name_plural = "报名表"


class Payment(models.Model):
    '''缴费记录'''
    # 先交钱，在报名，关联报名表
    customer = models.ForeignKey("Customer", on_delete=True)
    course = models.ForeignKey("Course", verbose_name="所报课程", on_delete=True)
    # 定金最少500
    amount = models.PositiveIntegerField(verbose_name="缴费金额", default=500)
    consultant = models.ForeignKey("UserProfile", verbose_name="办理的顾问", on_delete=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.customer, self.amount)

    class Meta:
        verbose_name_plural = "缴费记录"


class UserProfile(models.Model):
    '''账户表'''
    # ForeignKey 和 onetoonefield区别，onetoonefield 关联后，其他的不许关联了
    # 需要关联django自带的表User，继承，无 “”
    user = models.OneToOneField(User, on_delete=True)
    name = models.CharField(max_length=32)
    role = models.ForeignKey("Role", blank=True, null=True, on_delete=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "账号"


class Role(models.Model):
    '''角色表'''
    name = models.CharField(max_length=32, unique=True)
    menus = models.ForeignKey("Menu", blank=True, on_delete=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "角色"


class Menu(models.Model):
    '''菜单表(用作动态菜单调用)'''
    name = models.CharField(max_length=32, unique=True)
    url_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "菜单"