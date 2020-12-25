from django.contrib import admin
from .models import Cluster, Event, Case, PI, CaseQuestion

# Register your models here.
class EventInline(admin.TabularInline):
    model = Event

class ClusterAdmin(admin.ModelAdmin):
    inlines = [EventInline]

class PIInline(admin.TabularInline):
    model = PI

class CaseQuestionInline(admin.TabularInline):
    model = CaseQuestion
    max_num = 4

class CaseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Case Data', {'fields':['title', 'event','year', 'level']}),
        ('Description', {'fields': ['description']}),
    ]
    inlines = [PIInline, CaseQuestionInline]

admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Case, CaseAdmin)