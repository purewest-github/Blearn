from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.db import IntegrityError, models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView,  DeleteView, View

from blearn_app.models import Content
from .forms import ContentForm

# Create your views here.

def signupfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username,'',password)
            return redirect('login')
        except IntegrityError:
            return render(request,'signup.html', {'error':'このユーザーはすでに登録されています'})
    return render(request, 'signup.html')

def loginfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('create')
        else:
            return  redirect('signup')
    return render(request,'login.html', {})


def logoutfunc(request):
    logout(request)
    return redirect('login')


class ContentCreate(CreateView):
    model = Content
    template_name = 'create.html'
    form_class = ContentForm
    success_url = reverse_lazy('create')

    # 投稿者ユーザーとリクエストユーザーを紐付ける
    
    def form_valid(self, form):            
        data = form.cleaned_data
        title = data['title']
        blur_word = data['blur_word']
        content = data['content']
        # blur_wordにタグをつけてblur変換
        blur_content = content.replace(blur_word, '<label id="blur_word">'+ blur_word +'</label>')
        ctxt = self.get_context_data(blur_content=blur_content, form=form)
        # Contentsテーブルに登録
        n_content = Content(content=content, title=title, new_content=blur_content, blur_word=blur_word,user=self.request.user,category=data['category'])
        n_content.save()
        return redirect('create')
    
   


    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        category_choice = ((1, "network"), (2, "web"), (3, "linux"),(4, "git"))
        kwgs["categories"] = category_choice
        return kwgs
    
class Index(View):
    form_class = ContentForm



class ContentList(LoginRequiredMixin, ListView):
    template_name = 'list.html'
    model = Content
    
    def get_queryset(self):
        return Content.objects.filter(user=self.request.user,category="1")

    
class ContentList2(LoginRequiredMixin, ListView):
    template_name = 'list.html'
    model = Content

    def get_queryset(self):
        return Content.objects.filter(user=self.request.user,category="2")
    
    
class ContentList3(LoginRequiredMixin, ListView):
    template_name = 'list.html'
    model = Content

    def get_queryset(self):
        return Content.objects.filter(user=self.request.user,category="3")
    
    
class ContentList4(LoginRequiredMixin, ListView):
    template_name = 'list.html'
    model = Content

    def get_queryset(self):
        return Content.objects.filter(user=self.request.user,category="4")
    

class ContentDetail(DetailView):
    template_name = 'detail.html'
    model = Content

class ContentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # 投稿削除ページ
    model = Content
    template_name = 'delete.html'
    success_url = reverse_lazy('create')

    def test_func(self, **kwargs):
        # アクセスできるユーザーを制限
        pk = self.kwargs["pk"]
        post = Content.objects.get(pk=pk)
        return (post.user == self.request.user)

       