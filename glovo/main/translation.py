from .models import *
from modeltranslation.translator import TranslationOptions, register


@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('store_name', 'description', 'address')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'description',)


@register(ProductCombo)
class ProductComboTranslationOptions(TranslationOptions):
    fields = ('combo_name', 'description',)
