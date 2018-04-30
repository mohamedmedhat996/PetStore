from django.contrib.auth import authenticate
from django.db import connection
from django.shortcuts import render, redirect
from Home.models import Person, Pet, HistoryRecord, PaymentMethod, PetCategory, PetCategoryKind
from Search.models import RecentSearch, Comment


def search(request):
    cursor = connection.cursor()
    try:
        username = request.user.username
        # user = Person.objects.get(username=username)
        cursor.execute("SELECT id FROM auth_user WHERE username = %s", [username])
        id_t = list(cursor.fetchone())[0]
        user = list(Person.objects.raw("SELECT * FROM Home_person WHERE user_ptr_id = %s", [id_t]))[0]
    except:
        user = None

    # results = Pet.objects.all()
    results = Pet.objects.raw("SELECT * FROM Home_pet")
    # print(results)
    try:
        category = request.GET['category']
        if category != '':
            # results = results.filter(category__category=category)
            cursor.execute("SELECT id FROM Home_petcategory WHERE category = %s", [category])
            c_id = list(cursor.fetchone())[0]
            results = list(Pet.objects.raw("SELECT * FROM Home_pet WHERE category_id = %s", [c_id]))
    except:
        pass

    try:
        s_age = int(request.GET['s_age'])
        e_age = int(request.GET['e_age'])
        results = results.filter(age__range=[s_age, e_age]).order_by('age')
    except:
        pass
    if user is not None:
        recent_search = RecentSearch(keys=' age from : ' + request.GET['s_age'] + ' to : ' + request.GET['e_age'] + ' category : ' + category, user=user)
        recent_search.save()
    context = {
        'user': user,
        'results': results,
    }
    return render(request, 'results.html', context)


def details(request, pet_pk):
    cursor = connection.cursor()
    try:
        username = request.user.username
        # user = Person.objects.get(username=username)
        cursor.execute("SELECT id FROM auth_user WHERE username = %s", [username])
        id_t = list(cursor.fetchone())[0]
        user = list(Person.objects.raw("SELECT * FROM Home_person WHERE user_ptr_id = %s", [id_t]))[0]
    except:
        user = None

    # pet = Pet.objects.get(pk=pet_pk)
    pet = list(Pet.objects.raw("SELECT * FROM Home_pet WHERE id = %s", [pet_pk]))[0]
    print(pet)
    # records = HistoryRecord.objects.filter(pet=pet)
    records = list(HistoryRecord.objects.raw("SELECT * FROM Home_historyrecord WHERE pet_id = %s", [pet_pk]))
    context = {
        'user': user,
        'pet': pet,
        'comments': pet.comment_set.all(),
        'records': records,
    }
    return render(request, 'details.html', context)


def addcomment(request, pet_pk, comment_pk):
    cursor = connection.cursor()
    if request.method == 'GET':
        username = request.user.username
        cursor.execute("SELECT id FROM auth_user WHERE username = %s", [username])
        id_t = list(cursor.fetchone())[0]
        user = list(Person.objects.raw("SELECT * FROM Home_person WHERE user_ptr_id = %s", [id_t]))[0]
        if user.is_active:
            pet = list(Pet.objects.raw("SELECT * FROM Home_pet WHERE id = %s", [pet_pk]))[0]
            body = request.GET['body']
            comment = Comment(user=user, body=body, pet=pet)
            comment.save()
            return redirect('/search/details/' + str(pet_pk) + '/')

        return redirect('/search/details/' + str(pet_pk) + '/')
    else:
        cursor.execute("DELETE FROM Search_comment WHERE id= %s",[comment_pk])
        return redirect('/search/details/' + str(pet_pk) + '/')



def verify(request, pet_pk):
    username = request.user.username
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM auth_user WHERE username = %s", [username])
    id_t = list(cursor.fetchone())[0]
    user = list(Person.objects.raw("SELECT * FROM Home_person WHERE user_ptr_id = %s", [id_t]))[0]
    pet = list(Pet.objects.raw("SELECT * FROM Home_pet WHERE id = %s", [pet_pk]))[0]

    if request.method == 'GET':
        error = ''
        context = {
            'error': error,
            'user': user,
            'pet': pet,
        }
        return render(request, 'verify.html', context)

    else:
        type = request.POST['type']
        number = request.POST['number']
        password = request.POST['password']
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