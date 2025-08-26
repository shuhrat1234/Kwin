from django import template

register = template.Library()

@register.filter
def get_name_by_lang(product, lang):
    return product.get_name(lang)

@register.filter
def get_color_by_lang(product, lang):
    return product.get_color(lang)  


@register.filter
def get_description_by_lang(product, lang):
    return product.get_desc(lang)

@register.filter
def is_in_cart(product, user):
    if not user.is_authenticated:
        return False
    return user.carts.filter(product=product).exists()

