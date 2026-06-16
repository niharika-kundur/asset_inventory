"""
Views for the assets app.

This module contains all view functions that handle HTTP requests
and return HTTP responses for the Asset Inventory Tool.
"""

import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Asset, AssetHistory
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone


def home(request):
    """Home page with welcome message."""
    return render(request, 'home.html')


@login_required
def asset_list(request):
    """Display all assets in a table with filtering options."""
    selected_status = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    date_filter_type = request.GET.get('date_filter', '')
    assigned_on = request.GET.get('assigned_on', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if request.user.is_superuser:
        base_assets = Asset.objects.all()
    else:
        base_assets = Asset.objects.filter(assigned_to=request.user.username)

    # Apply search filter
    if search_query:
        base_assets = base_assets.filter(asset_id__icontains=search_query)

    # Apply date filters
    if date_filter_type == 'on' and assigned_on:
        base_assets = base_assets.filter(assigned_date=assigned_on)
    elif date_filter_type == 'between' and date_from and date_to:
        base_assets = base_assets.filter(assigned_date__gte=date_from, assigned_date__lte=date_to)

    available_statuses = (
        base_assets.values_list('status', flat=True)
        .distinct()
        .order_by('status')
    )

    assets = base_assets
    if selected_status:
        assets = assets.filter(status=selected_status)

    return render(
        request,
        'asset_list.html',
        {
            'assets': assets,
            'available_statuses': available_statuses,
            'selected_status': selected_status,
            'search_query': search_query,
            'date_filter_type': date_filter_type,
            'assigned_on': assigned_on,
            'date_from': date_from,
            'date_to': date_to,
        }
    )

@login_required
def add_asset(request):
    """Simple form to add a new asset."""
    error_message = None
    if request.method == 'POST':
        asset_id = request.POST['asset_id']
        existing = Asset.objects.filter(asset_id=asset_id).first()
        if existing:
            error_message = f"Asset ID '{asset_id}' already exists and is assigned to {existing.assigned_to}."
        else:
            if request.user.is_superuser:
                assigned_to = request.POST['assigned_to']
            else:
                assigned_to = request.user.username

            # Create the asset
            asset = Asset.objects.create(
                asset_id=asset_id,
                asset_name=request.POST['asset_name'],
                asset_type=request.POST['asset_type'],
                assigned_to=assigned_to,
                status=request.POST['status'],
                assigned_date=timezone.now().date(),
            )

            # Create audit history record
            AssetHistory.objects.create(
                asset=asset,
                changed_by=request.user.username,
                change_type='Created',
                new_value=f"Assigned to {assigned_to}",
                notes=f"Asset created with status: {asset.status}"
            )

            messages.success(request, 'Asset added successfully!')
            return redirect('asset_list')
    users = User.objects.all()
    return render(request, 'add_asset.html', {'error_message': error_message, 'users': users})

@login_required
def delete_asset(request, asset_id):
    """Delete an asset - only superuser allowed."""
    if not request.user.is_superuser:
        return redirect('asset_list')
    asset = Asset.objects.get(id=asset_id)
    # Note: History is deleted with asset due to CASCADE
    asset.delete()
    messages.success(request, 'Asset deleted successfully!')
    return redirect('asset_list')

@login_required
def edit_asset(request, asset_id):
    """Transfer asset - only superuser allowed."""
    if not request.user.is_superuser:
        return redirect('asset_list')
    asset = Asset.objects.get(id=asset_id)

    if request.method == 'POST':
        old_assigned_to = asset.assigned_to
        old_status = asset.status
        new_assigned_to = request.POST['assigned_to']
        new_status = request.POST['status']

        # Track changes in history
        if old_assigned_to != new_assigned_to:
            AssetHistory.objects.create(
                asset=asset,
                changed_by=request.user.username,
                change_type='Transferred',
                field_changed='assigned_to',
                old_value=old_assigned_to,
                new_value=new_assigned_to,
                notes=f"Asset transferred from {old_assigned_to} to {new_assigned_to}"
            )
            # Update assigned_date when transferred
            asset.assigned_date = timezone.now().date()

        if old_status != new_status:
            AssetHistory.objects.create(
                asset=asset,
                changed_by=request.user.username,
                change_type='Updated',
                field_changed='status',
                old_value=old_status,
                new_value=new_status,
                notes=f"Status changed from {old_status} to {new_status}"
            )

        asset.assigned_to = new_assigned_to
        asset.status = new_status
        asset.save()
        messages.success(request, 'Asset updated successfully!')
        return redirect('asset_list')

    users = User.objects.all()
    return render(request, 'edit_asset.html', {'asset': asset, 'users': users})


@login_required
def asset_history(request, asset_id):
    """View audit history for an asset - only superuser allowed."""
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to view asset history.')
        return redirect('asset_list')

    asset = get_object_or_404(Asset, id=asset_id)
    history = asset.history.all()  # Uses related_name='history'

    return render(request, 'asset_history.html', {
        'asset': asset,
        'history': history,
    })


@login_required
def export_assets_csv(request):
    """Export assets to CSV file for download."""
    # Create response with CSV content type
    user_name = request.user.username
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user_name}_assets.csv"'

    # Create CSV writer
    writer = csv.writer(response)

    # Get field names dynamically from model (exclude 'id')
    field_names = [field.name for field in Asset._meta.fields if field.name != 'id']

    # Write header row (convert field names to Title Case)
    headers = [name.replace('_', ' ').title() for name in field_names]
    writer.writerow(headers)

    # Get assets based on user role
    if request.user.is_superuser:
        assets = Asset.objects.all()
    else:
        assets = Asset.objects.filter(assigned_to=user_name)

    # Write data rows dynamically
    for asset in assets:
        row = [getattr(asset, field) for field in field_names]
        writer.writerow(row)

    return response


