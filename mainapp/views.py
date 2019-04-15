import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
# from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, PostPhoto, Tag, Category, Document, Article, Message, Contact
from .models import Registry, Menu
from .models import Staff
from .forms import PostForm, ArticleForm, DocumentForm
from .forms import SendMessageForm, SubscribeForm, AskQuestionForm, SearchRegistryForm
from .adapters import MessageModelAdapter
from .message_tracker import MessageTracker
from .utilites import UrlMaker
from .registry_import import Importer, data_url

# Create your views here.

def index(request):
    #TODO:  сделать когда-нибудь вывод форм на глваную
    title = 'НАКС Уфа'
    """this is mainpage view with forms handler and adapter to messages"""
    # tracker = MessageTracker()
    if request.method == 'POST':
        request_to_dict = dict(zip(request.POST.keys(), request.POST.values()))
        form_select = {
            'send_message_button': SendMessageForm,
            'subscribe_button': SubscribeForm,
            'ask_question': AskQuestionForm,
        }
        for key in form_select.keys():
            if key in request_to_dict:
                print('got you!', key)
                form_class = form_select[key]
        form = form_class(request_to_dict)
        if form.is_valid():

            # saving form data to messages (need to be cleaned in future)
            adapted_data = MessageModelAdapter(request_to_dict)
            adapted_data.save_to_message()
            print('adapted data saved to database')
            tracker.check_messages()
            tracker.notify_observers()
        else:
            raise ValidationError('form not valid')

    # docs = Document.objects.filter(
    #     publish_on_main_page=True).order_by('-created_date')[:3]

    # main_page_news = Post.objects.filter(
    #     publish_on_main_page=True).order_by('-published_date')[:7]

    #Посты с картинками
    # posts = {}
    # for post in main_page_news:
    #     posts[post] = PostPhoto.objects.filter(post__pk=post.pk).first()

    #Вывести ВСЕ объекты из БД
    # posts = Post.objects.all()[:3]
    posts = Post.objects.filter(publish_on_main_page=True).order_by('-published_date')[:5]
    publications = []
    for post in posts:
        try:
            publications.append({'post': post, 'photo': PostPhoto.objects.get(post=post).image.url })
        except PostPhoto.DoesNotExist:
            publications.append({'post': post, 'photo': 'https://place-hold.it/1200x700'})
    print('PUBLICACTIONS', publications)
    # main_page_articles = Article.objects.filter(
    #     publish_on_main_page=True).order_by('-published_date')[:3]

    # print(request.resolver_match)
    # print(request.resolver_match.url_name)

    content = {
        'title': title,
        'publications': publications
        # 'docs': docs,
        # 'articles': main_page_articles,
        # 'send_message_form': SendMessageForm(),
        # 'subscribe_form': SubscribeForm(),
        # 'ask_question_form': AskQuestionForm()
    }

    return render(request, 'mainapp/index.html', content)

def reestr(request):
    title = 'Реестр'

    content = {
        'title': title
    }
    return render(request, 'mainapp/reestr.html', content)

def doc(request):
    documents= Document.objects.all()
    content={
        "title": "doc",
        "documents": documents
    }
    return render(request, 'mainapp/doc.html', content)
def news(request):
    return render(request, 'mainapp/news.html')
def ocenka_details(request):
    return render(request, 'mainapp/ocenka_details.html')
def news_two(request):
    return render(request, 'mainapp/news_two.html')
def center(request):
    return render(request, 'mainapp/center.html')
def profstandarti(request):
    return render(request, 'mainapp/profstandarti.html')
def all_news(request):
    content = {
        'title': 'All news',
        'news': Post.objects.all().order_by('-published_date')[:9]
    }
    return render(request, 'mainapp/all_news.html', content)
def political(request):
    return render(request, 'mainapp/political.html')

def details(request, content=None, pk=None):

    return_link = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    if request.GET:
        content = request.GET.get('content_type')
        pk = request.GET.get('pk')

    content_select = {
        'post': Post,
        'article': Article
    }
    obj = get_object_or_404(content_select[content], pk=pk)
    print(obj)
    common_content = {'title': obj.title}
    if content == 'post':
        attached_images = PostPhoto.objects.filter(post__pk=pk)
        attached_documents = Document.objects.filter(post__pk=pk)
        post_content = {
            'post': obj,
            'images': attached_images,
            'documents': attached_documents,
            'bottom_related_news': Post.objects.filter(publish_on_main_page=False).exclude(pk=pk).order_by('published_date')[:4]
        }
    if content == 'article':
        tags_pk_list = [tag.pk for tag in obj.tags.all()]
        related_articles = Article.objects.filter(
            tags__in=tags_pk_list).exclude(pk=pk).distinct()
        post_content = {
            'post': obj,
            'related': related_articles,
            #Следуюая строка - это вывод новостей в нижную часть страницы
            'bottom_related_news': related_articles.order_by('-created_date')[:4]
        }

    context = common_content.copy()
    context.update(post_content)
    context['return_link'] = return_link

    print('CONTEXT:', context)

    print(request.resolver_match)
    print(request.resolver_match.url_name)

    return render(request, 'mainapp/page_details.html', context)