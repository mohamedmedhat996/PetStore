from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from Home.models import Person, Pet, HistoryRecord, PaymentMethod, PetCategory, PetCategoryKind
from Search.models import RecentSearch, Comment


def search(request):
    try:
        user = Person.objects.get(username=request.user)
    except:
        user = None
    results = Pet.objects.all()
    try:
        category = request.GET.__getitem__('category')
        if category != '':
            results = results.filter(category__category=category)
    except:
        pass

    try:
        s_age = int(request.GET.__getitem__('s_age'))
        e_age = int(request.GET.__getitem__('e_age'))
        results = results.filter(age__range=[s_age, e_age]).order_by('age')
    except:
        pass
    if user is not None:
        recent_search = RecentSearch(keys=' age from : ' + request.GET.__getitem__('s_age') + ' to : ' + request.GET.__getitem__('e_age') + ' category : ' + category, user=user)
        recent_search.save()
    context = {
        'user': user,
        'results': results,
    }
    return render(request, 'results.html', context)


def details(request, pet_pk):
    try:
        user = Person.objects.get(username=request.user)
    except:
        user = None
    pet = Pet.objects.get(pk=pet_pk)
    records = HistoryRecord.objects.filter(pet=pet)
    context = {
        'user': user,
        'pet': pet,
        'comments': pet.comment_set.all(),
        'records': records,
    }
    return render(request, 'details.html', context)


def addcomment(request, pet_pk, comment_pk):
    if request.method == 'GET':
        user = Person.objects.get(username=request.user)
        if user.is_active:
            pet = Pet.objects.get(pk=pet_pk)
            body = request.GET.__getitem__('body')
            comment = Comment(user=user, body=body, pet=pet)
            comment.save()
            return redirect('/search/details/' + str(pet_pk) + '/')

        return redirect('/search/details/' + str(pet_pk) + '/')
    else:
        Comment.objects.get(pk=comment_pk).delete()
        return redirect('/search/details/' + str(pet_pk) + '/')



def verify(request, pet_pk):
    if request.method == 'GET':
        user = Person.objects.get(username=request.user)
        pet = Pet.objects.get(pk=pet_pk)
        error = ''
        context = {
            'error': error,
            'user': user,
            'pet': pet,
        }
        return render(request, 'verify.html', context)

    else:
        user = Person.objects.get(username=request.user)
        pet = Pet.objects.get(pk=pet_pk)
        type = request.POST.__getitem__('type')
        number = request.POST.__getitem__('number')
        password = request.POST.__getitem__('password')
        if PaymentMethod.objects.filter(user=user, number=number, type=type).exists() and pet.state == 'available':
            user = authenticate(username=request.user, password=password)
            if user is not None:
                pet.state = 'sold'
                pet.save()
                error = ''
                notification = 'done successfully'
            else:
                error = 'wrong password!'
                notification = 'error occured'
        else:
            error = 'payment method does not exist or bet is already sold!'
            notification = 'error occured'
        context = {
            'notification': notification,
            'error': error,
            'user': user,
            'pet': pet,
        }
        return render(request, 'verify.html', context)


def kind(request, category_pk, kind_pk):
    kind = PetCategoryKind.objects.get(pk=kind_pk)
    try:
        user = Person.objects.get(username=request.user)
    except:
        user = None
    context = {
        'user': user,
        'kind': kind,
        'category': kind.category,
        'pets': Pet.objects.filter(kind=kind)
    }
    return render(request, 'kind.html', context)


def category(request, category_pk):
    category = PetCategory.objects.get(pk=category_pk)
    kinds = PetCategoryKind.objects.filter(category=category)
    try:
        user = Person.objects.get(username=request.user)
    except:
        user = None
    context = {
        'category': category,
        'kinds': kinds,
        'user': user,
    }
    return render(request, 'category.html', context)