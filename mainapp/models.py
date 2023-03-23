"""
File: models.py
Email: yourname@email.com
Description: models to site project
"""
import os

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
# using this as a store for weld orgs:
from picklefield.fields import PickledObjectField

# from django_resized import ResizedImageField


# Create your models here.
class Tag(models.Model):

    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Category(models.Model):
    """category model class"""

    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class ContentMixin(models.Model):
    """base class for Post, Article and Documents"""

    number = models.PositiveSmallIntegerField(default=0)
    title = models.CharField("Название", max_length=200)
    url_code = models.CharField(
        "Код ссылки", max_length=30, blank=True, default="НЕ УКАЗАН"
    )

    short_description = models.CharField("Краткое описание", max_length=200, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="Тэги")
    published_date = models.DateTimeField("Дата публикации", blank=True, null=True)
    created_date = models.DateTimeField("Дата создания", default=timezone.now)
    text = RichTextUploadingField(verbose_name="Текст")
    author = models.ForeignKey(
        "auth.User", verbose_name="Автор", on_delete=models.CASCADE
    )
    publish_on_main_page = models.BooleanField(
        verbose_name="Опубликовать на главной", default=False
    )

    class Meta:
        abstract = True


class Post(ContentMixin):
    """child of contentmixin"""

    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.CASCADE
    )
    publish_on_news_page = models.BooleanField(
        verbose_name="Опубликовать в ленте новостей", default=False
    )
    publish_in_basement = models.BooleanField(
        "Опубликовать в подвале на главной", default=False
    )

    class Meta:
        ordering = ["created_date"]
        get_latest_by = ["created_date"]
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"

    def get_absolute_url(self):
        return reverse("detailview", kwargs={"content": "post", "pk": self.pk})

    def publish(self):
        """unused function"""
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Article(ContentMixin):
    """child of ContentMixin"""

    class Meta:
        ordering = ["created_date"]
        get_latest_by = ["created_date"]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def publish(self):
        """unused, left for future"""
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Document(models.Model):
    title = models.CharField("Название", max_length=500)
    url_code = models.CharField(
        "Код ссылки", max_length=30, blank=True, default="НЕ УКАЗАН"
    )
    document = models.FileField(
        verbose_name="Документ",
        upload_to="documents/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf", "docx", "doc", "jpg", "jpeg"],
                message="Неправильный тип файла, используйте\
                                        PDF, DOCX, DOC, JPG, JPEG",
            )
        ],
    )
    preview = models.FileField(
        null=True,
        blank=True,
        upload_to="documents/",
    )
    uploaded_at = models.DateTimeField(verbose_name="Загружен", default=timezone.now)
    tags = models.ManyToManyField(Tag, verbose_name="Тэги", blank=True)
    created_date = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания"
    )
    post = models.ForeignKey(
        Post,
        verbose_name="Страница",
        blank=True,
        default="",
        on_delete=models.SET_NULL,
        null=True,
    )
    publish_on_main_page = models.BooleanField(
        verbose_name="Опубиковать на главной", default=False
    )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.title

    def extension(self):
        name, extension = os.path.splitext(self.document.name)
        return extension


def upload_to(instance, filename):
    """left for future, unused function"""
    filename_base, filename_ext = os.path.splitext(filename)
    return "upload/{post_pk}/{filename}{extension}".format(
        post_pk=instance.pk,
        filename=slugify(filename_base),
        extension=filename_ext.lower(),
    )


def get_image_filename():
    """unused function, left for future"""
    return "image_{}".format(slugify(timezone.now()))


class PostPhoto(models.Model):
    """model to load photos to content page"""

    post = models.ForeignKey(
        Post,
        verbose_name="новость",
        related_name="images",
        on_delete=models.SET_NULL,
        null=True,
    )
    image = models.ImageField("изображение", upload_to="upload/")
    title = models.CharField(
        "название", max_length=64, blank=True, default=get_image_filename
    )
    position = models.PositiveIntegerField("Позиция", default=0)

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фотографии"
        ordering = ["position"]

    def __str__(self):
        return "{} - {}".format(self.post, self.image)


class Message(models.Model):
    """this is the class to use within adapter patter realization"""

    STATUS_LIST = (
        (0, "new"),
        (1, "registered"),
        (2, "added_to_sending_queue"),
        (3, "notify_sent"),
    )
    title = models.CharField("Заголовок", max_length=64, blank=True)
    typeof = models.CharField("Тип сообщения", max_length=64, blank=True)
    params = models.CharField("Параметры сообщения", max_length=512, blank=True)
    sender_email = models.EmailField(
        "Адрес электронной почты", max_length=64, blank=True
    )
    sender_phone = models.CharField("Телефон", max_length=64, blank=True)
    created_date = models.DateTimeField("Дата получения", default=timezone.now)
    status = models.IntegerField("Статус", default=0, choices=STATUS_LIST)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.title

    def set_status(self, status_code):
        # if status_code in STATUS_LIST:
        self.status = status_code


