import json

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
# from django.contrib import messages
from django.utils import timezone

from .adapters import MessageModelAdapter
from .forms import (ArticleForm, AskQuestionForm, DocumentForm, OrderForm,
                    PostForm, SearchRegistryForm, SendMessageForm,
                    SubscribeForm)
from .message_tracker import MessageTracker
from .models import *
from .registry_import import Importer, data_url
from .utilites import UrlMaker

# Create your views here.


def accept_order(request):
    if request.method == "POST":
        # print('REQUEST POST', request.POST)
        data = {
            "name": request.POST.get("name"),
            "phone": request.POST.get("phone"),
            "captcha_1": request.POST.get("captcha_1"),
            "captcha_0": request.POST.get("captcha_0"),
        }
        order_variants = ["attst", "attso", "attsvsp", "attlab", "attsm", "ocenka"]
        if any([request.POST.get(order_item) for order_item in order_variants]):
            order_compound = {
                "Аттестация технологий": "attst" in request.POST,
                "Аттестация оборудования": "attso" in request.POST,
                "Аттестация персонала": "attso" in request.POST,
                "Аттестация лаборатории": "attlab" in request.POST,
                "Аттестация материалов": "attsm" in request.POST,
                "Оценка квалификации": "ocenka" in request.POST,
            }
            data.update({"compound": "{}".format(order_compound)})
        else:
            order_compound = {"Ничего не заявлено": True}
        form = OrderForm(data)
        if form.is_valid():
            instance = form.save()
            current_absolute_url = request.build_absolute_uri()
            email_address_arr = ["popov.anatoly@gmail.com"]
            order_arr = []

            for key in order_compound.keys():
                if order_compound[key] is True:
                    order_arr.append(key)

            if "8000" not in current_absolute_url:
                if OrderEmail.objects.first() is not None:
                    # admin_email_address = Profile.objects.first().org_order_email.split(" ")
                    admin_email_address = [
                        addr.email for addr in OrderEmail.objects.all()
                    ]
                else:
                    admin_email_address = "popov@naks.ru"
                email_address_arr += admin_email_address
            # 4seconds economy to send_email every time i make tests
            if not instance.name == "tolik_make_tests":
                send_mail(
                    "Заполнена заявка на сайте",
                    """
    Заполнена заявка на сайте {url}
    Имя: {name}, Телефон: {phone},
    Заявлено: {order_string}
    """.format(
                        url=current_absolute_url,
                        name=instance.name,
                        phone=instance.phone,
                        order_string=", ".join(order_arr),
                    ),
                    settings.EMAIL_HOST_USER,
                    email_address_arr,
                )
            return JsonResponse({"message": "ok", "order_id": instance.pk})
        else:
            return JsonResponse({"errors": form.errors})


def pdn_politics(request):
    pdn_page = Post.objects.filter(url_code="pdn-politics").first()
    if not pdn_page:
        pdn_page = {
            "title": "no_pdn_politics",
            "pdn_content": "no_pdn_politics",
        }
    context = {
        "title": "Политика",
        "pdn_page": pdn_page,
    }
    return render(request, "mainapp/pdn_politics.html", context)


def index(request):
    """this is mainpage view with forms handler and adapter to messages"""
    # TODO:  сделать когда-нибудь вывод форм на глваную
    title = Profile.objects.first().org_short_name or "Аттестационный центр"
    form = OrderForm()
    if request.method == "POST":
        """
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
            adapted_data = MessageModelAdapter(request_to_dict)
            adapted_data.save_to_message()
            print('adapted data saved to database')
            tracker.check_messages()
            tracker.notify_observers()
        else:
            raise ValidationError('form not valid')
        """
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save()
            print("new_order", new_order)
        else:
            print("errors->", form.errors)
    certificates = Document.objects.filter(publish_on_main_page=True).order_by(
        "-created_date"
    )[:10]

    # main_page_news = Post.objects.filter(
    #     publish_on_main_page=True).order_by('-published_date')[:7]

    # Посты с картинками
    # posts = {}
    # for post in main_page_news:
    #     posts[post] = PostPhoto.objects.filter(post__pk=post.pk).first()

    # Вывести ВСЕ объекты из БД
    # posts = Post.objects.all()[:3]
    posts = Post.objects.filter(publish_on_main_page=True).order_by("number")[:9]
    publications = []
    for post in posts:
        try:
            publications.append(
                {
                    "post": post,
                    "photo": PostPhoto.objects.filter(post=post).first().image.url,
                }
            )
        except Exception as e:
            publications.append({"post": post, "photo": None})
    print("PUBLICACTIONS", publications)
    # main_page_articles = Article.objects.filter(
    #     publish_on_main_page=True).order_by('-published_date')[:3]

    # print(request.resolver_match)
    # print(request.resolver_match.url_name)

    content = {
        "title": title,
        "publications": publications,
        "form": form,
        "certificates": certificates,
        # 'docs': docs,
        # 'articles': main_page_articles,
        # 'send_message_form': SendMessageForm(),
        # 'subscribe_form': SubscribeForm(),
        # 'ask_question_form': AskQuestionForm()
    }

    return render(request, "mainapp/index.html", content)


def reestr(request):
    title = "Реестр"

    content = {"title": title}
    return render(request, "mainapp/reestr.html", content)


def doc(request):
    documents = Document.objects.all()
    content = {"title": "doc", "documents": documents}
    return render(request, "mainapp/doc.html", content)


def news(request):
    return render(request, "mainapp/news.html")


def ocenka_details(request):
    return render(request, "mainapp/ocenka_details.html")


def news_two(request):
    return render(request, "mainapp/news_two.html")


def center(request):
    return render(request, "mainapp/center.html")


def profstandarti(request):
    from .models import Profstandard

    profstandards = Profstandard.objects.all().order_by("number")
    return render(
        request, "mainapp/profstandarti.html", {"profstandards": profstandards}
    )


def all_news(request):
    content = {
        "title": "All news",
        "news": Post.objects.all().order_by("-published_date")[:9],
    }
    return render(request, "mainapp/all_news.html", content)


def political(request):
    return render(request, "mainapp/political.html")


def details(request, content=None, pk=None):
    return_link = HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

    if request.GET:
        content = request.GET.get("content_type")
        pk = request.GET.get("pk")

    content_select = {"post": Post, "article": Article}
    obj = get_object_or_404(content_select[content], pk=pk)
    print(obj)
    common_content = {"title": obj.title}
    if content == "post":
        attached_images = PostPhoto.objects.filter(post__pk=pk)
        attached_documents = Document.objects.filter(post__pk=pk)
        post_content = {
            "post": obj,
            "images": attached_images,
            "documents": attached_documents,
            "bottom_related_news": Post.objects.filter(publish_on_main_page=False)
            .exclude(pk=pk)
            .order_by("published_date")[:4],
        }
    if content == "article":
        tags_pk_list = [tag.pk for tag in obj.tags.all()]
        related_articles = (
            Article.objects.filter(tags__in=tags_pk_list).exclude(pk=pk).distinct()
        )
        post_content = {
            "post": obj,
            "related": related_articles,
            # Следуюая строка - это вывод новостей в нижную часть страницы
            "bottom_related_news": related_articles.order_by("-created_date")[:4],
        }

    context = common_content.copy()
    context.update(post_content)
    context["return_link"] = return_link

    print("CONTEXT:", context)

    print(request.resolver_match)
    print(request.resolver_match.url_name)

    return render(request, "mainapp/page_details.html", context)
