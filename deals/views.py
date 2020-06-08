from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, render_to_response

from comentz.forms import CommentForm
from comentz.models import Comment
from contact.models import Contact
from locations.models import City
from .models import Deal, DealLike
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
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


def deals_home(request):
    search = request.GET.get("search", "")
    if search:
        deals = Deal.objects.filter(title__icontains=search)
    else:
        deals = Deal.objects.all()
    paginator = Paginator(deals, 5)
    page = request.GET.get("page")
    deals = paginator.get_page(page)
    s_form = SearchForm
    return render(request, "website/deals.html", {"deals": deals, "s_form": s_form},)


@login_required
def deal_details(request, id):
    getLanguage(request)
    deal = get_object_or_404(Deal, id=id)

    comments = deal.comments
    liked = DealLike.objects.filter(user=request.user, deal=deal).exists()
    likes = DealLike.objects.filter(deal=deal).count()
    initial_data = {"content_type": deal.get_content_type, "object_id": deal.id}
    comment_form = CommentForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
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
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {
        "deal": deal,
        "comments": comments,
        "comment_form": comment_form,
        "liked": liked,
        "likes": likes,
    }
    return render(request, "website/deal-detail.html", context=context)


class DealCreateView(LoginRequiredMixin, CreateView):
    form_class = DealForm
    model = Deal
    titleView = _("Створити проект")
    buttonView = _("Створити")
    # fields = ['title', 'description','speciality','country','city']

    template_name = "website/deal_form.html"

    def get_form(self, form_class=None):
        form = super(DealCreateView, self).get_form(form_class)
        form.fields["speciality"].widget.attrs.update(
            {
                "id": "choices-multiple-remove-button",
                "placeholder": _("Введіть спеціальності"),
            }
        )
        form.fields["country"].widget.attrs.update(
            {"class": "form-control", "required": "true"}
        )
        form.fields["city"].widget.attrs.update(
            {"class": "form-control", "required": "true"}
        )
        form.fields["website_link"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Ссылка на сайт (необязательно). Например https://google.com",
            }
        )
        form.fields["presentation_link"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Ссылка на презентацию (необязательно). Например https://google.com",
            }
        )

        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)
        ctx["titleView"] = self.titleView
        ctx["buttonView"] = self.buttonView
        return ctx


class DealUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Deal
    form_class = DealForm

    template_name = "website/deal_update.html"

    def get_form(self, form_class=None):
        form = super(DealUpdateView, self).get_form(form_class)
        form.fields["speciality"].widget.attrs.update(
            {
                "id": "choices-multiple-remove-button",
                "placeholder": _("Введіть спеціальності"),
            }
        )
        form.fields["country"].widget.attrs.update({"class": "form-control"})
        form.fields["city"].widget.attrs.update({"class": "form-control"})
        form.fields["website_link"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Ссылка на сайт (необязательно). Например https://google.com",
            }
        )
        form.fields["presentation_link"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Ссылка на презентацию (необязательно). Например https://google.com",
            }
        )

        return form

    def form_valid(self, form):
        form.fields["speciality"].widget.attrs.update(
            {
                "id": "choices-multiple-remove-button",
                "placeholder": _("Введіть спеціальності"),
            }
        )
        form.fields["country"].widget.attrs.update({"class": "form-control"})
        form.fields["city"].widget.attrs.update({"class": "form-control"})
        form.instance.author = self.request.user

        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class DealDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Deal
    titleView = "Delete deal"
    buttonView = "Delete"
    template_name = "website/deal-delete.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titleView"] = self.titleView
        ctx["buttonView"] = self.buttonView
        return ctx

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def like_deal(request, id):
    if request.method == "POST":
        user = request.user
        deal = get_object_or_404(Deal, pk=id)

        like_exists = DealLike.objects.filter(user=user, deal=deal).exists()
        if not like_exists:
            DealLike.objects.get_or_create(user=user, deal=deal)
            status = "created"
        else:
            DealLike.objects.get(user=user, deal=deal).delete()
            status = "deleted"
        likes = DealLike.objects.filter(deal=deal).count()
        return JsonResponse(
            {"status": status, "likes": likes}, content_type="application/json"
        )
    else:
        return JsonResponse({"status": "error"}, content_type="application/json")


def load_cities(request):
    country_id = request.GET.get("country")
    cities = City.objects.filter(country_id=country_id).order_by("name")
    return render(request, "cities/city_dropdown_list_options.html", {"cities": cities})


@login_required
def myideas(request):
    getLanguage(request)
    author = Deal.objects.filter(author=request.user)

    return render(request, "website/myideas.html", {"author": author})


def landing(request):
    # getLanguage(request)
    # if request.method == "POST":
    #     name = request.POST.get("name")
    #     email = request.POST.get("email")
    #     message = request.POST.get("message")
    #     new_contact = Contact.objects.create(name=name, email=email, message=message)
    #     if new_contact:
    #         messages.info(request, _("Ваше повідомлення відправлено!"))
    # if request.user.is_authenticated:
    return redirect("deals-home")
    # return render(request, "website/landing.html")


def create_contact(request):
    if request.method == "GET":
        name = request.GET.get("name")
        email = request.GET.get("email")
        message = request.GET.get("message")
        new_contact = Contact.objects.create(name=name, email=email, message=message)
        contacts = Contact.objects.all()
        if new_contact:
            messages.info(request, _("Ваше повідомлення відправлено!"))
        if new_contact in contacts:
            return HttpResponse("yes")
        else:
            return HttpResponse("no")
