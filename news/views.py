from django.contrib import messages
from django.core.mail import send_mail
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import NewsAddForm, UserRegisterForm, UserLoginForm, EmailForm, Contact
from .models import News, Category

from django.views.decorators.cache import cache_page


@cache_page(60*15)
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('index')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form, 'title': 'Регистрация'})


@cache_page(60*15)
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form, 'title': 'Вход'})


def user_logout(request):
    logout(request)
    return redirect('index')


@cache_page(60*15)
def send_email(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'lotvw13@gmail.com',
                             [form.cleaned_data['to']], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('mail')
            else:
                messages.error(request, 'Ошибка отправки! Попробуйте позже.')
        else:
            messages.error(request, 'Форма неправильно заполнена!')
    else:
        form = EmailForm()

    return render(request, 'news/send_mail.html', {'form': form, 'title': 'Отправка почты'})


@cache_page(60*15)
def contact(request):
    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject'] + ' → ' + form.cleaned_data['from_user']
            mail = send_mail(subject=subject,
                             message=form.cleaned_data['content'],
                             from_email='lotvw13@gmail.com',
                             auth_user='lotvw13@gmail.com',
                             recipient_list=['lotvw13@gmail.com'],
                             fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено! Мы ответим в ближайшее время по электронной почте!')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки! Попробуйте позже.')
        else:
            messages.error(request, 'Форма неправильно заполнена!')
    else:
        form = Contact()

    return render(request, 'news/contact.html', {'form': form, 'title': 'Обратная связь'})


class HomeNews(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список новостей:'
        context['all_news_main'] = self.model.objects.all().count()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category_id')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, id=self.kwargs['category_id'])
        context['all_news_category'] = self.model.objects.filter(category_id=self.kwargs['category_id']).count()
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True) \
            .select_related('category_id')


class ViewNews(DetailView):
    model = News
    pk_url_kwarg = 'news_id'
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)

        queryset = queryset.filter(pk=pk, is_published=True)

        try:
            return queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(("Не могу найти такую %(verbose_name)s") %
                          {'verbose_name': queryset.model._meta.verbose_name})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_news'] = News.objects.order_by('-created_at')[:10]
        return context


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsAddForm
    template_name = 'news/add_news.html'
    raise_exception = True

    # success_url = reverse_lazy('add_news')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_news'] = News.objects.order_by('-created_at')[:10]
        context['title'] = 'Добавление новости'

        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        return super(CreateNews, self).dispatch(request, *args, **kwargs)

        # def index(request):
#     news = News.objects.order_by('-created_at')
#     context = {
#         'news': news,
#         'title': 'Список новостей:',
#     }
#
#     return render(request, 'news/index.html', context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = get_object_or_404(Category, pk=category_id)
#
#     context = {
#         'news': news,
#         'category': category,
#     }
#
#     return render(request, template_name='news/category.html', context=context)


# def view_news(request, news_id):
#     all_news = News.objects.order_by('-created_at')[:10]
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item, 'all_news': all_news})


# def add_news(request):
#     error = ''
#     if request.method == 'POST':
#         form = NewsAddForm(request.POST, request.FILES)
#         if form.is_valid():
#             print('HERE!!!!!!!')
#             news = form.save()
#             return redirect(news)
#         else:
#             error = form.errors
#     else:
#         form = NewsAddForm()
#
#     all_news = News.objects.order_by('-created_at')[:10]
#     context = {'title': 'Добавление новости', 'form': form, 'all_news': all_news, 'error': error}
#     return render(request, 'news/add_news.html', context=context)
