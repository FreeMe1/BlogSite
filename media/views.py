from django.shortcuts import render, redirect
from blog.DB_Controller import get_hash

# Create your views here.


def media(requests):
    try:
        uid = requests.session['uid']
        right_hear = requests.COOKIES['right_hear']
        if 'HTTP_X_FORWARDED_FOR' in requests.META.keys():
            ip = requests.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = requests.META['REMOTE_ADDR']
        if uid and right_hear == get_hash(ip):
            return render(requests, 'media_fpg.html')
        else:
            return redirect('/login/')
    except Exception as e:
        print(e)
        return redirect('/login/')