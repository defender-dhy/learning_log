'''表单'''
from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text':'主题'}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text':''}
        widgets = {'text':forms.Textarea(attrs={'cols':80})}



'''首先导入了模块forms以及要使用的模型Topic。我们定义了一个名为TopicForm
的类，它继承了forms.ModelForm。

最简单的ModelForm版本只包含一个内嵌的Meta类，它告诉Django根据哪个模型创建表单，以
及在表单中包含哪些字段。我们根据模型Topic创建一个表单，该表单只包含字段text
。labels处的代码让Django不要为字段text生成标签。'''

'''新类EntryForm继承了forms.ModelForm，它包含的Meta类指出了表单基于的模型以及要在表单
中包含哪些字段。这里也给字段'text'指定了一个空标签。

定义了属性widgets。小部件（widget）是一个HTML表单元素，如单行文本框、
多行文本区域或下拉列表。通过设置属性widgets，可覆盖Django选择的默认小部件。通过让
Django使用forms.Textarea，我们定制了字段'text'的输入小部件，将文本区域的宽度设置为80
列，而不是默认的40列。这给用户提供了足够的空间，可以编写有意义的条目'''