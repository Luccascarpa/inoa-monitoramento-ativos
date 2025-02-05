from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, get_resolver
from django.contrib import messages
from .models import Asset, PriceHistory, AlertEmails
from .forms import AssetForm, PriceHistoryFilterForm, AlertEmailsForm


def list_endpoints(request):
    resolver = get_resolver()
    urls = [f"/{url.pattern}" for url in resolver.url_patterns]

    return render(request, "monitoring/endpoints_list.html", {"urls": urls})

def asset_list(request):
    assets = Asset.objects.all()
    return render(request, 'monitoring/asset_list.html', {'assets': assets})

def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ativo criado com sucesso!")
            return redirect(reverse("asset_list"))
    else:
        form = AssetForm()  # Certifique-se de criar o formulário também para GET

    return render(request, 'monitoring/asset_form.html', {'form': form, 'title': 'Novo Ativo'})

def asset_edit(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, "Ativo atualizado com sucesso!")
            return redirect(reverse('asset_list'))
    else:
        form = AssetForm(instance=asset)
    return render(request, 'monitoring/asset_form.html', {'form': form, 'title': 'Editar Ativo'})

def asset_delete(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    asset.delete()
    messages.success(request, "Ativo removido com sucesso!")
    return redirect(reverse('asset_list'))

def price_history(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    filter_form = PriceHistoryFilterForm(request.GET or None)
    queryset = PriceHistory.objects.filter(asset=asset).order_by('-timestamp')

    if filter_form.is_valid():
        start_date = filter_form.cleaned_data['start_date']
        end_date = filter_form.changed_data['end_date']
        if start_date:
            queryset = queryset.filer(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filer(timestamp__lte=end_date)
    
    return render(request, 'monitoring/price_history.html', {
        'asset': asset,
        'price_history': queryset,
        'filter_form': filter_form
    })

def alert_emails_list(r):
    # List all emails
    emails = AlertEmails.objects.all()
    return render(r, 'monitoring/alert_emails_list.html', {'emails': emails})

def alert_emails_create(r):
    # Add new email to the alerts list
    if r.method == 'POST':
        form = AlertEmailsForm(r.POST)
        if form.is_valid():
            form.save()
            messages.success(r, 'E-mail adicionado!')
            return redirect(reverse("alert_emails_list"))
    else:
        form = AlertEmailsForm()

    return render(r, 'monitoring/alert_emails_form.html', {'form': form, 'title': 'Adicionar Email'})


def alert_email_delete(r, email_id):
    # Delete emils from the list
    recipient = AlertEmails.objects.get(id=email_id)
    recipient.delete()
    messages.success(r, "E-mail removido!")
    return redirect(reverse('alert_emails_list'))