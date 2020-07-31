from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm 


# Create your views here.

def logout_view(request):
    '''注销用户'''
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))


def register(request):
    '''注册新用户'''
    if request.method != 'POST':
        # 显示注册的空表单
        form = UserCreationForm()
    else:
        # 处理填好的表单
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # 让用户自动登录，再重定向到主页
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form':form}
    return render(request, 'users/register.html', context)



    '''在注册页面首次被请求时，视图函数register()需要显示一个空的注册表单，并在用户提交
填写好的注册表单时对其进行处理。如果注册成功，这个函数还需让用户自动登录。'''

'''如果响应的是POST请求，我们就根据提交的数据创建一个UserCreationForm实例，
并检查这些数据是否有效：就这里而言，是用户名未包含非法字符，输入的两个密码相同，以及
用户没有试图做恶意的事情。

如果提交的数据有效，我们就调用表单的方法save()，将用户名和密码的散列值保存到数据
库中。方法save()返回新创建的用户对象，我们将其存储在new_user中。

保存用户的信息后，我们让用户自动登录，这包含两个步骤。首先，我们调用authenticate()，
并将实参new_user.username和密码传递给它。用户注册时，被要求输入密码两次；由于
表单是有效的，我们知道输入的这两个密码是相同的，因此可以使用其中任何一个。在这里，我
们从表单的POST数据中获取与键'password1'相关联的值。如果用户名和密码无误，方法
authenticate()将返回一个通过了身份验证的用户对象，而我们将其存储在authenticated_user
中。接下来，我们调用函数login()，并将对象request和authenticated_user传递给它，
这将为新用户创建有效的会话。最后，我们将用户重定向到主页，其页眉中显示了一条
个性化的问候语，让用户知道注册成功了。'''