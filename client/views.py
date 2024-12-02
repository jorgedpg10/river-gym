from arrow import now
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, 
                                  DeleteView, 
                                  DetailView,
                                  TemplateView )
from django.db.models import Q

from entry.models import Entry

from .models import Client
from .forms import ClientForm

""" class IndexView(TemplateView):
    template_name = 'home.html'  """

def home(request):
    clients = Client.objects.all()   
    return render(request, "home.html", {"clients": clients})


class ClientListView(ListView):
    template_name='client/all.html'
    model = Client
    paginate_by=6
    context_object_name = "clients"


class ClientDetailView(DetailView):
    model = Client
    template_name = "client/detail.html"
    context_object_name = "client"


def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('client_list') 
    else:
        form = ClientForm()

    return render(request, 'client/add.html', {'form': form})

def update_client(request, pk):
    client = get_object_or_404(Client, pk=pk) 
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)  # Bind form to the client instance
        if form.is_valid():
            form.save()
            return redirect('client_list')  
    else:
        form = ClientForm(instance=client)  # Prepopulate the form with the client's data

    return render(request, 'client/update.html', {'form': form, 'client': client})

class ClientDeleteView(DeleteView):
    model = Client
    template_name = "client/delete.html"
    success_url = reverse_lazy("client_list") 


class ListClientByKeyword(ListView):
    template_name='client/list_by_keyword.html'
    context_object_name='clients'

    def get_queryset(self):
        keyword = self.request.GET.get("kword", '').strip()
        
        if keyword:
            clients = Client.objects.filter(
                Q(name__icontains=keyword) | Q(dni__icontains=keyword)
            )
        else:
            clients = Client.objects.none()
        
        return clients