class Contact(models.Model):
    title = models.CharField("Название контакта", max_length=64, blank=False)
    description = models.CharField("Описание", max_length=200, blank=False)
    email = models.EmailField("Адрес электронной почты", max_length=64, blank=False)
    phone = models.CharField("Телефон", max_length=64, blank=False)
    number = models.SmallIntegerField("Порядок вывода на сайт", default=0)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.title


class Staff(models.Model):
    photo = models.ImageField("Фотография", blank=True)
    name = models.CharField("ФИО", max_length=120, blank=False)
    job = models.CharField("Должность", max_length=120, blank=False)
    experience = models.CharField("Опыт работы", max_length=500, blank=True)
    priority = models.SmallIntegerField("Приоритет", default=0)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return "{} - {}".format(self.name, self.job)


class Menu(models.Model):
    """linking main page UI elements with its description"""

    url_code = models.CharField("Код ссылки", max_length=30)
    title = models.CharField("Заголовок ссылки", max_length=60)
    url = models.CharField("Адрес ссылки", max_length=200, default="НЕТ")

    class Meta:
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"

    def __str__(self):
        return self.title


class Registry(models.Model):
    """this is the class to load external registry records"""

    STATUS_LIST = ((0, "new"), (1, "published"))
    title = models.CharField("Название", max_length=64, blank=True)
    org = models.CharField("Организация", max_length=120, blank=True)
    typeof = models.CharField("Тип", max_length=64, blank=True)
    params = models.CharField("Параметры", max_length=999, blank=True)
    created_date = models.DateField("Дата получения", blank=True)
    status = models.IntegerField("Статус", default=0, choices=STATUS_LIST)

    class Meta:
        verbose_name = "Запись реестра"
        verbose_name_plural = "Записи реестра"

    def __str__(self):
        return self.title


class WeldData(models.Model):
    """database agnostic storage for weld-data"""

    title = models.CharField("Название", blank=True, max_length=100)
    uid = models.IntegerField("UID", unique=True, blank=True)
    args = PickledObjectField()

    class Meta:
        abstract = True


class Profstandard(models.Model):
    title = models.CharField("Название профстандарта", max_length=200)
    info = models.CharField("Информация о стандарте(код)", max_length=300)
    reg_number = models.CharField("Регистрационный номер", max_length=20)
    mintrud_prikaz = models.CharField("Приказ минтруда", max_length=100)
    document = models.FileField("Файл", upload_to="upload/")
    number = models.SmallIntegerField("Порядок сортировки")

    class Meta:
        verbose_name = "Профстандарт"
        verbose_name_plural = "Профстандарты"

    def __str__(self):
        return self.title


class Chunk(models.Model):
    """class for making html chunks on pages"""

    title = models.CharField("Название вставки", max_length=64)
    code = models.CharField(
        "Уникальный код вставки", max_length=64, default="КОД_ВСТАВКИ"
    )
    html = RichTextUploadingField("Форматирование вставки")
    details_link = models.URLField("Ссылка на подробнее", null=True, blank=True)

    class Meta:
        verbose_name = "Вставка"
        verbose_name_plural = "Вставки"

    def __str__(self):
        return self.title


