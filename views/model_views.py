from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from gedgo.models import Gedcom, Person, BlogPost, Documentary
from gedgo.views.util import render, process_comments


def gedcom(request, gedcom_id):
    g = get_object_or_404(Gedcom, id=gedcom_id)
    post = BlogPost.objects.all().order_by("-created").first()

    noun = g.title or ("Gedcom #%d" % g.id)
    form, redirect = process_comments(request, noun)
    if redirect is not None:
        return redirect

    return render(
        request,
        'gedcom.html',
        {
            'gedcom': g,
            'post': post,
            'form': form,
            'comment_noun': noun
        }
    )


def person(request, gedcom_id, person_id):
    g = get_object_or_404(Gedcom, id=gedcom_id)
    p = get_object_or_404(Person, gedcom=g, pointer=person_id)

    noun = "%s (%s)" % (p.full_name, p.pointer)
    form, redirect = process_comments(request, noun)
    if redirect is not None:
        return redirect

    context = {
        'person': p,
        'posts': BlogPost.objects.filter(tagged_people=p),
        'gedcom': g,
        'form': form,
        'comment_noun': noun
    }

    return render(request, 'person.html', context)


def documentaries(request):
    documentaries = Documentary.objects.all().order_by('-last_updated')

    return render(
        request,
        "documentaries.html",
        {'documentaries': documentaries}
    )
