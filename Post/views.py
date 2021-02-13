from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import ListView, DetailView, CreateView
from django.core.mail import send_mail

from .models import Post, Category, Comments
from .forms import UserLoginForm, UserRegisterForm, PostForm, ContactForm, CommentForm


class Posts(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'Post/main.html'
    paginate_by = 5

    # Это вместо get_queryset + меньше SQL
    queryset = Post.objects.select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи обо всем'

        return context


class PostsByCategory(ListView):
    model = Category
    template_name = 'Post/main.html'
    context_object_name = 'posts'
    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        # select_related используется для уменьшение SQL запросов
        return Post.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ShowPost(DetailView):
    model = Post
    template_name = 'Post/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comments.objects.filter(
            post_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comments(content=request.POST.get('content'),
                                  author=self.request.user,
                                  post_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'Post/add_post.html'
    context_object_name = 'form'
    # success_url = reverse_lazy('home')
    login_url = '/admin/'


def contactMail(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                'mr.muhajan@inbox.ru',
                ['petker_kz@mail.ru'],
                fail_silently=True
            )
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('home')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Отправка не удалась')
    else:
        form = ContactForm()
    return render(request, 'Post/contact.html', {'form': form})



def userLogin(request):
    if request.method == 'POST':
        form_login = UserLoginForm(data=request.POST)
        if form_login.is_valid():
            user = form_login.get_user()
            login(request, user)
            messages.success(request, 'Вы вошли в систему')
            return redirect('home')
    else:
        form_login = UserLoginForm()
    return render(request, 'Post/login.html', {'form': form_login})

def user_logout(request):
    logout(request)
    messages.error(request, 'Вы вышли из системы')
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка в регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'Post/register.html', {'form': form})

