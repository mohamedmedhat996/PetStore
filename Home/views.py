import random
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Home.forms import UserForm
from Home.models import Person, PaymentMethod, Pet, PetCategory, PetCategoryKind
from Search.models import RecentSearch


def index(request):
    if request.path == '/':
        return redirect('/index/')
    try:
        user = Person.objects.get(username=request.user)
    except:
        user = None
    context = {
        'user': user,
        'Pets': Pet.objects.all(),
        'recent_searches': RecentSearch.objects.filter(user=user),
        'categories': PetCategory.objects.all(),
        'kinds': PetCategoryKind.objects.all(),
    }
    return render(request, 'index.html', context)


def login_f(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.__getitem__('username')
        password = request.POST.__getitem__('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/index/')
        return render(request, "login.html", {'error': 'wrong user name or password'})


def logout_f(request):
    logout(request)
    return redirect('/index/')


def profile(request):
    try:
        user = Person.objects.get(username=request.user)
    except:
        user = None
    context = {
        'user': user,
        'PaymentMethods': PaymentMethod.objects.filter(user=user)
    }
    return render(request, 'profile.html', context)


def signup(request):
    if request.method == 'GET':
        form = UserForm(None)
        return render(request, 'signup.html', {'form': form})

    else:
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            password_conf = request.POST.__getitem__('password_conf')
            try:
                try:
                    user_e = Person.objects.get(email=user.email)
                    return render(request, 'signup.html', {'error': 'the user already exists'})
                except:
                    user_u = Person.objects.get(username=user.username)
                    return render(request, 'signup.html', {'error': 'the user already exists'})
            except:
                if password == password_conf:
                    user.set_password(password)
                    user.is_active = False
                    code = random.randint(10000000, 90000000)
                    user.code = code
                    user.save()
                    subject = 'confirmation email'
                    message = 'please enter this code to activate your account ' + str(code) + \
                              'or click the link http://127.0.0.1:8000/home/activate/' + str(user.pk) + '/' + str(code)
                    send_mail(subject, message, 'thepetstore770@gmail.com', [user.email], fail_silently=False)

                    return render(request, 'activation.html', {'user': user})
                else:
                    return render(request, 'signup.html', {'error': 'the passwords does not match'})

        else:
            return render(request, 'signup.html', {'error': 'one or more field is invalid'})


def activate(request):
    if request.method == 'POST':
        code = request.POST.__getitem__('code')
        username = request.POST.__getitem__('username')
        user = Person.objects.get(username=username)
        if user is not None:
            if str(user.code) == str(code):
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('/')
        return HttpResponse('<h1>user does not exist</h1>')
    else:
        return render(request, 'activation.html')


def activate_u(request, user_pk, code):
    user = Person.objects.get(pk=user_pk)
    if user is not None:
        if str(user.code) == str(code):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('/')
    return HttpResponse('<h1>user does not exist</h1>')


def delete(request):
    user = Person.objects.get(username=request.user)
    RecentSearch.objects.filter(user=user).delete()
    return redirect('/index/')


def addpaymentmethod(request, number):
    if request.method == 'POST':
        user = Person.objects.get(username=request.user)
        if user.is_active:
            type = request.POST.__getitem__('type')
            number = request.POST.__getitem__('number')
            payment_method = PaymentMethod(user=user, type=type, number=number)
            payment_method.save()
            return redirect('/home/profile/')

        return redirect('/home/profile/')
    else:
        user = Person.objects.get(username=request.user)
        if user.is_active:
            PaymentMethod.objects.get(user=user, number=number).delete()
            return redirect('/home/profile/')
        return redirect('/home/profile/')


def recover(request):
    if request.method == 'GET':
        return render(request, 'recover.html')
    else:
        email = request.POST.__getitem__('email')
        print(email)
        subject = 'Recover your password'
        try:
            user = Person.objects.get(email=email)
            code = random.randint(10000000, 90000000)
            user.code = code
            user.save()
            message = 'It seems that your requested to reset your password,' \
                      ' click this link http://127.0.0.1:8000/home/recover/' + str(user.pk) + '/' + str(code) + '/'
            send_mail(subject, message, 'thepetstore770@gmail.com', [email], fail_silently=False)
            return render(request, 'recover.html', {'notifications': 'an email containing'
                                                                     ' a link to reset your password is sent'})
        except:
            return render(request, 'recover.html', {'notifications': 'user does not exists'})


def recover_p(request, user_pk, code):
    if request.method == 'GET':
        try:
            user = Person.objects.get(pk=user_pk)
            if user.code == code:
                return render(request, 'recover_p.html')
            else:
                HttpResponse('<h1>e7m</h1>')
        except:
            return HttpResponse("<h1>shit</h1>")

    else:
        password = request.POST.__getitem__('password')
        password_conf = request.POST.__getitem__('password_conf')
        try:
            user = Person.objects.get(pk=user_pk)
            print(password)
            print(password_conf)
            if password == password_conf:
                user.set_password(password)
                user.save()
                return HttpResponse('<h1>done!</h1>')
            return HttpResponse('<h1>passwords doesnt match</h1>')
        except:
            return HttpResponse('<h1>user does not exists</h1>')


def contact_us(request):
    if request.method == 'GET':
        try:
            user = Person.objects.get(username=request.user)
        except:
            user = None
        return render(request, 'contactus.html', {'user': user})

    else:
        try:
            print(request.POST.__getitem__('username'))
            user = Person.objects.get(username=request.POST.__getitem__('username'))
            print(user)
            message = request.POST.__getitem__('message')
            email = request.POST.__getitem__('email')
            subject = 'contact us: from: ' + user.username
            send_mail(subject, message, 'thepetstore770@gmail.com', ['thepetstore770@gmail.com'], fail_silently=False)
            return redirect('/index/')

        except:
            return redirect('/contactus/')