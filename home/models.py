from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import MultiFieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
# from pravo.pravozanami2.pravozanami.settings.func import *
#from pravozanami.settings.base import URL
#from pravozanami.settings.func import *
from wagtail.core.blocks import URLBlock, TextBlock, RawHTMLBlock, RichTextBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock

from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    StreamFieldPanel,
    PageChooserPanel,
    ObjectList,
    TabbedInterface,
)

#from custom_editor.blocks import CustomEditor
from mysite.settings.base import URL


class HomePage(Page):
    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главные страницы'

    keywords = models.TextField(blank=True, null=True, verbose_name=_('keywords'),
                                help_text=_("Ключевые слова для индексации поисковыми роботами"))
    partners_title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Партнеры (заголовок)'))
    partners_desc = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Партнеры (описание)'))
    converter_title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Конвертер (заголовок)'))
    converter_desc = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Конвертер (описание)'))
    converter_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    onas_title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('О нас (заголовок)'))
    onas_desc = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('О нас (описание)'))
    onas_image1 = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', blank=True, null=True,
        verbose_name='О нас (Изображение1)'
    )
    onas_image2 = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', blank=True, null=True,
        verbose_name='О нас (Изображение2)'
    )
    onas_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+', verbose_name='О нас (Ссылка на страницу)'
    )

    yt_videos = StreamField([
        ('YouTubeVideo', RawHTMLBlock()),
    ], verbose_name='видео с YouTube',blank=True,null=True)

    PAGE_TEMPLATE_VAR = 'page'
    #promote_panels = set_promote_panels()
    content_panels = Page.content_panels
    yt_panels = [
        MultiFieldPanel(
            [
                StreamFieldPanel('yt_videos'),
            ],
            # heading="видео с YouTube",
        ),

    ]

    banners_panels = [
        MultiFieldPanel(
            [
                InlinePanel('banner_item', label="Изображения для баннера"),
            ],
            heading="Банеры",
        ),
    ]

    converter_panels = [
        MultiFieldPanel(
            [
                FieldPanel('converter_title'),
                FieldPanel('converter_desc'),
                PageChooserPanel('converter_page'),
            ],
            heading="Конвертер",
        ),
    ]

    onas_panels = [
        MultiFieldPanel(
            [
                FieldPanel('onas_title'),
                FieldPanel('onas_desc'),
                ImageChooserPanel('onas_image1'),
                ImageChooserPanel('onas_image2'),
                PageChooserPanel('onas_page'),
            ],
            heading="О нас",
        ),
    ]

    diploms_panel = [
        MultiFieldPanel(
            [
                InlinePanel('diploms', label="Дипломы"),
                FieldPanel('partners_title'),
                FieldPanel('partners_desc'),
                InlinePanel('PartnersLogo', label="Логотипы партнеров"),
            ],
            heading="Дипломы",
        ),

    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Основное"),
            ObjectList(banners_panels, heading="Баннеры"),
            # This is our custom banner_panels. It's just a list, how easy!
            ObjectList(diploms_panel, heading="Партнеры"),
            ObjectList(converter_panels, heading="Конвертер"),
            ObjectList(yt_panels, heading="YouTube"),
            ObjectList(onas_panels, heading="О нас"),
            ObjectList(Page.promote_panels, heading="Продвижение"),
            ObjectList(Page.settings_panels, heading="Настройки"),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = {
            self.PAGE_TEMPLATE_VAR: self,
            'self': self,
            'request': request,
        }

        if self.context_object_name:
            context[self.context_object_name] = self

        context['menuitems'] = Page.objects.filter(
            live=True,
            show_in_menus=True
        )

        # context['portfolio'] = PortfolioPage.objects.all()[0:5]

        return context

    def save(self, *args, **kwargs):
        #self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ElectroKadrPage(Page):
    keywords = models.TextField(blank=True, null=True, verbose_name=_('keywords'),
                                help_text=_("Ключевые слова для индексации поисковыми роботами"))

    class Meta:
        verbose_name = 'Электронный кадровик'
        verbose_name_plural = 'Электронный кадровик'

    body = StreamField([
        ('Heading', blocks.CharBlock(form_classname="full title")),
        ('Text', RichTextBlock()),
        ('img', ImageChooserBlock()),
        ('HTML', RawHTMLBlock()),
        ('docs', DocumentChooserBlock()),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),

    ]

    PAGE_TEMPLATE_VAR = 'page'
    #promote_panels = set_promote_panels()

    def save(self, *args, **kwargs):
        #self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class SimplePage(Page):
    keywords = models.TextField(blank=True, null=True, verbose_name=_('keywords'),
                                help_text=_("Ключевые слова для индексации поисковыми роботами"))

    class Meta:
        verbose_name = 'Обычная страница'
        verbose_name_plural = 'Обычная страница'

    body = StreamField([
        ('Heading', blocks.CharBlock(form_classname="full title")),
        ('Text', RichTextBlock()),
        ('img', ImageChooserBlock()),
        ('HTML', RawHTMLBlock()),
        ('docs', DocumentChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),

    ]

    PAGE_TEMPLATE_VAR = 'page'
    #promote_panels = set_promote_panels()

    def save(self, *args, **kwargs):
        #self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BannerItem(Orderable):
    class Meta:
        verbose_name = 'Окно баннера'
        verbose_name_plural = 'Окна баннера'

    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='banner_item')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', blank=True, null=True,
        verbose_name='Изображение'
    )
    title = models.CharField(blank=True, null=True, max_length=255, verbose_name='Заголовок')
    desc = models.CharField(blank=True, null=True, max_length=255, verbose_name='Описание')
    select_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+', verbose_name='Страница'
    )
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('desc'),
        PageChooserPanel('select_page'),

    ]


