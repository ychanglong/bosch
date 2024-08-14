from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from .models import BlogCategory, Blog
from .forms import PubBlogForms
from django.http.response import JsonResponse


# Create your views here.


def index(request):
    return render(request, 'index.html')


def blog_detail(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    return render(request, 'blog_detail.html', context={'blog': blog})


@login_required(login_url=reverse_lazy('zlauth:login'))
@require_http_methods(['GET', 'POST'])
def public_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'public.html', context={'categories': categories})
    else:
        form = PubBlogForms(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            blog = Blog.objects.create(title=title, category_id=category_id, content=content, author=request.user)
            return JsonResponse({'code': 200, 'message': '博客发布成功', 'data': {'blog_id': blog.id}})
        else:
            print(form.__dict__)
            print(form.errors)
            return JsonResponse({'code': 400, 'message': '参数验证失败'})
