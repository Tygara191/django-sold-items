from django.core.exceptions import FieldDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from . import models, forms
from .common import is_int, get_clean_params
# Create your views here.
def main_listing(request):
    context = {}

    q = models.Klimatik.objects

    q_in = request.GET.get('q')
    if q_in:
        if request.GET.get('incd'):
            q = q.filter(Q(title__search=q_in) | Q(description__search=q_in))
        else:
            q = q.filter(title__search=q_in)

    q_c = q.count()

    if q_c > 0:

        # Do filtering here

        # Guarantee period
        gp = get_clean_params(request, 'gp')
        if gp:
            q = q.filter(guarantee_months__in=gp)

        # Energy class cold
        ecc = get_clean_params(request, 'ecc')
        if ecc:
            q = q.filter(energy_class_cold__in=ecc)

        # Energy class warm
        ecw = get_clean_params(request, 'ecw')
        if ecw:
            q = q.filter(energy_class_warm__in=ecw)

        # Place sizes
        ps = get_clean_params(request, 'ps')
        if ps:
            q = q.filter(places_size__in=ps)

        # Categories
        cat = request.GET.get('cat')
        if cat and is_int(cat):
            q = q.filter(category=cat)

        # Price min
        pmin = request.GET.get('pmin')
        if pmin:
            if is_int(pmin):
                q = q.filter(price__gte=pmin)

        # Price min
        pmax = request.GET.get('pmax')
        if pmax:
            if is_int(pmax):
                q = q.filter(price__lte=pmax)

        # Ordering
        order = request.GET.get('order')
        if order:
            order_f = order
            try:
                if order.startswith('-') and len('order')>1:
                    order_f = order[1:]
                models.Klimatik._meta.get_field(order_f)
                q = q.order_by(order)
            except FieldDoesNotExist:
                pass

    all_klimatici = q.filter()

    # We now prepare all the data we need for rendering
    paginator = Paginator(all_klimatici, 6)

    try:
        klimatici = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        klimatici = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        klimatici = paginator.page(paginator.num_pages)

    context['klimatici'] = klimatici
    context['categories'] = models.Category.objects.all()

    filter_criteria = {
        "energy_classes_cold": {}, # Done 1
        "energy_classes_warm": {}, # Done 1
        "place_sizes": {}, # Done 1
        "guarantee_periods": [], # Done 1
        "manufacturers": {}, # Done 1
        "powers": [], # Done 1
        "price_max": 0, # Done
        "price_min": 0 # Done
    }

    for klimatik in all_klimatici:
        # Energy classes cold
        if klimatik.energy_class_cold_id not in filter_criteria["energy_classes_cold"]:
            filter_criteria["energy_classes_cold"][klimatik.energy_class_cold_id] = klimatik.energy_class_cold

        # Energy classes warm
        if klimatik.energy_class_warm_id not in filter_criteria["energy_classes_warm"]:
            filter_criteria["energy_classes_warm"][klimatik.energy_class_warm_id] = klimatik.energy_class_warm

        # Place sizes
        if klimatik.places_size_id not in filter_criteria["place_sizes"]:
            filter_criteria["place_sizes"][klimatik.places_size_id] = klimatik.places_size

        # Manufactures
        if klimatik.manufacturer_id not in filter_criteria["manufacturers"]:
            filter_criteria["manufacturers"][klimatik.manufacturer_id] = klimatik.manufacturer

        # Powers
        if klimatik.power not in filter_criteria["powers"]:
            filter_criteria["powers"].append(klimatik.power)

        # Guarantee periods
        if klimatik.guarantee_months not in filter_criteria["guarantee_periods"]:
            filter_criteria["guarantee_periods"].append(klimatik.guarantee_months)

    # Convert dicts to lists
    for key, value in filter_criteria.items():
        if isinstance(value, dict):
            # Now convert to
            list = []
            for subkey, subvalue in value.items():
                list.append(subvalue)
            filter_criteria[key] = list


    filter_criteria['price_min'] = int(filter_criteria.get("price_min"))
    filter_criteria['price_max'] = int(filter_criteria.get("price_max"))

    context.update(filter_criteria)

    return render(request, 'sold_items/listing.html', context)

def details(request, slug):
    klimatik = get_object_or_404(models.Klimatik, slug=slug)
    context = {
        'klimatik':klimatik,
        'feedback':False,
        'feedback_success':False
    }

    if request.method == "POST":
        form = forms.FeedbackForm(request.POST)
        if form.is_valid():
            new_feedback = models.Feedback(
                klimatik = klimatik,
                person_name = form.cleaned_data['person_name'],
                feedback_text = form.cleaned_data['feedback_text'],
                feedback_rating = form.cleaned_data['feedback_rating'],
            )
            new_feedback.save()

            context['form'] = ""
            context['feedback_success'] = True
        else:
            context['form'] = form
        context['feedback'] = True
    else:
        context['form'] = forms.FeedbackForm()

    return render(request, 'sold_items/details.html', context)