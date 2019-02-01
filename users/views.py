from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View

from deals.models import Deal
from deals.views import getLanguage
from users.models import City, Chat, Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SearchPeopleForm, MessageForm
from django.contrib.auth.decorators import login_required


def register(request):
    getLanguage(request)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, '%s %s' % ('Your account has been created. Please login as',username))
            form.save()
            user = authenticate(username = username, password = password)
            login(request,user)
            return redirect('create-profile')

    else:
        form = UserRegisterForm()
    return render(request,'users/reg.html',{'form':form})
@login_required
def fill_profile(request):
    getLanguage(request)
    usr = request.user
    form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
    if form.is_valid():
        country = form.cleaned_data.get('country')
        city = form.cleaned_data.get('city')
        language = form.cleaned_data.get('language')
        speciality = form.cleaned_data.get('speciality')
        skills = form.cleaned_data.get('skills')
        status = form.cleaned_data.get('status')
        bio = form.cleaned_data.get('bio')
        facebook = form.cleaned_data.get('facebook')
        linkedin = form.cleaned_data.get('linkedin')
        form.save()
        # Profile.objects.filter(user=usr).update(
        #     country=country,
        #     city=city,
        #     language=language,
        #     speciality=speciality,
        #     skills=skills,
        #     status=status,
        #     bio=bio,
        #     linkedin=linkedin,
        #     facebook=facebook
        #
        #
        # )
        return redirect('deals-home')
    return render(request,'users/fill_profile.html',context={'form':form})
@login_required
def profile(request):
    getLanguage(request)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '%s' % 'Your profile has been updated')
            return redirect('profile')
    else:
        getLanguage(request)
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }


    return render(request,'users/cabinet.html',context)



def people(request):
    search = request.GET.get('search', '')
    country = request.GET.get('country', '')
    city = request.GET.get('city', '')
    # order = request.GET.get('orderBy', '')
    spec = request.GET.getlist('speciality', '')
    skills = request.GET.getlist('skills','')
    s_form = SearchPeopleForm
    message = ""
    users = User.objects.filter(profile__speciality=not None,profile__country=not None,profile__city=not None)
    if search:
        for term in search.split():
            users = users.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term))
    else:
        if country and city and spec and skills:
            users = users.filter(Q(profile__speciality__in=spec), Q(profile__country=country), Q(profile__city=city),Q(profile__skills__in=skills))
        elif country and city and spec:
            users = users.filter(Q(profile__speciality__in=spec), Q(profile__country=country), Q(profile__city=city))
        elif country and city and skills:
            users = users.filter(Q(profile__skills__in=skills), Q(profile__country=country), Q(profile__city=city))

        elif country and city:
            users = users.filter(Q(profile__country=country), Q(profile__city=city))
        elif country and spec:
            users = users.filter(Q(profile__speciality__in=spec), Q(profile__country=country))
        elif country and skills:
            users = users.filter(Q(profile__skills__in=skills), Q(profile__country=country))
        elif country:
            users = users.filter(profile__country=country)
        elif spec and skills:
            users = users.filter(Q(profile__speciality__in=spec), Q(profile__skills__in=skills))
        elif spec:
            users = users.filter(profile__speciality__in=spec)
        elif skills:
            users = users.filter(profile__skills__in=skills)

        else:
            users = users.all()
        #     if request.user.is_authenticated:
        #         message = "special"
        #         users = users.filter(speciality=request.user.profile.speciality)


    users = users.distinct()

    if users.count() < 1:
        message = "wrong"

    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    users = paginator.get_page(page)

    context={
        'people': users,
        's_form': s_form,
        'message':message
    }
    return render(request, 'website/users.html', context)


def userDetails(request,slug):
    user = User.objects.get(username__iexact=slug)
    deals = Deal.objects.filter(author=user)
    return render(request, 'users/user-details.html', context={'usr':user,'deals':deals})

def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'cities/city_dropdown_list_options.html', {'cities': cities})

#Messages and dialogs

class DialogsView(View):
    def get(self, request):
        getLanguage(request)
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(request, 'users/dialogs.html', {'user_profile': request.user, 'chats': chats})


class MessagesView(View):
    def get(self, request, chat_id):
        getLanguage(request)
        chats = Chat.objects.filter(members__in=[request.user.id])
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'users/messages.html',
            {

                'user_profile': request.user,
                'chat': chat,
                'form': MessageForm(),
                'chats': chats,
            }
        )

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('messages', kwargs={'chat_id': chat_id}))

class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(
            c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('messages', kwargs={'chat_id': chat.id}))

def check_name(request):
    print("Hello")
    username = request.GET["username"]
    people = {"max2211","admin"}
    # people = User.objects.all()
    if username in people:
        return HttpResponse("yes")
    else:
        return HttpResponse("no")