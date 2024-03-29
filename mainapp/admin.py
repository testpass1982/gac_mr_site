from django.contrib import admin
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html

from .models import *

# from .models import WeldData
# from .domain_model import WeldOrg, Welder
# Register your models here.


def get_picture_preview(obj):
    if (
        obj.pk
    ):  # if object has already been saved and has a primary key, show picture preview
        return format_html(
            """<a href="{src}" target="_blank">
        <img src="{src}" alt="{title}" style="max-width: 200px; max-height: 200px;" />
        </a>""".format(
                src=obj.image.url,
                title=obj.title,
            )
        )
    return "(После загрузки фотографии здесь будет ее миниатюра)"


get_picture_preview.allow_tags = True
get_picture_preview.short_description = "Предварительный просмотр:"


def get_url(obj):
    # Надо обязательно изменить на боевом сервере адрес ссылки
    if obj.pk:
        return format_html(
            '<a href="{}" target="_blank">http://127.0.0.0{}</a>'.format(
                obj.get_absolute_url(), obj.get_absolute_url()
            )
        )


get_url.allow_tags = True
get_url.short_description = "Ссылка на страницу"


class PostPhotoInline(admin.StackedInline):
    model = PostPhoto
    extra = 0
    fields = ["id", "get_edit_link", "title", "image", "position", get_picture_preview]
    readonly_fields = ["id", "get_edit_link", get_picture_preview]

    def get_edit_link(self, obj=None):
        if (
            obj.pk
        ):  # if object has already been saved and has a primary key, show link to it
            url = reverse(
                "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.model_name),
                args=[force_text(obj.pk)],
            )
            return format_html(
                """<a href="{url}">{text}</a>""".format(
                    url=url,
                    text="Редактировать %s отдельно" % obj._meta.verbose_name,
                )
            )
        return (
            '(Загрузите фотографию и нажмите "Сохранить и продолжить редактирование")'
        )

    get_edit_link.short_description = "Изменить"
    get_edit_link.allow_tags = True


class DocumentInline(admin.StackedInline):
    model = Document
    extra = 0
    fields = ["id", "title", "document"]
    list_display = ["title", "publish_on_main_page"]


def get_tag_list(obj):
    return [tag.name for tag in obj.tags.all()]


get_tag_list.allowtags = True
get_tag_list.short_description = "Список тэгов"


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", get_tag_list, "publish_on_main_page"]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "publish_on_main_page", "created_date"]


def show_url(obj):
    return '<a href="{}">View on site</a>'.format(obj.get_absolute_url())


show_url.allow_tags = True


def get_center_photo_preview(obj):
    if (
        obj.pk
    ):  # if object has already been saved and has a primary key, show picture preview
        return format_html(
            """<a href="{src}" target="_blank">
        <img src="{src}" alt="{title}" style="max-width: 200px; max-height: 200px;" />
        </a>""".format(
                src=obj.image.thumb.url,
                title=obj.title,
            )
        )
    return "(После загрузки фотографии здесь будет ее миниатюра)"


@admin.register(CenterPhoto)
class CenterPhotoAdmin(admin.ModelAdmin):
    list_display = ["number", "title", get_center_photo_preview]
    list_display_links = ["title", get_center_photo_preview]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # save_on_top = True
    view_on_site = True

    fields = [
        "id",
        "number",
        "title",
        "url_code",
        "tags",
        "category",
        "author",
        "short_description",
        "text",
        get_url,
        "created_date",
        "published_date",
        "publish_on_main_page",
        "publish_on_news_page",
        "publish_in_basement",
    ]
    readonly_fields = ["id", get_url]
    list_display = [
        "number",
        "title",
        "category",
        "created_date",
        "publish_on_main_page",
        "publish_on_news_page",
    ]
    inlines = [PostPhotoInline, DocumentInline]

    def view_on_site(self, obj):
        url = reverse("detailview", kwargs={"content": "post", "pk": obj.pk})
        return "http://127.0.0.1:8000" + url


@admin.register(PostPhoto)
class PostPhotoAdmin(admin.ModelAdmin):
    # save_on_top = True
    fields = ["id", "post", "image", "title", "position", get_picture_preview]
    readonly_fields = ["id", get_picture_preview]
    list_display = ["title", "post", get_picture_preview]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["title", "typeof", "params", "sender_email", "status"]


@admin.register(OrderService)
class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phone", "ready", "compound"]
    fields = ["name", "phone", "compound", "ready"]


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ["title", "number"]


admin.site.register(Profstandard)
admin.site.register(OrderEmail)
# admin.site.register(OrderService)
admin.site.register(Chunk)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Staff)
admin.site.register(Registry)
admin.site.register(Menu)
admin.site.register(Profile)
admin.site.register(Phone)
# admin.site.register(WeldOrg)
# admin.site.register(Welder)
