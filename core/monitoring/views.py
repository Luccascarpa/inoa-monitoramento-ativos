from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .models import Asset, PriceHistory
from .forms import AssetForm, PriceHistoryFilterForm

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
