'''定义learning_logs的url模式'''

from django.conf.urls import url

from . import views

urlpatterns = [
    # 主页
    url(r'^$',views.index, name='index'),

    # 显示所有的主题
    url(r'^topics/$',views.topics, name='topics'),

    # 特定主题的详细页面
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),

    # 用于添加新主题的网页
    url(r'^new_topic/$', views.new_topic, name='new_topic'),

    # 用于添加新条目的页面
    url(r'^new_entry/(?P<topic_id>\d+)/$',views.new_entry ,name='new_entry'),

    # 用于编辑条目的页面
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
]


'''
导入了函数url，因为我们需要使用它来将URL映射到视图
模块views，其中的句点让Python从当前的urls.py模块所在的文件夹中导入视图。
变量urlpatterns是一个列表，包含可在应用程序learning_logs中请求的网页

实际的URL模式是一个对函数url()的调用，这个函数接受三个实参。第一个是一个
正则表达式。Django在urlpatterns中查找与请求的URL字符串匹配的正则表达式，因此正则表达
式定义了Django可查找的模式。第二个实参指定了要调用的视图函数。请求的URL与前述正则表达式匹配时，
Django将调用views.index（这个视图函数将在下一节编写）。第三个实参将这个URL模式的名称
指定为index，让我们能够在代码的其他地方引用它。每当需要提供到这个主页的链接时，我们
都将使用这个名称，而不编写URL。

[正则表达式r'^$'。其中的r让Python将接下来的字符串视为原始字
符串，脱字符（^）让Python查看字符串的开头，而美元符号让Python查看字符串的末尾。总体而言，
这个正则表达式让Python查找开头和末尾之间没有任何东西的URL。Python忽略项目的基础
URL（http://localhost:8000/），因此这个正则表达式与基础URL匹配。其他URL都与这个正则表达
式不匹配。如果请求的URL不与任何URL模式匹配，Django将返回一个错误页面。]
'''
'''
r'^topics/(?P<topic_id>\d+)/$'。r让
Django将这个字符串视为原始字符串，并指出正则表达式包含在引号内。这个表达式的第二部分
（/(?P<topic_id>\d+)/）与包含在两个斜杠内的整数匹配，并将这个整数存储在一个名为topic_id
的实参中。这部分表达式两边的括号捕获URL中的值；?P<topic_id>将匹配的值存储到topic_id
中；而表达式\d+与包含在两个斜杆内的任何数字都匹配，不管这个数字为多少位。
发现URL与这个模式匹配时，Django将调用视图函数topic()，并将存储在topic_id中的值作
为实参传递给它。在这个函数中，我们将使用topic_id的值来获取相应的主题。
'''
''' //添加新条目的页面//这个URL模式与形式为http://localhost:8000/new_entry/id/的URL匹配，
其中id是一个与主题ID匹配的数字。(?P<topic_id>\d+)捕获一个数字值，并将其存储在变量topic_id中。
请求的URL与这个模式匹配时，Django将请求和主题ID发送给函数new_entry()。'''
