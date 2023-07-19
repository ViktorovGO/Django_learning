from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import Musician, Category
from .forms import *
from .utils import *
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator

class MusHome(DataMixin, ListView): 
    model = Musician
    template_name = 'posts/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница") 
        context = dict(list(context.items()) + list(c_def.items())) 
        return context
    
    def get_queryset(self):
        return Musician.objects.filter(is_published = True)
    
# def index(request):
#     posts = Musician.objects.all()
#     context = {
#         'posts': posts,  
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'posts/index.html', context = context)

@login_required
def about(request):
    contact_list = Musician.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get ('page')
    page_obj = paginator.get_page(page_number)
    context = {   
        'title': 'О сайте',
        'cat_selected': 0,
        'menu':menu,
        'page_obj':page_obj
    }
    return render(request, 'posts/about.html', context = context)

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'posts/addpage.html'
    success_url = reverse_lazy('posts:home')
    login_url = reverse_lazy('posts:home')
    # raise_exception = True
    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи') 
        context = dict(list(context.items()) + list(c_def.items()))  
        return context

# def add_page(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data) 
#             form.save()
#             # Musician.objects.create(**form.cleaned_data)
#             return redirect('posts:home')

#     else:    
#         form = AddPostForm() 
    
#     context = {
#         'form':form,
#         'title':'Добавление статьи',
#         'menu':menu
#     }
#     return render(request, 'posts/addpage.html', context = context)


def contact(request):
    return HttpResponse('Контакты')



class ShowPost(DataMixin, DetailView):
    model = Musician
    template_name = 'posts/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'].title, cat_selected = context['post'].cat_id) 
        context = dict(list(context.items()) + list(c_def.items())) 
        return context

# def show_post(request, post_slug):
#     post = get_object_or_404(Musician, slug = post_slug)
#     context ={
#         'post':post,
#         'title':post.title,
#         'cat_selected':post.cat_id
#     } 
#     return render(request, 'posts/post.html', context = context)

class MusCategory(DataMixin, ListView):
    
    model = Musician
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat), cat_selected = Category.objects.get(slug = self.kwargs['cat_slug']).id) 
        context = dict(list(context.items()) + list(c_def.items())) 

        return context

    def get_queryset(self):
        return Musician.objects.filter(cat__slug = self.kwargs['cat_slug'], is_published = True)
        

# def show_category(request, cat_slug):
#     cat_id = Category.objects.get(slug = cat_slug).id
#     posts = Musician.objects.filter(cat_id = cat_id)

#     if len(posts)==0:
#         raise Http404()
#     context = {
#         'posts': posts,  
#         'title': 'Отображение по категориям',
#         'cat_selected': cat_id,
#         'menu':menu,
#     }
#     return render(request, 'posts/index.html', context = context)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def login(request):
    return HttpResponse('Авторизация')

class RegisterUser(DataMixin, CreateView):
   form_class = RegisterUserForm
   template_name = 'posts/register.html'
   success_url = reverse_lazy('posts:login') 
   def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация') 
        context = dict(list(context.items()) + list(c_def.items()))  
        return context