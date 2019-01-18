from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, render_to_response

from comentz.forms import CommentForm
from comentz.models import Comment
from locations.models import City
from .models import Deal
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import SearchForm, DealForm

from django.utils import translation

def getLanguage(request):
    if request.user.is_authenticated:
        user_language = request.user.profile.language.name
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    else:
        user_language = request.browser_language
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language

# new version
class DealView(ListView):

    model = Deal
    template_name = "website/deals.html"
    # context_object_name = "deals"
    ordering = ["-date_posted"]


    def get(self, request, *args, **kwargs):
        getLanguage(request)
        search = request.GET.get('search', '')
        country = request.GET.get('country','')
        city = request.GET.get('city','')
        order = request.GET.get('orderBy', '')
        spec = request.GET.getlist('speciality','')
        s_form = SearchForm
        message = ""
        deals = self.get_queryset()
        if search:
            deals = deals.filter(title__icontains=search)
        else:

            if country and city and spec:
                deals = deals.filter(Q(speciality__in=spec),Q(country=country),Q(city=city))

            elif country and city:
                deals = deals.filter(Q(country=country), Q(city=city))

            elif country:
                deals = deals.filter(country=country)
            elif spec:

                    deals = deals.filter(speciality__in=spec)

            else:
                if request.user.is_authenticated:
                    message = "special"
                    if request.user.profile.city:
                        deals = deals.filter(city=request.user.profile.city)
                    elif request.user.profile.country:
                        deals = deals.filter(country=request.user.profile.country)
                    else:
                        deals = deals.all()

                else:
                    deals = deals.all()

            deals = deals.distinct()
        if deals.count() < 1:
            message = "wrong"
        paginator = Paginator(deals,3)
        page = request.GET.get('page')
        deals = paginator.get_page(page)

        return render(request, self.template_name, {'deals': deals,'s_form':s_form,'message':message})





# class DealDetailView(DetailView):
#     model = Deal
#     template_name = 'website/deal-detail.html'
#
#
#
#     # def get_context_data(self, **kwargs):
#     #     ctx = super().get_context_data(**kwargs)
#     #     ctx['comments'] = self.comments
#     #     return ctx

def deal_details(request,id):
    getLanguage(request)
    deal = get_object_or_404(Deal, id=id)

    comments = deal.comments

    initial_data = {
        'content_type': deal.get_content_type,
        'object_id': deal.id
    }
    comment_form = CommentForm(request.POST or None,initial=initial_data)
    if comment_form.is_valid():
        print(comment_form.cleaned_data)
        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        object_id = comment_form.cleaned_data.get("object_id")
        content_data = comment_form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content_data,
            parent=parent_obj
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {
        'deal':deal,
        'comments':comments,
        'comment_form':comment_form,
    }
    return render(request,'website/deal-detail.html',context=context)

class DealCreateView(LoginRequiredMixin, CreateView):
    form_class = DealForm
    model = Deal
    titleView = 'Створити проект'
    buttonView = 'Створити'
    # fields = ['title', 'description','speciality','country','city']

    template_name = 'website/deal_form.html'

    def get_form(self, form_class=None):
        form = super(DealCreateView, self).get_form(form_class)
        form.fields['speciality'].widget.attrs.update({'id': 'choices-multiple-remove-button','placeholder':_('Введіть спеціальності')})
        form.fields['country'].widget.attrs.update({'class': 'form-control'})
        form.fields['city'].widget.attrs.update({'class': 'form-control'})

        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)
        ctx['titleView'] = self.titleView
        ctx['buttonView'] = self.buttonView
        return ctx



class DealUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Deal
    form_class = DealForm
    # titleView = 'Update deal'
    # buttonView = 'Update'
    # fields = ['title', 'description', 'speciality', 'country', 'city']

    template_name = 'website/deal_update.html'

    def get_form(self, form_class=None):
        form = super(DealUpdateView, self).get_form(form_class)
        form.fields['speciality'].widget.attrs.update({'id': 'choices-multiple-remove-button','placeholder':_('Введіть спеціальності')})
        form.fields['country'].widget.attrs.update({'class': 'form-control'})
        form.fields['city'].widget.attrs.update({'class': 'form-control'})

        return form

    def form_valid(self, form):
        form.fields['speciality'].widget.attrs.update(
            {'id': 'choices-multiple-remove-button', 'placeholder': _('Введіть спеціальності')})
        form.fields['country'].widget.attrs.update({'class': 'form-control'})
        form.fields['city'].widget.attrs.update({'class': 'form-control'})
        form.instance.author = self.request.user

        return super().form_valid(form)

    # # def get_context_data(self, **kwargs):
    # #     ctx = super().get_context_data(**kwargs)
    # #     ctx['titleView'] = self.titleView
    # #     ctx['buttonView'] = self.buttonView
    # #     return ctx
    #
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class DealDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Deal
    titleView = 'Delete deal'
    buttonView = 'Delete'
    template_name = 'website/deal-delete.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titleView'] = self.titleView
        ctx['buttonView'] = self.buttonView
        return ctx

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# def cabinet(request):
#     return render(request, 'users/cabinet.html')


def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'cities/city_dropdown_list_options.html', {'cities': cities})

def test(request):
    return render(request,'website/deal_update.html')
@login_required
def myideas(request):
    getLanguage(request)
    author = Deal.objects.filter(author=request.user)

    return render(request,'website/myideas.html',{'author':author})

def landing(request):
    getLanguage(request)
    if request.user.is_authenticated:
        return redirect('deals-home')
    return render(request,'website/landing.html')





# old version
# def home(request):
#     search = request.GET.get('search', '')
#     country = request.GET.get('country','')
#     city = request.GET.get('city','')
#     order = request.GET.get('orderBy', '')
#     spec = request.GET.getlist('speciality','')
#     s_form = SearchForm
#     message = ""
#     # if request.method == "GET":
#     #     if s_form.is_valid():
#
#
#     # form = DealForm
#     if search:
#         deals = Deal.objects.filter(title__icontains=search).order_by("-date_posted")
#     else:
#
#         if country and city and spec:
#             deals = Deal.objects.filter(Q(speciality__in=spec),Q(country=country),Q(city=city)).order_by("-date_posted")
#
#         elif country and city:
#             deals = Deal.objects.filter(Q(country=country), Q(city=city)).order_by("-date_posted")
#
#         elif country:
#             deals = Deal.objects.filter(country=country).order_by("-date_posted")
#         elif spec:
#
#                 deals = Deal.objects.filter(speciality__in=spec).order_by("-date_posted")
#
#         else:
#             if request.user.is_authenticated:
#                 message = "special"
#                 deals = Deal.objects.filter(speciality=request.user.profile.speciality).order_by("-date_posted")
#
#             else:
#
#                 deals = Deal.objects.all().order_by("-date_posted")
#
#     paginator = Paginator(deals,1)
#     if deals.count() < 1:
#         message = "wrong"
#     return render(request, 'website/deals.html', {'deals': deals,'s_form':s_form,'message':message})