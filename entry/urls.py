from django.urls import path
from entry.views import ( ListAllEntries,
                         ListEntriesByClient,
                         entries_by_date,
                         create_entry )

urlpatterns = [
    path("entries/", ListAllEntries.as_view(), name='entry_list'),
    path("entries/add/", create_entry, name="entry_add"),
    path('entries/by-client/<int:client_pk>/', ListEntriesByClient.as_view(), name='entries_by_client'),
    path('entries/by-date/', entries_by_date, name='entries_by_date'),

]