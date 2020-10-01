from gedgo.models import Gedcom, Person
from django_datatables_view.base_datatable_view import BaseDatatableView
from gedgo.views.util import render
from django.db.models import Q
from django.utils.safestring import mark_safe
import json


def get_date(o):
    if not o or not o.date:
        return ''
    return o.date_string


def people_list(request):
    g = Gedcom.objects.first()
    search = request.GET.get('q', '')

    context = {
        'gedcom': g,
        'search_json': mark_safe(json.dumps(search)),
    }

    return render(
        request,
        'list.html',
        context
    )


class PeopleListJson(BaseDatatableView):
    model = Person
    columns = ["last_name", "first_name", "birth", "death", "pointer"]
    order_columns = ["last_name", "first_name", "birth.date", "death.date", "pointer"]
    max_display_length = 500

    def render_column(self, row, column):
        if column == 'birth':
            return get_date(row.birth)
        elif column == 'death':
            return get_date(row.death)
        else:
            return row.__dict__[column]

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        search = self.request.GET.get('search[value]', "")
        for term in search.split():
            qs = qs.filter(Q(last_name__icontains=term) | Q(first_name__icontains=term))

        return qs

