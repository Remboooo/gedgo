from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from gedgo.models import BlogPost
from gedgo.views.util import render, process_comments

from datetime import datetime


def blog(request, year, month):
    "Blog front page - listing posts by creation date."
    posts = BlogPost.objects.all().order_by("-created")

    if year:
        posts = posts.filter(created__year=year)
    if month:
        posts = posts#.filter(created__month=month)

    paginator = Paginator(posts, 2)

    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    months = set(
        (d.year, d.month, datetime(2015, d.month, 1).strftime('%B'))
        for d in BlogPost.objects.values_list('created', flat=True))

    return render(
        request,
        "blogpost_list.html",
        {'posts': posts, 'months': months},
    )


def blog_list(request):
    return blog(request, None, None)


def blogpost(request, post_id):
    "Single post."

    noun = "blog post"
    form, redirect = process_comments(request, noun)
    if redirect is not None:
        return redirect

    context = {
        'post': get_object_or_404(BlogPost, id=post_id),
        'form': form,
        'comment_noun': noun
    }

    return render(
        request,
        "blogpost.html",
        context
    )
