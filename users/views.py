from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.db.models.functions import Concat
from django.db.models import Q, F
from django.db.models import Value as V
from django.contrib.auth.decorators import login_required
from deals.models import Deal
from deals.views import getLanguage
from users.models import City, Chat, Profile, Message
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    SearchPeopleForm,
    MessageForm,
)


def register(request):
    getLanguage(request)
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            messages.success(
                request,
                "%s %s" % ("Your account has been created. Please login as", username),
            )
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("create-profile")

    else:
        form = UserRegisterForm()
    return render(request, "users/reg.html", {"form": form})


@login_required
def fill_profile(request):
    getLanguage(request)
    usr = request.user
    form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid():
        country = form.cleaned_data.get("country")
        city = form.cleaned_data.get("city")
        language = form.cleaned_data.get("language")
        speciality = form.cleaned_data.get("speciality")
        skills = form.cleaned_data.get("skills")
        status = form.cleaned_data.get("status")
        bio = form.cleaned_data.get("bio")
        facebook = form.cleaned_data.get("facebook")
        linkedin = form.cleaned_data.get("linkedin")
        form.save()
        return redirect("deals-home")
    else:
        print(form.errors)
        messages.error(request, form.errors)
    return render(request, "users/fill_profile.html", context={"form": form})


@login_required
def profile(request):
    getLanguage(request)
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "%s" % "Your profile has been updated")
            return redirect("profile")
    else:
        getLanguage(request)
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {"u_form": u_form, "p_form": p_form}

    return render(request, "users/cabinet.html", context)


def people(request):
    search = request.GET.get("search", "")
    country = request.GET.get("country", "")
    city = request.GET.get("city", "")
    spec = request.GET.getlist("speciality", "")
    skills = request.GET.getlist("skills", "")
    s_form = SearchPeopleForm
    message = ""
    users = User.objects.all()
    if search:
        users = users.annotate(
            full_name=Concat("first_name", V(" "), "last_name")
        ).filter(full_name__icontains=search)
        print("search")

    if users.count() < 1:
        message = "wrong"

    paginator = Paginator(users, 5)
    page = request.GET.get("page")
    users = paginator.get_page(page)

    context = {"people": users, "s_form": s_form, "message": message}
    return render(request, "website/users.html", context)


def userDetails(request, slug):
    user = User.objects.get(username__iexact=slug)
    deals = Deal.objects.filter(author=user)
    return render(
        request, "users/user-details.html", context={"usr": user, "deals": deals}
    )


def load_cities(request):
    country_id = request.GET.get("country")
    cities = City.objects.filter(country_id=country_id).order_by("name")
    return render(request, "cities/city_dropdown_list_options.html", {"cities": cities})


# Messages and dialogs
class DialogsView(View):
    def get(self, request):
        getLanguage(request)
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(
            request,
            "users/dialogs.html",
            {"user_profile": request.user, "chats": chats},
        )


class MessagesView(View):
    def get(self, request, chat_id):
        getLanguage(request)
        chats = Chat.objects.filter(members__in=[request.user.id])
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(
                    author=request.user
                ).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            "users/messages.html",
            {
                "user_profile": request.user,
                "chat": chat,
                "form": MessageForm(),
                "chats": chats,
            },
        )

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse("messages", kwargs={"chat_id": chat_id}))


class CreateDialogView(View):
    def get(self, request, user_id):
        chats = (
            Chat.objects.filter(
                members__in=[request.user.id, user_id], type=Chat.DIALOG
            )
            .annotate(c=Count("members"))
            .filter(c=2)
        )
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse("messages", kwargs={"chat_id": chat.id}))


@login_required
def get_count_of_unread_messages(request):
    chats = Chat.objects.filter(members__in=[request.user.id])
    message_count = (
        Message.objects.filter(chat__in=chats, is_readed=False)
        .exclude(author=request.user)
        .count()
    )
    return JsonResponse({"count": message_count}, content_type="application/json")
