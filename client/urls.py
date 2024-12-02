from django.urls import path
from client.views import (  home,
                            ClientDeleteView, 
                            ClientListView, 
                            ClientDetailView,
                            ListClientByKeyword,
                            create_client,
                            update_client )

urlpatterns = [
    path("", home, name='index'),
    path("clients/", ClientListView.as_view(), name='client_list'),
    path("clients/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("clients/add/",  create_client, name='client_add'),
    path("clients/<int:pk>/update/", update_client, name='client_update'),
    path("clients/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
    path("clients/search/", ListClientByKeyword.as_view(), name="client_search"),

]