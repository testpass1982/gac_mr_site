from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.core.files import File
from mainapp.models import Menu, Post, Article, PostPhoto, Tag, Category
from mainapp.models import Contact, Document
from django.conf import settings
from mixer.backend.django import mixer
import random
from django.utils import timezone
# from model_mommy.recipe import Recipe, foreign_key, seq

try:
    popov_user = User.objects.get(username='popov')
except:
    popov_user=User.objects.create(username='popov', email='popov@naks.ru', password='2011')

images = [
    'media/01.JPG',
    'media/02.JPG',
    'media/03.JPG',
    'media/04.JPG',
    'media/05.JPG',
    'media/06.JPG',
]

news_titles = [
    'Конференция НАКС',
    'Общее собрание',
    'Семинар НАКС',
    'Вебинар НАКС',
]

documents = [
    'media/document1.doc',
    'media/document2.doc',
    'media/document3.doc',
    'media/document4.doc',
    'media/document5.doc',
]

menu_urls = [
    'ABOUT_US', 'ASSP', 'ASSV', 'ATTSP', 'ATTST', 'COK', 'CONTACT', 'DOKZAYAV',
    'INFO', 'OBLD', 'OBLDATT', 'PROFST', 'REGISTRY', 'RKNK', 'SPECSVAR', 'VSENOVOSTI', 'ZAYAV', 'SOSTAV_KOMISS'
]
menu_urls_titles = [
    'О центре', 'Аттестация сварщиков и специалистов', 'Аттестация сварщиков', 
    'Аттестация специалистов', 'Аттестация сварочных технологий', 'Центр оценки квалификации',
    'Контакты', 'Документы и заявки', 'Информация для заявителей', 'Область деятельности', 
    'Область аттестации', 'Профессиональные стандарты', 'Реестры', 'Разрушающий и неразрушающий контроль', 
    'Спецподготовка сварщиков', 'Все новости', 'Заявки', 'Состав комиссии',
]

profstandards = [
    {'title': 'Сварщик' , 'ps_code': '40.002', 'reg_number': '14', 'mintrud_reg': 'Приказ Минтруда России № 701н от 28.11.2013 г., зарегистрирован Минюстом России 13.02.2014г., рег. № 31301'},
    {'title': 'Специалист сварочного производства' , 'ps_code': '40.002', 'reg_number': '15', 'mintrud_reg': 'Приказ Минтруда России № 701н от 28.11.2013 г., зарегистрирован Минюстом России 13.02.2014г., рег. № 31301'},
    {'title': 'Контролер сварочных работ', 'ps_code': '40.002', 'reg_number': '16', 'mintrud_reg': 'Приказ Минтруда России № 701н от 28.11.2013 г., зарегистрирован Минюстом России 13.02.2014г., рег. № 31301'},
    {'title': 'Специалист неразрушающего контроля', 'ps_code': '40.002', 'reg_number': '16', 'mintrud_reg': 'Приказ Минтруда России № 701н от 28.11.2013 г., зарегистрирован Минюстом России 13.02.2014г., рег. № 31301'},
    {'title': 'Термист', 'ps_code': '40.002', 'reg_number': '16', 'mintrud_reg': 'Приказ Минтруда России № 701н от 28.11.2013 г., зарегистрирован Минюстом России 13.02.2014г., рег. № 31301'}
]

document_titles = [
    'Постановление Госгортехнадзора России №36 от 25.06.2002г. Об утверждении \
        новой редакции "Технологического регламента проведения аттестации \
            сварщиков и специалистов сварочного производства"',
    'ПБ-03-273-99 "Правила аттестации сварщиков и специалистов \
        сварочного производства',
    'Положение о порядке продления срока действия аттестационных удостоверений \
        сварщиков и специалистов сварочного производства',
    'Перечень групп технических устройств опасных производственных объектов',
    'Инструкция по оформлению заявок на аттестацию заявителей - физических лиц',
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        #delete all Posts, Articles, Menus and other
        Tag.objects.all().delete()
        Category.objects.all().delete()
        Menu.objects.all().delete()
        Post.objects.all().delete()
        Article.objects.all().delete()
        PostPhoto.objects.all().delete()
        Document.objects.all().delete()
        Contact.objects.all().delete()

        #make PostPhotos
        for i in range(0, len(images)):
            #make Tags
            mixer.blend(Tag),
            #make Categories
            mixer.blend(Category),
            #make Posts without pictures
            mixer.blend(Post, title=random.choice(news_titles), published_date=timezone.now())
            mixer.blend(PostPhoto,
                        image=File(open(images[i], 'rb')))
            #make Articles
            mixer.blend(Article, author=popov_user),
            mixer.blend(Contact)
        # for i in range(0, len(profstandards)):
        #     mixer.blend(Profstandard, title=profstandards[i]['title'],
        #                 reg_number=profstandards[i]['reg_number'],
        #                 mintrud_reg=profstandards[i]['mintrud_reg'],
        #                 ps_code=profstandards[i]['ps_code'],
        #                 document=documents[i])

        for i in range(0, len(documents)):
            mixer.blend(Document, document=File(open(documents[i], 'rb')),
                        title=document_titles[i], post=random.choice(Post.objects.all()))

        #make Menus
        for i in range(0, len(menu_urls)):
            mixer.blend(Menu, url_code=menu_urls[i], url=reverse(
                'detailview', kwargs={'content': 'post', 'pk': Post.objects.first().pk}),
                title=menu_urls_titles[i])
        # for i in range(0, len(images)):
        #     PostPhoto.objects.create(
        #         title ='image{}'.format(i),
        #         image=File(open(images[i], 'rb')))
        print('*********fill_db_complete************')