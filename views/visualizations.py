from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from gedgo.models import Person
from datetime import datetime
from collections import defaultdict

from gedgo.current_history import HISTORY as HISTORICAL

import random
import json


def pedigree(request, gid, pid):
    person = get_object_or_404(Person, gedcom_id=gid, pointer=pid)
    n = _node(person, 0)
    n['gid'] = gid
    return HttpResponse(
        json.dumps(n),
        content_type="application/json"
    )


def _node(person, level):
    r = {}
    r['name'] = _truncate(person.full_name)
    r['span'] = '(%s)' % person.year_range
    r['id'] = person.pointer
    if (level < 2) and person.child_family:
        r['children'] = []
        if person.child_family.husbands.exists():
            for parent in person.child_family.husbands.iterator():
                r['children'].append(_node(parent, level + 1))
        if person.child_family.wives.exists():
            for parent in person.child_family.wives.iterator():
                r['children'].append(_node(parent, level + 1))
        while len(r['children']) < 2:
            if person.child_family.husbands.all():
                r['children'].append({'name': 'unknown', 'span': '', 'id': ''})
            else:
                r['children'] = [
                    {'name': 'unknown', 'span': '', 'id': ''}
                ] + r['children']
    return r


def _truncate(inp):
    return (inp[:25] + '..') if len(inp) > 27 else inp


def timeline(request, gid, pid):
    """
    TODO:
      - Clean up: flake8 and flow control improvements
      - Extend Historical Events to include 19th Century and before
      - Balance events so they don't crowd together
      - Comments
    """
    person = get_object_or_404(Person, gedcom_id=gid, pointer=pid)
    now = datetime.now().year

    # Don't show timelines for people without valid birth dates.
    if not valid_event_date(person.birth) or \
            (not valid_event_date(person.death) and
             (now - person.birth.date.year > 100)):
        return HttpResponse('{"events": []}', content_type="application/json")

    start_date = person.birth.date.year
    events = [
        {
            'text': 'born',
            'year': start_date,
            'type': 'personal'
        }
    ]

    if person.spousal_families.exists():
        for family in person.spousal_families.iterator():
            if valid_event_date(family.joined):
                events.append({
                    'text': 'married',
                    'year': family.joined.date.year,
                    'type': 'personal'
                })
            if valid_event_date(family.separated):
                events.append({
                    'text': 'divorced',
                    'year': family.separated.date.year,
                    'type': 'personal'
                })
            for child in family.children.iterator():
                if valid_event_date(child.birth):
                    events.append({
                        'text': child.full_name + " born",
                        'year': child.birth.date.year,
                        'type': 'personal'
                    })
                if valid_event_date(child.death):
                    if child.death.date < person.birth.date:
                        events.append({
                            'name': child.full_name + " died",
                            'year': child.death.date.year,
                            'type': 'personal'
                        })

    if not valid_event_date(person.death):
        end_date = now
        events.append({'text': 'now', 'year': now, 'type': 'personal'})
    else:
        end_date = person.death.date.year
        events.append({'text': 'died', 'year': end_date, 'type': 'personal'})

    # Don't show timelines for people with only birth & end_date.
    if len(events) < 3:
        return HttpResponse('{"events": []}', content_type="application/json")

    # open_years is an set of years where historical events may be added into
    # the timeline, to prevent overcrowding of items
    open_years = set(range(start_date + 1, end_date))
    for e in events:
        open_years -= set([e['year'] - 1, e['year'], e['year'] + 1])

    number_allowed = max(((end_date - start_date) / 3) + 2 - len(events), 5)

    historical_count = 0
    random.shuffle(HISTORICAL)
    for text, year in HISTORICAL:
        if historical_count > number_allowed:
            break
        if year not in open_years:
            continue
        events.append({'text': text, 'year': year, 'type': 'historical'})
        # Keep historical events three years apart to keep from crowding.
        open_years -= set([year - 1, year, year + 1])
        historical_count += 1

    response = {'start': start_date, 'end': end_date, 'events': events}
    return HttpResponse(json.dumps(response), content_type="application/json")


def valid_event_date(event):
    if event is not None:
        if event.date is not None:
            return True
    return False


def __gatherby(inlist, func):
    d = defaultdict(list)
    for item in inlist:
        d[func(item)].append(item)
    return d.values()

