from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    '''学习笔记的主页'''
    return render(request,'learning_logs/index.html')

'''向函数render()提供了两个实参：原始请求对象以及一个可用于创建网页的模板'''


@login_required
def topics(request):
    '''显示所有的主题'''
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)

'''导入了函数login_required()。我们将login_required()作为装饰器用于视图函数
topics()——在它前面加上符号@和login_required，让Python在运行topics()的代码前先运行
login_required()的代码。
login_required()的代码检查用户是否已登录，仅当用户已登录时，Django才运行topics()
的代码。如果用户未登录，就重定向到登录页面。

先导入了与所需数据相关联的模型。函数topics()包含一个形参：Django从服
务器那里收到的request对象。首先，我们查询数据库——请求提供Topic对象，并按属
性date_added对它们进行排序。我们将返回的查询集存储在topics中。

context处，我们定义了一个将要发送给模板的上下文。上下文是一个字典，其中的键是我们将
在模板中用来访问数据的名称，而值是我们要发送给模板的数据。在这里，只有一个键—值对，
它包含我们将在网页中显示的一组主题。创建使用数据的网页时，除对象request和模板的路径
外，我们还将变量context传递给render()

用户登录后，request对象将有一个user属性，这个属性存储了有关该用户的信息。代码
Topic.objects.filter(owner=request.user)让Django只从数据库中获取owner属性为当前用户的
Topic对象。由于我们没有修改主题的显示方式，因此无需对页面topics的模板做任何修改。'''


@login_required
def topic(request, topic_id):
    '''显示单个主题及其所有的条目'''
    topic = Topic.objects.get(id = topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

'''这个函数接受正则表达式(?P<topic_id>\d+)捕获的值，并将其存储到topic_id中。
我们使用get()来获取指定的主题，就像前面在Django shell中所做的那样。我们获取与该主题相关联的条目，
并将它们按date_added排序：date_added前面的减号指定按降序排列，即先显示最近的条目。'''


@login_required
def new_topic(request):
    '''添加新主题'''
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form':form}
    return render(request,'learning_logs/new_topic.html', context)

'''导入了HttpResponseRedirect类，用户提交主题后我们将使用这个类将用户重定向到网
页topics。函数reverse()根据指定的URL模型确定URL，这意味着Django将在页面被请求时生成
URL。我们还导入了刚才创建的表单TopicForm。

创建Web应用程序时，将用到的两种主要请求类型是GET请求和POST请求。对于只是从服务
器读取数据的页面，使用GET请求；在用户需要通过表单提交信息时，通常使用POST请求。处理
所有表单时，我们都将指定使用POST方法。

如果请求方法不是POST，请求就可能是GET，
因此我们需要返回一个空表单（即便请求是其他类型的，返回一个空表单也不会有任何问题）。
我们创建一个TopicForm实例，将其存储在变量form中，再通过上下文字典将这个表单发
送给模板。由于实例化TopicForm时我们没有指定任何实参，Django将创建一个可供用户
填写的空表单。

如果请求方法为POST，将执行else代码块，对提交的表单数据进行处理。我们使用用户输
入的数据（它们存储在request.POST中）创建一个TopicForm实例，这样对象form将包含
用户提交的信息。
要将提交的信息保存到数据库，必须先通过检查确定它们是有效的。函数is_valid()
核实用户填写了所有必不可少的字段（表单字段默认都是必不可少的），且输入的数据与要求的
字段类型一致（例如，字段text少于200个字符，这是我们在第18章中的models.py中指定的）。这
种自动验证避免了我们去做大量的工作。如果所有字段都有效，我们就可调用save()，传递实参
commit=False，这是因为我们先修改新主题，再将其保存到数据库中。接下来，将新主题的owner
属性设置为当前用户。最后，对刚定义的主题实例调用save()。现在主题包含所有必不可少的数据，
将被成功地保存。

将表单中的数据写入数据库。保存数据后，就可离开这个页面了。我们使用reverse()获取页面
topics的URL，并将其传递给HttpResponseRedirect()，后者将用户的浏览器重定向到页
面topics。在页面topics中，用户将在主题列表中看到他刚输入的主题。'''


@login_required
def new_entry(request, topic_id):
    '''在特定的主题中添加新条目'''
    topic = Topic.objects.get(id = topic_id)
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)

'''如果是GET请求，将执行if代码块：创建一个空的EntryForm实例。如果请求方法为POST，我们
就对数据进行处理：创建一个EntryForm实例，使用request对象中的POST数据来填充它；再检查表单
是否有效，如果有效，就设置条目对象的属性topic，再将条目对象保存到数据库。

调用save()时，我们传递了实参commit=False，让Django创建一个新的条目对象，并
将其存储到new_entry中，但不将它保存到数据库中。我们将new_entry的属性topic设置为在这个
函数开头从数据库中获取的主题，然后调用save()，且不指定任何实参。这将把条目保
存到数据库，并将其与正确的主题相关联。

我们将用户重定向到显示相关主题的页面。调用reverse()时，需要提供两个实参：
要根据它来生成URL的URL模式的名称；列表args，其中包含要包含在URL中的所有实参。在这
里，列表args只有一个元素——topic_id。接下来，调用HttpResponseRedirect()将用户重定向到
显示新增条目所属主题的页面，用户将在该页面的条目列表中看到新添加的条目。'''


@login_required
def edit_entry(request, entry_id):
    '''编辑既有条目'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # post提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)

'''首先需要导入模型Entry。我们获取用户要修改的条目对象，以及与该条目相
关联的主题。在请求方法为GET时将执行的if代码块中，我们使用实参instance=entry创建一个
EntryForm实例。这个实参让Django创建一个表单，并使用既有条目对象中的信息填充它。
用户将看到既有的数据，并能够编辑它们。

处理POST请求时，我们传递实参instance=entry和data=request.POST，让Django根
据既有条目对象创建一个表单实例，并根据request.POST中的相关数据对其进行修改。
然后，我们检查表单是否有效，如果有效，就调用save()，且不指定任何实参。接下来，
我们重定向到显示条目所属主题的页面，用户将在其中看到其编辑的条目的新版本。'''
