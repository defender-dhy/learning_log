from django.db import models
from django.contrib.auth.models import User

# Create your models here.
'''让我们创建自己的模型。模型告诉Django如何处理应用程序中存储的数据。
在代码层面，模型就是一个类，就像前面讨论的每个类一样，包含属性和方法。'''

class Topic(models.Model):
    '''用户学习的主题'''
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''返回模型的字符串表示'''
        return self.text


    '''Topic的类继承了Model——Django中一个定义了模型基本功能的
    类。Topic类只有两个属性：text和date_added。

    text是一个CharField——由字符或文本组成的数据,需要存储少量的文本，如名称、标题或城市时，
    可使用CharField。定义CharField属性时，必须告诉Django该在数据库中
    预留多少空间。200个字符对存储大多数主题名来说足够了。

    date_added是一个DateTimeField——记录日期和时间的数据。我们传递了实参
    auto_add_now=True，每当用户创建新主题时，这都让Django将这个属性自动设置成当前日期和时间。

    https://docs.djangoproject.com/en/3.0/ref/models/fields/ (获悉可在模型中使用的各种字段)

    需要告诉Django，默认应使用哪个属性来显示有关主题的信息。Django调用方法
    __str__()来显示模型的简单表示。在这里，我们编写了方法__str__()，它返回存储在属性text
    中的字符串

    首先导入了django.contrib.auth中的模型User，然后在Topic中添加了字段owner，它建
    立到模型User的外键关系。

    '''

class Entry(models.Model):
    '''学习到的有关某个主题的具体知识'''
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        '''返回模型的字符串表示'''
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text

'''
Entry也继承了Django基类Model。第一个属性topic是一个ForeignKey实
例。外键是一个数据库术语，它引用了数据库中的另一条记录；这些代码将每个条目关联
到特定的主题。每个主题创建时，都给它分配了一个键（或ID）。需要在两项数据之间建立联系时，
Django使用与每项信息相关联的键。

属性text，它是一个TextField实例。这种字段不需要长度限制，因为我们
不想限制条目的长度。属性date_added让我们能够按创建顺序呈现条目，并在每个条目旁边放置
时间戳。

在Entry类中嵌套了Meta类。Meta存储用于管理模型的额外信息，在这里，它让
我们能够设置一个特殊属性，让Django在需要时使用Entries来表示多个条目。如果没有这个类，
Django将使用Entrys来表示多个条目。

方法__str__()告诉Django，呈现条目时应显示哪些
信息。由于条目包含的文本可能很长，我们让Django只显示text的前50个字符
'''