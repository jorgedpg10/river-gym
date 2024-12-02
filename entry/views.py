from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.utils.timezone import make_aware, now
from django.utils.dateparse import parse_datetime, parse_date

from .models import Client, Entry


class ListAllEntries(ListView):
    template_name='entry/all.html'
    paginate_by=7
    model=Entry
    context_object_name='entries'


def create_entry(request):
    if request.method == "POST":
        client_id = request.POST.get("client")  

        if not client_id:  
            error = "Debes seleccionar un cliente."
        else:
            try:
                client = Client.objects.get(id=client_id) 

                if 'manual' in request.POST:
                    hora = request.POST.get('hora')
                    if hora:
                        date_time = make_aware(parse_datetime(hora))  # Parse user-provided datetime
                    else:
                        error = "Debe ingresar una fecha y hora válida."
                        return render(request, "home.html", {"clients": Client.objects.all(), "error": error})
                else:
                    date_time = now() 

                Entry.objects.create(client=client, date_time=date_time)
                return redirect("entry_list")  

            except Client.DoesNotExist:
                error = "El cliente seleccionado no existe."

    return render(request, "home.html", {"clients": Client.objects.all(), "error": error if 'error' in locals() else None})

class ListEntriesByClient(ListView):
    template_name='entry/by_client.html'
    paginate_by=7
    context_object_name='entries'

    def get_queryset(self):
        client_pk = self.kwargs.get('client_pk')
        entries = Entry.objects.filter(client__pk=client_pk)
        return entries
    
    
def entries_by_date(request):
    error = None  
    entries = []  

    if request.method == "POST":
        input_date = request.POST.get("date") 
        print(input_date)
        parsed_date = parse_date(input_date)  

        if not parsed_date:  
            error = "No se ingresó una fecha válida."
        else:
            try:
                entries = Entry.objects.filter(date_time__date=parsed_date)
                if not entries.exists():
                    error = "No se encontraron entradas para la fecha seleccionada."
            except Exception as e:  
                error = f"Ocurrió un error al buscar las entradas: {str(e)}"

    return render(request, "entry/by_date.html", {"entries": entries, "date": parsed_date, "error": error})
