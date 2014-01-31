from django.db import models

from document import Document
from documentary import Documentary


class Family(models.Model):
    class Meta:
        app_label = 'gedgo'
    pointer = models.CharField(max_length=10, primary_key=True)
    gedcom = models.ForeignKey('Gedcom')
    husbands = models.ManyToManyField('Person', related_name='family_husbands')
    wives = models.ManyToManyField('Person', related_name='family_wives')
    children = models.ManyToManyField('Person', related_name='family_children')

    notes = models.ManyToManyField('Note', null=True)
    kind = models.CharField('Event', max_length=10, blank=True, null=True)

    joined = models.ForeignKey(
        'Event',
        related_name='family_joined',
        blank=True,
        null=True
    )
    separated = models.ForeignKey(
        'Event',
        related_name='family_separated',
        blank=True,
        null=True
    )

    def family_name(self):
        nm = ''
        for set in [self.husbands.all(), self.wives.all()]:
            for person in set:
                nm += ' / ' + person.last_name
        return nm.strip(' / ')

    def __unicode__(self):
        txt = self.family_name()
        return (txt + ' (' + self.pointer + ')')

    def single_child(self):
        if len(self.children.all()) == 1:
            return self.children.all()[0]

    def photos(self):
        return Document.objects.filter(tagged_families=self, kind='PHOTO')

    def documentaries(self):
        return Documentary.objects.filter(tagged_families=self)
