from django.core.management.base import BaseCommand
from blog.DB_Controller import *
from blog.models import Users, UserTags, Articles


def show_u():
    for i in Users.objects.all():
        print(i.Nick, i.Psd, i.UserId)
        print('\n')


def show_ut():
    for i in UserTags.objects.all():
        print(i.UserId, i.Tags)
        print('\n')


def show_a():
    for i in Articles.objects.all():
        print(i.Tag, i.Title, i.Bode, i.UserId, i.CreateTime, i.UpdateTime)
        print('\n')


class Command(BaseCommand):

    def handle(self, *args, **options):

        while True:
            c = input('>>> ')
            try:
                if c == 'q':
                    break
                print(eval(c))
            except Exception as e:
                print(e)