class SocialItem(Orderable, models.Model):
    class Meta:
        verbose_name = 'Ссылка на соц. сеть'
        verbose_name_plural = 'Ссылка на соц. сети'

    page = ParentalKey(HomePage, related_name='socialitem')
    name = models.CharField(max_length=50, verbose_name='Наименование')
    link = models.URLField(blank=True, null=True, help_text="URL", verbose_name='Ссылка')
    text = RichTextField(blank=True, null=True, verbose_name='Текст')


class Diploms(Orderable):
    class Meta:
        verbose_name = 'Диплом'
        verbose_name_plural = 'Дипломы'

    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='diploms')
    image = models.ForeignKey('wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
                              verbose_name='Скрин диплома')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок')
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name='Описание')

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('desc'),
    ]


class PartnersLogo(Orderable):
    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'

    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='PartnersLogo')
    image = models.ForeignKey('wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='+',
                              verbose_name='Изображение')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок')
    desc = models.TextField(blank=True, null=True, verbose_name='Описание')

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('desc'),
    ]


@register_setting
class SocialMediaSettings(BaseSetting):
    class Meta:
        verbose_name = 'Социальные сети'
        verbose_name_plural = verbose_name

    youtube = models.URLField(blank=True, null=True, help_text="youtube URL")
    fb = models.URLField(blank=True, null=True, help_text="fb URL")
    telegram = models.URLField(blank=True, null=True, help_text="telegram URL")
    instagram = models.URLField(blank=True, null=True, help_text="instagram URL")
    panels = [
        MultiFieldPanel([
            FieldPanel("youtube"),
            FieldPanel("fb"),
            FieldPanel("telegram"),
            FieldPanel("instagram"),

        ], heading='Социальные сети')
    ]


@register_setting
class ContactSettings(BaseSetting):
    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = verbose_name

    tel1 = models.CharField(max_length=150, blank=True, null=True,
                            help_text="Телефон №1", verbose_name="Телефон №1")
    tel2 = models.CharField(max_length=150, blank=True, null=True,
                            help_text="Телефон №2", verbose_name="Телефон №2")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")

    address = models.CharField(max_length=255, blank=True, null=True)

    panels = [
        MultiFieldPanel([
            FieldPanel("tel1"),
            FieldPanel("tel2"),
            FieldPanel("email"),
            FieldPanel("address"),

        ], heading="Контакты")
    ]

    def get_bf_email(self):

        return f'{str(self.email).split("@")[0]}@{URL}'.replace('https://', '').replace('http://', '')

    def t2(self):
        if self.tel2 == None:
            return ''
        else:
            return self.tel2

    def t1(self):
        if self.tel1 == None:
            return ''
        else:
            return self.tel1

    def e(self):
        if self.email == None:
            return ''
        else:
            return self.email

    def a(self):
        if self.address == None:
            return ''
        else:
            return self.address


@register_setting
class PhotoMainPageSettings(BaseSetting):
    class Meta:
        verbose_name = 'Фотографии главной страницы'
        verbose_name_plural = verbose_name

    logo = models.ForeignKey(
        'wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+', blank=True,
        verbose_name='Основной логотип')
    logo_title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заголовок')
    contact_photo = models.ForeignKey('wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL,
                                      related_name='+', verbose_name='Изображение для раздела "Связаться с нами"')

    breadcrumb_photo = models.ForeignKey('wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL,
                                         related_name='+', verbose_name='Изображение для "хлебные крошки"')

    panels = [
        ImageChooserPanel('logo'),
        ImageChooserPanel('contact_photo'),
        ImageChooserPanel('breadcrumb_photo'),
    ]

