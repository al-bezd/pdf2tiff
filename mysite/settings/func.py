alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}

from django.template.defaultfilters import slugify as django_slugify
from wagtail.admin.edit_handlers import MultiFieldPanel
from wagtail.admin.edit_handlers import FieldPanel
def slugify(s):
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))

def set_promote_panels():
    return [
        MultiFieldPanel([
            FieldPanel('keywords'),
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('show_in_menus'),
            FieldPanel('search_description'),
        ], heading='ОБЩИЕ НАСТРОЙКИ СТРАНИЦ')
    ]