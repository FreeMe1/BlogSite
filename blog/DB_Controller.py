# -------introduction---------
# 操作数据库的函数
# -----------------------------

from blog.models import Users, UserTags, Articles
import hashlib
from datetime import datetime
SUCCESSFUL = 1
FAILED = 0
ACCOUNT_EXIST = 2
ACCOUNT_NOT_EXIST = 3
NO_TAG = 4
NO_ESSAY = 5

# -----------------------------------------


def get_hash(s):
    h = hashlib.md5()
    h.update(s.encode())
    return h.hexdigest()


def time_now():
    time = datetime.now()
    return '-'.join([
        str(time.year),
        str(time.month),
        str(time.day),
        str(time.hour),
        str(time.minute),
        str(time.second)
    ])


# -------------Users-----------------------


def create_account(nick, psd):
    if Users.objects.filter(Nick=nick):
        return ACCOUNT_EXIST
    else:
        try:
            psd = get_hash(psd)
            Users.objects.create(Nick=nick, Psd=psd)
            return SUCCESSFUL
        except Exception as e:
            print(e)
            return FAILED


def change_psd(nick, uid, new_psd):
    has_account = Users.objects.filter(Nick=nick, UserId=uid)
    if has_account:
        try:
            new_psd = get_hash(new_psd)
            has_account.update(Psd=new_psd)
            return SUCCESSFUL
        except Exception as e:
            print(e)
            return FAILED
    else:
        return ACCOUNT_NOT_EXIST


def delete_account(nick, psd):
    has_acount = Users.objects.filter(Nick=nick, Psd=get_hash(psd))
    if not has_acount:
        return ACCOUNT_NOT_EXIST
    else:
        has_acount.delete()
        return SUCCESSFUL


# --------------UserTags-------------------


def add_user_tags(uid, tag_list):
    has_account = Users.objects.filter(UserId=uid)
    new_tag = UserTags.objects
    if not has_account:
        return ACCOUNT_NOT_EXIST
    if has_account and tag_list:
        try:
            if isinstance(tag_list, list):
                for tag in tag_list:
                    if not new_tag.filter(Tags=tag):
                        new_tag.create(UserId=Users.objects.get(UserId=uid), Tags=tag)
                        return SUCCESSFUL
                    else:
                        return FAILED
            else:
                raise TypeError
        except Exception as e:
            print(e)
            return FAILED
    else:
        return FAILED


def delete_user_tags(uid, tag_list):
    has_account = UserTags.objects.filter(UserId=uid)
    if not has_account:
        return ACCOUNT_NOT_EXIST
    if has_account and tag_list:
        try:
            if isinstance(tag_list, list):
                for tag in tag_list:
                    has_account.filter(Tags=tag).delete()
                    Articles.objects.filter(UserId=uid, Tag=tag).delete()
                return SUCCESSFUL
            else:
                raise TypeError('args 2 must be type list')
        except Exception as e:
            print(e)
            return FAILED
    else:
        return FAILED


def re_name_user_tag(uid, old_tag, new_tag):
    has_old_tag = UserTags.objects.filter(UserId=uid, Tags=old_tag)
    if has_old_tag:
        try:
            tag_has_articles = Articles.objects.filter(Tag=old_tag)
            if tag_has_articles:
                try:
                    tag_has_articles.update(Tag=new_tag)
                except Exception as e:
                    print(e)
            has_old_tag.update(Tags=new_tag)
            return SUCCESSFUL
        except Exception as e:
            print(e)
            return FAILED
    else:
        return NO_TAG


# ---------------Articles--------------------


def article_add(uid, title, tag, bode):
    time = time_now()
    has_tag = UserTags.objects.filter(Tags=tag, UserId=uid)
    if not has_tag:
        return NO_TAG
    else:
        try:
            exist_article = Articles.objects.filter(UserId=uid, Title=title, Tag=tag)
            if not exist_article:
                Articles.objects.create(UserId=Users.objects.get(UserId=uid), Tag=tag, Bode=bode, Title=title,
                                        UpdateTime=time)
                return SUCCESSFUL
            else:
                exist_article.update(Bode=bode, UpdateTime=time)
                return SUCCESSFUL
        except Exception as e:
            print(e)
            return FAILED


def article_delete(uid, tag, title):
    try:
        has_art = Articles.objects.filter(UserId=uid, Tag=tag, Title=title)
        if has_art:
            has_art.delete()
            return SUCCESSFUL
        else:
            return FAILED
    except Exception as e:
        print(e)
        return FAILED


def article_re_title(uid, tag, old_title, new_title):
    try:
        has_art = Articles.objects.filter(UserId=uid, Tag=tag, Title=old_title)
        if has_art:
            has_art.update(Title=new_title)
            return SUCCESSFUL
        else:
            return FAILED
    except Exception as e:
        print(e)
        return FAILED


def article_change_tag(uid, old_tag, new_tag, title):
    try:
        has_art = Articles.objects.filter(UserId=uid, Tag=old_tag, Title=title)
        has_tag = UserTags.objects.filter(UserId=uid, Tags=new_tag)
        if has_art and has_tag:
            has_art.update(Tag=new_tag)
            return SUCCESSFUL
        else:
            return FAILED
    except Exception as e:
        print(e)
        return FAILED

# ------------API-functions----------------


