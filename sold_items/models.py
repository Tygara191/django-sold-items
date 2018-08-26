import os

from PIL import ImageEnhance
from django.db import models
from django.template.defaultfilters import slugify
from unidecode import unidecode
from likert_field.models import LikertField
from easy_thumbnails.fields import ThumbnailerImageField
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

def reduce_opacity(im, opacity):
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def Imprint(im, inputtext, font=None, color=None, opacity=.6, margin=(30,30)):
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    textlayer = Image.new("RGBA", im.size, (0,0,0,0))
    textdraw = ImageDraw.Draw(textlayer)

    textwidth, textheight = textdraw.textsize(inputtext, font=font)
    width, height = im.size

    x = margin[0]
    y = height - textheight - margin[1]

    textdraw.text((x, y), inputtext, font=font, fill=color)
    if opacity != 1:
        textlayer = reduce_opacity(textlayer,opacity)
    return Image.composite(textlayer, im, textlayer)

class BaseModel(models.Model):
    date_add  = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата на създаване"))
    date_edit = models.DateTimeField(auto_now=True, verbose_name=_("Дата на редакция"))

    class Meta:
        abstract = True

class Category(BaseModel):
    cat_name = models.CharField(max_length=255, verbose_name=_("Име на категорията"))

    def __str__(self):
        return u'%s' % self.cat_name

    class Meta:
        verbose_name = _("категория")
        verbose_name_plural = _("категории")

class Manufacturer(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Име на производителя"))
    image = models.ImageField(verbose_name=_("Лого на производителя"), upload_to="manufacturers")

    def __str__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name = _("производител")
        verbose_name_plural = _("производители")

class PlaceSize(models.Model):
    low_limit = models.IntegerField(verbose_name=_("От (кв.м)"))
    high_limit = models.IntegerField(verbose_name=_("До (кв.м)"))

    def __str__(self):
        return "От %d до %d кв.м" % (self.low_limit, self.high_limit)

    class Meta:
        verbose_name = _("размер")
        verbose_name_plural = _("размери")

class EnergyClass(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Клас"), help_text="Пример: A++")

    def __str__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = _("енергиен клас")
        verbose_name_plural = _("енергийни класове")

class Klimatik(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name=_("Номер"))

    # Core features
    title = models.CharField(max_length=255, verbose_name=_("Име"))
    slug = models.SlugField()
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("Цена"))
    image = ThumbnailerImageField(upload_to='klimatici', verbose_name=_("Снимка с високо качество"))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name=_("Категория"))
    available = models.BooleanField(verbose_name=_("В наличност"))
    guarantee_months = models.IntegerField(verbose_name=_("Гаранционен период в месеци"))
    description = models.TextField(verbose_name=_("Описание"))
    manufacturer = models.ForeignKey(Manufacturer, null=True, related_name="klimatici", on_delete=models.SET_NULL, verbose_name=_("Производител"))

    # Detailed specs
    places_size = models.ForeignKey(PlaceSize, null=True, related_name="klimatici", on_delete=models.SET_NULL, verbose_name=_("Размер на помещенията"))
    energy_class_warm = models.ForeignKey(EnergyClass, null=True, related_name="klimatici_warm", on_delete=models.SET_NULL, verbose_name=_("Енергиен клас отопление"))
    energy_class_cold = models.ForeignKey(EnergyClass, null=True, related_name="klimatici_cold", on_delete=models.SET_NULL, verbose_name=_("Енергиен клас охлаждане"))
    power = models.IntegerField(null=True, verbose_name=_("Мощност"), help_text=_("Мерна единица: BTU"))
    output_power_warm = models.CharField(max_length=255, null=True, verbose_name=_("Отдавана мощност(отопление)"), help_text=_("Мерна единица: kW"))
    output_power_cold = models.CharField(max_length=255, null=True, verbose_name=_("Отдавана мощност(охлаждане)"), help_text=_("Мерна единица: kW"))
    consumed_power_warm = models.CharField(max_length=255, null=True, verbose_name=_("Консумирана мощност(отопление)"), help_text=_("Мерна единица: kW"))
    consumed_power_cold = models.CharField(max_length=255, null=True, verbose_name=_("Консумирана мощност(охлаждане)"), help_text=_("Мерна единица: kW"))
    input_voltage = models.CharField(max_length=255, null=True, verbose_name=_("Входно напрежение"), help_text=_("Мерна единица: V"))
    inside_size = models.CharField(max_length=255, null=True, verbose_name=_("Размери на вътрешното тяло Ш x В x Д"), help_text=_("Мерна единица: MM"))
    outside_size = models.CharField(max_length=255, null=True, verbose_name=_("Размери на външното тяло Ш x В x Д"), help_text=_("Мерна единица: MM"))
    inside_weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name=_("Тегло на вътрешното тяло"), help_text=_("Мерна единица: Кг."))
    outside_weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name=_("Тегло на външното тяло"), help_text=_("Мерна единица: Кг."))
    cold_agent = models.CharField(max_length=255, null=True, verbose_name=_("Хладилен агент"))
    origin = models.CharField(max_length=255, null=True, verbose_name=_("Произход"), help_text=_("Пример: Германия"))

    __original_image = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_image = self.image

    def discount(self):
        if self.discount_inner:
            if self.discount_inner.time_end < timezone.now():
                self.discount_inner.delete()
                return Discount.objects.none()
            else:
                return self.discount_inner
        return Discount.objects.none()

    def has_discount(self):
        has_discount = False
        try:
            has_discount = (self.discount_inner is not None)
        except Discount.DoesNotExist:
            pass
        return has_discount

    def __str__(self):
        return _(u'%s (номер %d)') % (self.title, self.id)

    def save(self, *args, **kwargs):
        # Generate slug from title
        self.slug = slugify(unidecode(self.title))

        # Prevent same slug
        while True:
            try:
                Klimatik.objects.exclude(id=self.id).get(slug=self.slug)
                self.slug = u"%s%d" % (self.slug, 1)
            except Klimatik.DoesNotExist:
                break

        if self.has_discount():
            if self.price != self.discount_inner.new_price:
                self.discount_inner.delete_default()

        # Do actual save
        super(Klimatik, self).save(*args, **kwargs)

        # Only watermark if image has changed
        if self.__original_image != self.image:
            image = Image.open(self.image.path)
            image = Imprint(
                image,
                "zdrkp",
                font = ImageFont.truetype(os.path.join(settings.BASE_DIR, "sold_items", "static", "sold_items", "fonts", "ComicSans.ttf"), 18),
                color = (51, 153, 204, 255),
                opacity = 0.6,
                margin = (30, 30)
            )
            image.save(self.image.path)

    def rating(self):
        return self.feedbacks.aggregate(klima_rating=models.Avg('feedback_rating'))['klima_rating']

    class Meta:
        verbose_name = _("климатик")
        verbose_name_plural = _("климатици")