class OrderService(models.Model):
    name = models.CharField("Имя контакта", max_length=50)
    phone = models.CharField("Телефон контакта", max_length=50)
    compound = models.CharField(
        "Состав заявки", max_length=300, default=None, blank=True, null=True
    )
    ready = models.BooleanField("Вопрос решен", default=False, blank=True, null=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return self.name


class OrderEmail(models.Model):
    email = models.EmailField("Адрес электронной почты")

    def __str__(self):
        return self.email


class Profile(models.Model):
    """class for templating organization"""

    org_logotype = models.ImageField(
        "Логотип организации", upload_to="upload/", blank=True, null=True, default=None
    )
    org_footer_logotype = models.ImageField(
        "Логотип для футера (необязательно)",
        upload_to="upload/",
        blank=True,
        null=True,
        default=None,
    )
    org_short_name = models.CharField(
        "Краткое название организации",
        max_length=100,
        blank=True,
        null=True,
        default=None,
    )
    org_full_name = models.CharField(
        "Полное название организации",
        max_length=300,
        blank=True,
        null=True,
        default=None,
    )
    org_intro = models.TextField(
        "Текст для главной страницы", blank=True, null=True, default=None
    )
    org_history = models.TextField(
        "История организаици", blank=True, null=True, default=None
    )
    # phone1 for header
    org_main_phone = models.CharField(
        "Главный телефон организации (используется в хедере)",
        max_length=200,
        blank=True,
        null=True,
        default=None,
    )
    org_main_phone_text = models.CharField(
        'Подпись под телефоном в хедере, например "Многоканальный"',
        max_length=200,
        blank=True,
        null=True,
        default=None,
    )
    # phone2 for header
    org_secondary_phone = models.CharField(
        "Второй телефон организации (используется в хедере)",
        max_length=200,
        blank=True,
        null=True,
        default=None,
    )
    org_secondary_phone_text = models.CharField(
        'Подпись под вторым телефоном в хедере, например "Бухгалтерия"',
        max_length=200,
        blank=True,
        null=True,
        default=None,
    )
    org_phones = models.TextField("Телефоны", blank=True, null=True, default=None)
    org_email = models.TextField(
        "Адрес электронной почты", blank=True, null=True, default=None
    )
    org_order_email = models.CharField(
        "Адреса для подключения формы заявки",
        max_length=100,
        blank=True,
        null=True,
        default=None,
    )
    org_header_emails = models.TextField(
        "Адреса электронной почты (для хедера)", blank=True, null=True, default=None
    )
    org_header_phones = models.TextField(
        "Телефоны (для хедера)", blank=True, null=True, default=None
    )
    org_address = models.TextField(
        "Адрес местоположения организации", null=True, blank=True, default=None
    )
    org_address_map_link = models.CharField(
        "Ссылка на карту", blank=True, null=True, default=None, max_length=500
    )
    org_work_time = models.CharField(
        "Время работы организации", null=True, blank=True, default=None, max_length=100
    )
    org_csp_code = models.CharField(
        "шифр ЦСП (необязательно)", max_length=20, null=True, blank=True
    )
    org_csp_reestr_link = models.URLField("Ссылка на реестр ЦСП", blank=True, null=True)
    org_acsp_code = models.CharField(
        "шифр АЦСП (необязательно)", max_length=20, null=True, blank=True
    )
    org_acsp_reestr_link = models.URLField(
        "Ссылка на реестр АЦСП", blank=True, null=True
    )
    org_acsm_code = models.CharField(
        "шифр АЦСМ (необязательно)", max_length=20, null=True, blank=True
    )
    org_acsm_reestr_link = models.URLField(
        "Ссылка на реестр АЦСМ", blank=True, null=True
    )
    org_acso_code = models.CharField(
        "шифр АЦСО (необязательно)", max_length=20, null=True, blank=True
    )
    org_acso_reestr_link = models.URLField(
        "Ссылка на реестр АЦСО", blank=True, null=True
    )
    org_acst_code = models.CharField(
        "шифр АЦСТ (необязательно)", max_length=20, null=True, blank=True
    )
    org_acst_reestr_link = models.URLField(
        "Ссылка на реестр АЦСТ", blank=True, null=True
    )
    org_cok_code = models.CharField(
        "шифр ЦОК (необязательно)", max_length=20, null=True, blank=True
    )
    org_cok_reestr_link = models.URLField("Ссылка на реестр ЦОК", blank=True, null=True)
    add_ap_list = models.BooleanField(
        "Добавить ссылку на список пунктов", default=False
    )
    add_schedule = models.BooleanField(
        "Добавить ссылку на график аттестации", default=False
    )
    counterjs = models.TextField(
        "Код счетчика", blank=True, null=True, default=None, max_length=1500
    )
    counter_ID = models.CharField(
        "ID счетчика Яндекс.Метрики", blank=True, null=True, max_length=20
    )
    counter_js_goal1 = models.CharField(
        "JS код счетчика (1)", max_length=500, null=True, blank=True
    )
    counter_js_goal2 = models.CharField(
        "JS код счетчика (2)", max_length=500, null=True, blank=True
    )
    number = models.SmallIntegerField("Порядок сортировки", null=True, blank=True)

    class Meta:
        verbose_name = "Профиль организации"
        verbose_name_plural = "Профили организации"

    def __str__(self):
        return self.org_short_name


class Phone(models.Model):
    number = models.CharField("Номер телефона", max_length=20)
    title = models.CharField(
        "Название телефона (например, бухгалтерия)",
        max_length=30,
        null=True,
        blank=True,
    )
    sort = models.SmallIntegerField("Сортировка")

    def __str__(self):
        return self.number


class Partner(models.Model):
    title = models.CharField("Название партнера", max_length=60)
    logo = models.ImageField("Логотип партнера", upload_to="upload/")
    number = models.SmallIntegerField("Порядок вывода на сайт")

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"

    def __str__(self):
        return self.title
