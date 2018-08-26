from django.contrib import admin
from django.urls import reverse_lazy

from . import models
from . import forms

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Manufacturer)
admin.site.register(models.PlaceSize)

class EnergyClassAdmin(admin.ModelAdmin):
    list_display = ['title']
admin.site.register(models.EnergyClass, EnergyClassAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['klimatik', 'person_name', 'feedback_text', 'feedback_rating']
admin.site.register(models.Feedback, FeedbackAdmin)

class DiscountAdmin(admin.ModelAdmin):
    list_display = ['klimatik', 'new_price', 'old_price', 'time_end']
    exclude = ['old_price']
admin.site.register(models.Discount, DiscountAdmin)

class KlimaticiAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'price', 'undiscounted_price', 'category', 'available', 'origin', 'view_klimatik']

    def undiscounted_price(self, obj):
        if obj.discount:
            return obj.discount().old_price
        else:
            return "-"
    undiscounted_price.short_description = "Цена преди намалението"

    def view_klimatik(self, obj):
        return '<a href="%s" target="_blank">%s</a>' % (reverse_lazy('sold_items_details', kwargs={'slug': obj.slug}), "Виж обявата")
    view_klimatik.short_description = "Преглед"
    view_klimatik.allow_tags = True


    exclude = ['slug']

    form = forms.KlimatikForm
admin.site.register(models.Klimatik, KlimaticiAdmin)