class Discount(BaseModel):
    klimatik = models.OneToOneField(Klimatik, on_delete=models.CASCADE, verbose_name=_("Климатик"), related_name='discount_inner')
    old_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("Стара цена"))
    new_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_("Нова цена"))
    time_end = models.DateTimeField(verbose_name=_("Кога изтича намалението"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.id is not None:
            if self.time_end < timezone.now():
                    self.delete()

    def save(self, *args, **kwargs):
        if self.id is None:
            self.old_price = self.klimatik.price

        self.klimatik.price = self.new_price
        self.klimatik.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.klimatik.price = self.old_price
        self.klimatik.save()
        if self.id is not None:
            super().delete(*args, **kwargs)

    def delete_default(self, *args, **kwargs):
        if self.id is not None:
            super().delete(*args, **kwargs)

    class Meta:
        verbose_name = _("намаление")
        verbose_name_plural = _("намаления")

    def __str__(self):
        return u"Намаление на %s до %s" % (self.klimatik, self.time_end)

class Feedback(BaseModel):
    klimatik = models.ForeignKey(Klimatik, on_delete=models.CASCADE, verbose_name=_("Климатик"), related_name='feedbacks')
    person_name = models.CharField(max_length=255, verbose_name=_("Име"))
    feedback_text = models.TextField(verbose_name=_("Текст"))
    feedback_rating = LikertField(verbose_name=_("Оценка"))

    class Meta:
        verbose_name = _("отзив")
        verbose_name_plural = _("отзиви")