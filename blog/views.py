from django.shortcuts import render, HttpResponse, redirect
from blog import models
from blog.DB_Controller import *

# Create your views here.

DELETE_OPTIONS_LOCKED = True

# -----------page-requests-------------


def index(requests):
    """
    首页函数
    :param requests:
    :return:
    """
    try:
        if requests.session['is_login']:
            db_u = models.Users.objects.get(UserId=requests.session['uid'])
            nick = db_u.Nick
            if 'HTTP_X_FORWARDED_FOR' in requests.META.keys():
                ip = requests.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = requests.META['REMOTE_ADDR']
            response = render(requests, 'mode.html', {'nick': nick})
            response.set_cookie('right_hear', get_hash(ip))
            return response
        else:
            return redirect('/login/')
    except Exception as e:
        print(e)
        return redirect('/login/')


def login(requests):
    """
    登陆函数
    :param requests:
    :return:
    """
    return render(requests, 'login.html')

# -----------API-requests--------------


def confirm(requests):
    """
    验证登陆并设置session
    :param requests:
    :return:
    """
    try:
        nick = requests.POST['nick']
        psd = get_hash(requests.POST['psd'])
        db = models.Users.objects.filter(Nick=nick, Psd=psd)
        if db:
            requests.session['is_login'] = True
            requests.session['uid'] = db[0].UserId
            return redirect('/')
        else:
            return redirect('/login/')
    except Exception as e:
        print(e)
        return HttpResponse('出错了:)')


def get_tags(requests):
    data = []
    try:
        uid = requests.session['uid']
        db = models.UserTags.objects.filter(UserId=uid)
        for i in db:
            data.append(i.Tags)
        return HttpResponse(str(data))
    except Exception as e:
        print(e)
        return redirect('/login/')


def add_tag(requests):
    try:
        uid = requests.session['uid']
        new_tag = requests.POST['new_tag']
        if add_user_tags(uid, [new_tag]) == SUCCESSFUL:
            return HttpResponse('done')
        else:
            return HttpResponse('failed')
    except Exception as e:
        print(e)
        return redirect('/login/')


def delete_tag(requests):
    try:
        if not DELETE_OPTIONS_LOCKED:
            uid = requests.session['uid']
            deleting_tag = requests.POST['deleting_tag']
            if delete_user_tags(uid, [deleting_tag]) == SUCCESSFUL:
                return HttpResponse('done')
            else:
                return HttpResponse('failed')
        else:
            return HttpResponse('failed')
    except Exception as e:
        print(e)
        return redirect('/login/')


def get_tag_article(requests):
    data = {}
    tmp = []
    try:
        uid = requests.session['uid']
        tags = models.UserTags.objects.filter(UserId=uid)
        for t in tags:
            db = models.Articles.objects.filter(UserId=uid, Tag=t.Tags)
            for d in db:
                tmp.append([d.Title, str(d.UpdateTime)])
            data[t.Tags] = tmp
            tmp = []
        return HttpResponse(str(data))
    except Exception as e:
        print(e)
        return redirect('/login/')


def add_article(requests):
    try:
        uid = requests.session['uid']
        tag = requests.POST['tag']
        title = requests.POST['title']
        bode = requests.POST['bode']
        if article_add(uid, title, tag, bode) == SUCCESSFUL:
            return HttpResponse('done')
        else:
            return HttpResponse('failed')
    except Exception as e:
        print(e)
        return redirect('/login/')


def get_article(requests):
    try:
        uid = requests.session['uid']
        tag = requests.POST['tag']
        title = requests.POST['title']
        has_art = models.Articles.objects.get(UserId=uid, Tag=tag, Title=title)
        if has_art:
            return HttpResponse(has_art.Bode)
        else:
            return HttpResponse('failed')
    except Exception as e:
        print(e)
        return redirect('/login/')


def index_get_article(requests):
    try:
        uid = requests.session['uid']
        tag = requests.GET['tag']
        title = requests.GET['title']
        has_art = models.Articles.objects.get(UserId=uid, Tag=tag, Title=title)
        if has_art:
            return HttpResponse(has_art.Bode)
        else:
            return HttpResponse('文章不存在 :)')
    except Exception as e:
        print(e)
        return redirect('/login/')