from django.shortcuts import render,redirect, get_object_or_404 
from django.http import HttpResponse
from grnentry.models import Grnentry1,FormData, ProcessDetails,Delivery,Inventory,fields,material,Employee_info,calibration,master_component,Outsourse1,Notification,Supplier
import requests
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
import json
import http.client
from salesorder.models import salesorder
from apiitems.models import apiitems
from purchaseorders.models import apipurchaseorder
from django.utils import timezone
from .forms import DeliveryForm
from django.db.models import F, Sum
from django.conf import settings
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import logging
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from grnentry.models import fields
from django.urls import reverse
from .forms import GrnEntryForm,SupplierForm
from grnentry.models import LoginLog
from django.core.paginator import Paginator




#render template
def index(request):
   return render(request, 'index.html')
def grnentry(request):  
   return render(request,'grnentry.html')
def home(request):
    return render(request,'dashboard.html')      
def purchaseinfoshow(request):
    return render(request,'purchaseentryshow.html')
def maintracking(request):
    return render(request,'trackingmainpage.html')   
def trackingentry(request):
    return render(request,'trackingentry.html')
def salesorder1(request):
    return render(request,'salesorder.html')   
def purchaseorder1(request):
    return render(request,'purchaseorder1.html')
def trackentry(request):
    return render(request,'trackingentry.html') 
def inventory(request):
    return render(request,'inventory.html') 
def trackmainpage(request):
    return render(request,'trackingmainpage.html')
#materialinfo
def materialinfo(request):
    return render(request,'materialinfo.html')

def materialinfoform(request):
    return render(request,'materialinfoform.html')

def dashboard_view(request):
    # Query all ProcessDetails objects
    processes = ProcessDetails.objects.all()

    # Calculate total accepted and rejected quantities across all processes
    total_accepted = sum(process.acc_qty for process in processes)
    total_rejected = sum(process.rej_qty for process in processes)

    context = {
        'processes': processes,
        'total_accepted': total_accepted,
        'total_rejected': total_rejected,
    }

    return render(request, 'dashboard.html', context)
from django.shortcuts import get_object_or_404, redirect


def edit_employee(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee = get_object_or_404(Employee_info, id=employee_id)

        # Update fields
        employee.name = request.POST.get('name')
        employee.Designation = request.POST.get('Designation')
        employee.aadhar_no = request.POST.get('aadhar_no')
        employee.mobile_no = request.POST.get('mobile_no')
        employee.save()

        return redirect(showemployee)  # Replace 'employee_list' with your employee list view
from grnentry.models import Employee_info

def delete_employee(request, employee_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employee_info, id=employee_id)
        employee.delete()
        messages.success(request, 'Employee deleted successfully.')
        return redirect(showemployee)
    

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Log successful login attempt
            log_entry = LoginLog(user=user,
                                 ip_address=request.META.get('REMOTE_ADDR'),
                                 user_agent=request.META.get('HTTP_USER_AGENT'))
            log_entry.save()

            # Redirect to dashboard or a success page
            return redirect(home)
        else:
            # Invalid login attempt
            messages.error(request, 'Invalid username or password.')

    # Render the login form
    return render(request, 'login.html')
def dashboard_page(request):
    # Add logic for rendering the dashboard template
    return redirect(dashboard)
#outsourse
def outsourse(request):
    return render(request,'outsourse.html')

def outsourseform(request):
    if request.method == 'POST':
        grnno = request.POST.get('grnno')
        supplier_name = request.POST.get('supplier_name')
        supplier_process_name = request.POST.get('supplier_process_name')
        operation_name = request.POST.get('operation_name')
        part_desc = request.POST.get('part_desc')
        quantity = request.POST.get('quantity')
        out_date = request.POST.get('out_date')
        rate = request.POST.get('rate')

        en = Outsourse1(
            grnno=grnno,
            supplier_name=supplier_name,
            supplier_process_name=supplier_process_name,
            operation_name=operation_name,
            part_desc=part_desc,
            quantity=quantity,
            out_date=out_date,
            rate=rate
        )
        en.save()

        return redirect('showoutsourse')  # Ensure this name matches your URL pattern name
    return redirect('showoutsourse')

from django.shortcuts import get_object_or_404
@csrf_exempt
@csrf_exempt
def save_completion(request, entry_id):
    entry = get_object_or_404(Outsourse1, pk=entry_id)
    
    if request.method == 'POST':
        accepted_qty = request.POST.get('accepted_qty')
        rejected_qty = request.POST.get('rejected_qty')
        completion_date = request.POST.get('completion_date')

        if accepted_qty and rejected_qty and completion_date:
            entry.accepted_qty = int(accepted_qty)
            entry.rejected_qty = int(rejected_qty)
            entry.receive_date = completion_date
            entry.status = 'complete'
            entry.completed_time = timezone.now()
            entry.save()

            return redirect('showoutsourse')
        else:
            return JsonResponse({'error': 'All fields are required.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
def showoutsourse(request):
    out = Outsourse1.objects.all()
    suppliers = Supplier.objects.all()  # Use the correct class name
    for obj in out:
        print(obj.grnno)
    return render(request, 'outsourse.html', {'outsourse': out,'suppliers':suppliers})

def get_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'outsourse.html', {'suppliers': suppliers})

def save_supplier(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        # Check if supplier already exists
        if Supplier.objects.filter(name=name).exists():
            return JsonResponse({'success': False, 'error': 'Supplier already exists.'})

        # Create a new supplier
        new_supplier = Supplier.objects.create(name=name)

        # Return JSON response with the new supplier details
        return JsonResponse({'success': True, 'id': new_supplier.id, 'name': new_supplier.name})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
#dispatch 
def dispatch_details12(request, entry_id):
    if request.method == 'POST':
        form = DeliveryForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.form_data = FormData.objects.get(id=entry_id)
            form_data.dispatch_time = timezone.now()
            form_data.save()

            # Update the status of the associated entry based on form completion
            entry = FormData.objects.get(id=entry_id)
            if entry.order_status == 'Completed':
                entry.order_status = 'Delivered'
            else:
                entry.order_status = 'Completed'
            entry.save()

            return redirect('display_form_data')  # Redirect to a success page
    else:
        form = DeliveryForm()

    return render(request, 'dashboard.html', {'form': form})
from django.db import models, IntegrityError 
from django.contrib import messages
from urllib.parse import urlencode
def dispatch_details1(request, entry_id):
    form_data = get_object_or_404(FormData, id=entry_id)
    grn_entry = form_data.grn_entry

    if request.method == 'POST':
        form = DeliveryForm(request.POST, request.FILES)
        if form.is_valid():
            delivery = form.save(commit=False)
            delivery.form_data = form_data
            delivery.dispatch_time = timezone.now()
            
            remaining_quantity = get_remaining_quantity(form_data)
            if delivery.TTL_QNT_DISPATCH > remaining_quantity:
                messages.error(request, "Dispatched quantity exceeds available quantity.")
                return redirect('dispatch_details', entry_id=entry_id)
            
            delivery.save()

            # Update order status
            update_order_status(form_data)

            messages.success(request, 'Delivery details saved successfully.')
            return redirect('display_form_data')
    else:
        form = DeliveryForm()

    remaining_quantity = get_remaining_quantity(form_data)
    total_dispatched = get_total_dispatched(form_data)
    initial_quantity = form_data.grn_entry.grnentry_NOQUANTITY

    query_params = urlencode({
        'entry_id': entry_id,
        'remaining_quantity': remaining_quantity,
        'total_dispatched': total_dispatched,
        'initial_quantity': initial_quantity
    })
    url = reverse('grninfo') + '?' + query_params
    return redirect(url)

def update_order_status(form_data):
    total_dispatched = get_total_dispatched(form_data)
    initial_quantity = form_data.grn_entry.grnentry_NOQUANTITY

    if total_dispatched == initial_quantity:
        form_data.order_status = 'Delivered'
    else:
        form_data.order_status = 'Completed'

    form_data.save()

def get_remaining_quantity(form_data):
    total_dispatched = get_total_dispatched(form_data)
    initial_quantity = form_data.grn_entry.grnentry_NOQUANTITY
    return max(0, initial_quantity - total_dispatched)

def get_total_dispatched(form_data):
    return Delivery.objects.filter(form_data=form_data).aggregate(total=Sum('TTL_QNT_DISPATCH'))['total'] or 0

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now  # Import Django's timezone utility

#trackingentry

def form_view1(request, entry_id):
    grn_entry = get_object_or_404(Grnentry1, id=entry_id)

    if request.method == 'POST':
        try:
            vendor_name = request.POST.get('vendor_name')
            exptime = request.POST.get('exptime')
            quantitycheck = request.POST.get('quantitycheck')
            image = request.FILES.get('image')
            report = request.POST.get('report')

            form_data = FormData.objects.create(
                grn_entry=grn_entry,
                vendor_name=vendor_name,
                exptime=exptime,
                quantitycheck=quantitycheck,
                image=image,
                report=report
            )

            # Process static fields
            process_static = request.POST.getlist(f'process_static_{entry_id}[]')
            description_static = request.POST.getlist(f'description_static_{entry_id}[]')
            start_date_static = request.POST.getlist(f'start_date_static_{entry_id}[]')
            end_date_static = request.POST.getlist(f'end_date_static_{entry_id}[]')
            quantity_static = request.POST.getlist(f'quantity_static_{entry_id}[]')

            for process, description, start_date, end_date, quantity in zip(process_static, description_static, start_date_static, end_date_static, quantity_static):
                ProcessDetails.objects.create(
                    form_data=form_data,
                    grn_entry=grn_entry,
                    process=process,
                    description=description,
                    start_date=start_date,
                    end_date=end_date,
                    quantity=quantity
                )

            # Process dynamic fields
            process_dynamic = request.POST.getlist(f'process_dynamic_{entry_id}[]')
            description_dynamic = request.POST.getlist(f'description_dynamic_{entry_id}[]')
            start_date_dynamic = request.POST.getlist(f'start_date_dynamic_{entry_id}[]')
            end_date_dynamic = request.POST.getlist(f'end_date_dynamic_{entry_id}[]')
            quantity_dynamic = request.POST.getlist(f'quantity_dynamic_{entry_id}[]')

            for process, description, start_date, end_date, quantity in zip(process_dynamic, description_dynamic, start_date_dynamic, end_date_dynamic, quantity_dynamic):
                ProcessDetails.objects.create(
                    form_data=form_data,
                    grn_entry=grn_entry,
                    process=process,
                    description=description,
                    start_date=start_date,
                    end_date=end_date,
                    quantity=quantity
                )

            grn_entry.status = 'Completed'
            grn_entry.save()

            return redirect('display_form_data')

        except Exception as e:
            # Log the exception for debugging purposes
            logger.error(f"Error saving form data: {e}")
            return HttpResponseBadRequest("Error saving form data. Please try again.")

def form_view(request, entry_id):
    grn_entry = get_object_or_404(Grnentry1, id=entry_id)
    if request.method == 'POST':
        vendor_name = request.POST.get('vendor_name')

        form_data = FormData.objects.create(
            grn_entry=grn_entry,
            vendor_name=vendor_name,
        )

        process_details = request.POST.getlist('inputField[]')
        for i in range(0, len(process_details), 5):
            process = process_details[i]
            description = process_details[i + 1]
            start_date = process_details[i + 2]
            end_date = process_details[i + 3]
            quantity = int(process_details[i + 4])

            ProcessDetails.objects.create(
                grn_entry=grn_entry,
                form_data=form_data,
                process=process,
                description=description,
                start_date=start_date,
                end_date=end_date,
                quantity=quantity
            )
        grn_entry.status = 'Completed'
        grn_entry.save()
        # Update grnentry_DATETIME if needed
        if not grn_entry.grnentry_DATETIME:
            grn_entry.grnentry_DATETIME = now()  # or use appropriate datetime value
            grn_entry.save()

        return redirect(display_form_data)

    return render(request, 'formdynamics/form.html', {'grn_entry': grn_entry})

def tracking_entry_view(request, entry_id):
    grn_entry = get_object_or_404(Grnentry1, id=entry_id)
    return render(request, 'trackingentry.html', {'grn_entry': grn_entry})



def display_entry_details(request, entry_id):
    entry = get_object_or_404(FormData, pk=entry_id)
    process_details = entry.processdetails_set.all()
    last_completed = None
    upcoming_process_details = []

    # Calculate the total number of processes and completed processes
    total_processes = process_details.count()
    completed_processes = process_details.filter(completed=True).count()

    # Calculate the percentage of work done
    if total_processes > 0:
        work_done_percentage = (completed_processes / total_processes) * 100
    else:
        work_done_percentage = 0

    # Separate completed and upcoming processes
    for process_detail in process_details:
        if process_detail.completed:
            last_completed = process_detail
        else:
            upcoming_process_details.append(process_detail)

    if request.method == 'POST':
        process_id = request.POST.get('process_id')
        process = ProcessDetails.objects.get(pk=process_id)
        
        # Update ProcessDetails instance with accepted_qty and rejected_qty
        accepted_qty = request.POST.get('accepted_qty')
        rejected_qty = request.POST.get('rejected_qty')
        
        process.acc_qty = accepted_qty
        process.rej_qty = rejected_qty
        
        process.completed = True
        process.completed_time = timezone.now()
        process.save()
        entry.update_order_status()
        # Update rejected quantity total for FormData
        entry.update_ttl_rejected_qty()
        entry.update_ttl_accepted_qty()

        return redirect('display_entry_details', entry_id=entry_id)

    return render(request, 'entry_details.html', {
        'entry': entry,
        'last_completed': last_completed,
        'upcoming_process_details': upcoming_process_details,
        'total_processes': total_processes,
        'completed_processes': completed_processes,
        'work_done_percentage': work_done_percentage
    })
def display_form_data(request):
    form_data = FormData.objects.all().order_by('-id')
    Delivery1=Delivery.objects.all().order_by('-id')
    return render(request, 'form_data_list.html', {'form_data': form_data,'Delivery1':Delivery1})

#grnentry   
def grninfo(request):
    field_list = fields.objects.all()
    grninfo = Grnentry1.objects.all().order_by('-id')
    error = request.GET.get('error', '')  # Retrieve the error message from query parameters
    for elements in grninfo:
        print(elements.grnentry_QUANTITYTYPE)
    return render(request, 'grnmainpage.html', {'grn': grninfo, 'error': error,'col': field_list})

def savegrndata1(request):
   
   if request.method== "POST":
      GRNNO=request.POST.get('GRNNO')
      MATERIALDESCRIPTION=request.POST.get('MATERIALDESCRIPTION')
      MATERIALGRADE=request.POST.get('MATERIALGRADE')
      QUANTITYTYPE=request.POST.get('QUANTITYTYPE')
      NOQUANTITY=request.POST.get('NOQUANTITY')
      STOREOWNER=request.POST.get('STOREOWNER')
      ORDERTYPE=request.POST.get('ORDERTYPE')
      PONO=request.POST.get('PONO')
      CHALLANNO=request.POST.get('CHALLANNO')
      COMMENTS=request.POST.get('COMMENTS')
      SONO=request.POST.get('SONO')
      PARTNAME=request.POST.get('PARTNAME')
      DRAWINGNO=request.POST.get('DRAWINGNO')
      EXPTIME=request.POST.get('EXPTIME')
      FILE=request.get.FILES('FILES')
      en= Grnentry1(grnentry_GRNNO=GRNNO,grnentry_MATERIALDESCRIPTION=MATERIALDESCRIPTION,grnentry_MATERIALGRADE=MATERIALGRADE,grnentry_QUANTITYTYPE=QUANTITYTYPE,grnentry_NOQUANTITY=NOQUANTITY,grnentry_ORDERTYPE=ORDERTYPE,grnentry_STOREOWNER=STOREOWNER,grnentry_PONO=PONO,grnentry_CHALLANNO=CHALLANNO,grnentry_COMMENTS=COMMENTS,grnentry_SONO=SONO,grnentry_PARTNAME=PARTNAME,grnentry_DRAWINGNO=DRAWINGNO,grnentry_EXPTIME=EXPTIME,FILE=FILE)
      en.save()
   return redirect(grninfo)

def serve_pdf(request, file_path):
    # Construct the absolute file path
    pdf_path = os.path.join(settings.MEDIA_ROOT, file_path)

    try:
        # Open the PDF file for reading
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(pdf_path)}"'
            return response
    except FileNotFoundError:
        return HttpResponse('PDF file not found', status=404)

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import urllib.parse

def edit_grnentry(request, pk):
    cal = get_object_or_404(Grnentry1, pk=pk)
    
    if request.method == 'POST':
        # Update the existing Grnentry1 object with data from the form
        cal.grnentry_GRNNO = request.POST.get('edit_grnentry_GRNNO')
        cal.grnentry_MATERIALDESCRIPTION = request.POST.get('grnentry_MATERIALDESCRIPTION')
        cal.grnentry_MATERIALGRADE = request.POST.get('grnentry_MATERIALGRADE')
        cal.grnentry_QUANTITYTYPE = request.POST.get('grnentry_QUANTITYTYPE')
        cal.grnentry_NOQUANTITY = request.POST.get('grnentry_NOQUANTITY')
        cal.grnentry_STOREOWNER = request.POST.get('grnentry_STOREOWNER')
        cal.grnentry_ORDERTYPE = request.POST.get('grnentry_ORDERTYPE')
        cal.grnentry_PONO = request.POST.get('grnentry_PONO')
        cal.grnentry_CHALLANNO = request.POST.get('grnentry_CHALLANNO')
        cal.grnentry_COMMENTS = request.POST.get('grnentry_COMMENTS')
        cal.grnentry_SONO = request.POST.get('grnentry_SONO')
        cal.grnentry_PARTNAME = request.POST.get('grnentry_PARTNAME')
        cal.grnentry_DRAWINGNO = request.POST.get('grnentry_DRAWINGNO')
        cal.REVISIONNO = request.POST.get('REVISIONNO')
        
        cal.customername = request.POST.get('customername')

        # Only update FILE if a new file is provided
        if 'FILE' in request.FILES:
            cal.FILE = request.FILES['FILE']

        try:
            cal.save()
            # Redirect to the 'grninfo' view to display updated data
            return redirect(reverse('grninfo', args=[cal.pk]))  # Redirect to grninfo view with the updated cal pk
        except Exception as e:
            print(f"Error saving entry: {e}")
            # Redirect to 'grninfo' view with the error message as a query parameter
            error_message = urllib.parse.quote(str(e))  # URL encode the error message
            redirect_url = f"{reverse('grninfo')}?error={error_message}"
            return redirect(redirect_url)
    
    
    # If it's a GET request, just display the edit form
    return render(request, 'grnentrymain.html', {'cal': cal})

@csrf_exempt
def savegrndata(request):
    if request.method == "POST":
        GRNNO = request.POST.get('GRNNO')
        MATERIALDESCRIPTION = request.POST.get('MATERIALDESCRIPTION')
        MATERIALGRADE = request.POST.get('MATERIALGRADE')
        QUANTITYTYPE = request.POST.get('grnentry_QUANTITYTYPE')
        NOQUANTITY = request.POST.get('NOQUANTITY')
        STOREOWNER = request.POST.get('grnentry_STOREOWNER')
        ORDERTYPE = request.POST.get('grnentry_ORDERTYPE')
        PONO = request.POST.get('PONO')
        CHALLANNO = request.POST.get('CHALLANNO')
        COMMENTS = request.POST.get('COMMENTS')
        SONO = request.POST.get('SONO')
        PARTNAME = request.POST.get('PARTNAME')
        DRAWINGNO = request.POST.get('DRAWINGNO')
        REVISIONNO = request.POST.get('REVISIONNO')
        EXPTIME = request.POST.get('EXPTIME')
        FILE = request.FILES.get('FILE')  
        customername=request.POST.get('customername')# Correct field name

        # Create an instance of your model and save it
        grn_entry = Grnentry1(
            grnentry_GRNNO=GRNNO,
            grnentry_MATERIALDESCRIPTION=MATERIALDESCRIPTION,
            grnentry_MATERIALGRADE=MATERIALGRADE,
            grnentry_QUANTITYTYPE=QUANTITYTYPE,
            grnentry_NOQUANTITY=NOQUANTITY,
            grnentry_STOREOWNER=STOREOWNER,
            grnentry_ORDERTYPE=ORDERTYPE,
            grnentry_PONO=PONO,
            grnentry_CHALLANNO=CHALLANNO,
            grnentry_COMMENTS=COMMENTS,
            grnentry_SONO=SONO,
            grnentry_PARTNAME=PARTNAME,
            grnentry_DRAWINGNO=DRAWINGNO,
            REVISIONNO=REVISIONNO,
            grnentry_EXPTIME=EXPTIME,
            FILE=FILE,customername=customername
        )
        grn_entry.save()

    return redirect(grninfo)

#fields
def field(request):
    field_list = fields.objects.all()
    return render(request, 'grnmainpage.html', {'col': field_list})

def save_field(request):
    if request.method == 'POST':
        field_name = request.POST.get('field')
        if fields.objects.filter(field=field_name).exists():
            return JsonResponse({'success': False, 'error': 'Field already exists.'})
        else:
            new_field = fields.objects.create(field=field_name)
            redirect_url = reverse('grninfo')  # Assuming 'grninfo' is the name of the view
            return JsonResponse({'success': True, 'redirect_url': redirect_url})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
#employee

def saveemployee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Designation = request.POST.get('Designation')
        aadhar_no = request.POST.get('aadhar_no')
        mobile_no = request.POST.get('mobile_no')

        EN=Employee_info(name=name, Designation=Designation, aadhar_no=aadhar_no, mobile_no=mobile_no)
        EN.save()

    return redirect(showemployee)

def showemployee(request):
    employees = Employee_info.objects.all()
    return render(request, 'Employees.html', {'employees': employees})

def update_employee(request, employee_id):
    if request.method == 'POST':
        employee = Employee_info.objects.get(id=employee_id)
        employee.name = request.POST.get('name')
        employee.Designation = request.POST.get('Designation')
        employee.aadhar_no = request.POST.get('aadhar_no')
        employee.mobile_no = request.POST.get('mobile_no')
        employee.save()
        return redirect(showemployee)
    else:
        employee = Employee_info.objects.get(id=employee_id)
        return render(request, 'Employee.html', {'employee': employee})

#instruction calibration
def instruction_calibration(request):
    return render(request, 'instruction_calibration.html')

def ins_cal_form(request):
    if request.method == 'POST':
        # Get data from the form
        inst_name = request.POST.get('inst_name')
        make = request.POST.get('make')
        least_count = request.POST.get('least_count')
        least_count_unit = request.POST.get('least_count_unit')
        least_range = request.POST.get('least_range')
        max_range = request.POST.get('max_range')
        range_unit = request.POST.get('range_unit')
        location = request.POST.get('location')
        calibrated_date = request.POST.get('calibrated_date')
        next_calibration_due_date = request.POST.get('next_calibration_due_date')
        remark = request.POST.get('remark')
        # Create a new calibration object
        en = calibration(
            inst_name=inst_name, make=make, least_count=least_count, least_count_unit=least_count_unit,
            least_range=least_range, max_range=max_range, range_unit=range_unit, location=location,
            calibrated_date=calibrated_date, next_calibration_due_date=next_calibration_due_date, remark=remark
        )
        en.save()
        # Redirect to show_ins_cal view
        return redirect(show_ins_cal)
    return render(request, 'instruction_calibration.html')

def update_cal(request, pk):
    cal = get_object_or_404(calibration, pk=pk)
    if request.method == 'POST':
        # Update the existing calibration object
        cal.inst_name = request.POST.get('inst_name')
        cal.make = request.POST.get('make')
        cal.least_count = request.POST.get('least_count')
        cal.least_count_unit = request.POST.get('least_count_unit')
        cal.least_range = request.POST.get('least_range')
        cal.max_range = request.POST.get('max_range')
        cal.range_unit = request.POST.get('range_unit')
        cal.location = request.POST.get('location')
        cal.calibrated_date = request.POST.get('calibrated_date')
        cal.next_calibration_due_date = request.POST.get('next_calibration_due_date')
        cal.remark = request.POST.get('remark')
        cal.save()
        # Redirect to show_ins_cal view
        return redirect(show_ins_cal)
    return render(request, 'instruction_calibration.html', {'cal': cal})

def show_ins_cal(request):
    # Retrieve all calibration objects
    ins_cal = calibration.objects.all()
    return render(request, 'instruction_calibration.html', {'cal': ins_cal})


#master omponent
def master_component_form(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        drawing_no = request.POST.get('drawing_no')
        revision_no = request.POST.get('revision_no')
        drawing_pdf = request.FILES.get('drawing_pdf')  # Correct field name
        
        en = master_component(description=description, drawing_no=drawing_no, revision_no=revision_no, drawing_pdf=drawing_pdf)
        en.save()
    return redirect(show_master_component)

def show_master_component(request):
    components=master_component.objects.all()
    for component in components:
        print(component.description)
    return render(request,'master_component.html',{'components':components})    

def update_master_component(request, component_id):
    component = get_object_or_404(master_component, id=component_id)
    if request.method == 'POST':
        component.description = request.POST.get('description')
        component.drawing_no = request.POST.get('drawing_no')
        component.revision_no = request.POST.get('revision_no')
        if request.FILES.get('drawing_pdf'):
           component.drawing_pdf = request.FILES.get('drawing_pdf')
        component.save()
        return redirect(show_master_component)
    return render(request, 'master_component.html', {'component': component})


from grnentry.models import material
#material
def mark_complete(request, pk):
    material = get_object_or_404(Outsourse1, pk=pk)
    material.status = 'complete'
    material.completed_time = timezone.now()
    material.save()
    return redirect('showoutsourse'),


def display_material(request):
    materials = material.objects.exclude(DRAWING_PDF__exact='')  # Exclude materials where DRAWING_PDF is empty
    return render(request, 'materialinfo.html', {'materials': materials})

def savematerial(request):
    if request.method == 'POST':
        part_description = request.POST.get('part_description')
        DRAW_NO = request.POST.get('DRAW_NO')
        Material_Grade = request.POST.get('Material_Grade')
        Finish_size = request.POST.get('Finish_size')
        Raw_material_size = request.POST.get('Raw_material_size')
        order_size = request.POST.get('order_size')
        DRAWING_PDF = request.FILES.get('DRAWING_PDF')  # Get uploaded file

        # Create material instance and save
        en = material(part_description=part_description,
                      DRAW_NO=DRAW_NO,
                      Material_Grade=Material_Grade,
                      Finish_size=Finish_size,
                      Raw_material_size=Raw_material_size,
                      order_size=order_size,
                      DRAWING_PDF=DRAWING_PDF)
        en.save()

        return redirect('display_material')  # Replace with your actual view name
    else:
        # Handle GET request or initial form display
        return render(request, 'your_template.html') 
    
def get_material(request):
    material_id = request.GET.get('id')
    material_obj = get_object_or_404(material, id=material_id)
    data = {
        'id': material_obj.id,
        'part_description': material_obj.part_description,
        'DRAW_NO': material_obj.DRAW_NO,
        'Material_Grade': material_obj.Material_Grade,
        'Finish_size': material_obj.Finish_size,
        'Raw_material_size': material_obj.Raw_material_size,
        'order_size': material_obj.order_size,
        'DRAWING_PDF': material_obj.DRAWING_PDF.url if material_obj.DRAWING_PDF else '',  # Ensure you handle if PDF is None
    }
    return JsonResponse(data)

def edit_material(request):
    if request.method == 'POST':
        material_id = request.POST.get('material_id')
        material_obj = get_object_or_404(material, id=material_id)
        material_obj.part_description = request.POST.get('part_description')
        material_obj.DRAW_NO = request.POST.get('DRAW_NO')
        material_obj.Material_Grade = request.POST.get('Material_Grade')
        material_obj.Finish_size = request.POST.get('Finish_size')
        material_obj.Raw_material_size = request.POST.get('Raw_material_size')
        material_obj.order_size = request.POST.get('order_size')
        if request.FILES.get('DRAWING_PDF'):
            material_obj.DRAWING_PDF = request.FILES['DRAWING_PDF']
        material_obj.save()
        return HttpResponse('Material updated successfully!')
    else:
        return HttpResponse('Invalid request method')

#inventory
def calculate_remaining_units():
    # Get all FormData objects
    form_data_list = FormData.objects.all()

    # Calculate remaining units for each FormData object
    for form_data in form_data_list:
        # Get the total quantity from the related Grnentry1 object
        total_quantity = form_data.grn_entry.grnentry_NOQUANTITY

        # Calculate total quantity dispatched
        total_dispatched_quantity = Delivery.objects.filter(form_data=form_data).aggregate(total=Sum('TTL_QNT_DISPATCH'))['total'] or 0

        # Calculate remaining units
        remaining_units = total_quantity - total_dispatched_quantity

        # Save remaining units to Inventory model
        inventory, created = Inventory.objects.get_or_create(form_data=form_data)
        inventory.remaining_quantity = remaining_units
        inventory.save()

from django.db.models import Sum

def inventory_view(request):
    # Query all FormData objects ordered by dispatch time
    form_data_list = FormData.objects.all().order_by('-dispatch_time')

    # Initialize dictionaries to store inventory data
    pending_inventory_data = {}
    completed_inventory_data = {}

    # Iterate through each FormData object
    for form_data in form_data_list:
        # Calculate total dispatched quantity for the current FormData object
        total_dispatched_quantity = form_data.delivery_set.aggregate(total_dispatched=Sum('TTL_QNT_DISPATCH'))['total_dispatched'] or 0

        # Get the total quantity from the related Grnentry1 object
        total_quantity = form_data.grn_entry.grnentry_NOQUANTITY

        # Calculate remaining units
        remaining_units = total_quantity - total_dispatched_quantity

        # Get the part name, drawing number, and material grade
        part_name = form_data.grn_entry.grnentry_PARTNAME
        drawing_no = form_data.grn_entry.grnentry_DRAWINGNO
        material_grade = form_data.grn_entry.grnentry_MATERIALGRADE

        # Determine order status
        order_status = form_data.order_status

        # Create a key for the dictionary based on the drawing number
        key = drawing_no

        # Retrieve the part costs from the associated Delivery objects
        part_costs = form_data.delivery_set.values_list('PARTCOST', flat=True)
        unique_part_costs = {int(cost) for cost in part_costs}  # Convert to int and ensure uniqueness

        # Determine if the FormData is pending or completed
        if order_status == 'Pending':
            if key in pending_inventory_data:
                pending_inventory_data[key]['remaining_quantity'] += remaining_units
                pending_inventory_data[key]['part_costs'].update(unique_part_costs)
            else:
                pending_inventory_data[key] = {
                    'part_name': part_name,
                    'drawing_no': drawing_no,
                    'material_grade': material_grade,
                    'remaining_quantity': remaining_units,
                    'part_costs': unique_part_costs,
                    'order_status': order_status
                }
        else:
            if key in completed_inventory_data:
                completed_inventory_data[key]['remaining_quantity'] += remaining_units
                completed_inventory_data[key]['part_costs'].update(unique_part_costs)
            else:
                completed_inventory_data[key] = {
                    'part_name': part_name,
                    'drawing_no': drawing_no,
                    'material_grade': material_grade,
                    'remaining_quantity': remaining_units,
                    'part_costs': unique_part_costs,
                    'order_status': order_status
                }

    # Convert sets back to lists for rendering
    for key in pending_inventory_data:
        pending_inventory_data[key]['part_costs'] = list(pending_inventory_data[key]['part_costs'])
    for key in completed_inventory_data:
        completed_inventory_data[key]['part_costs'] = list(completed_inventory_data[key]['part_costs'])

    # Calculate total remaining quantities for pending and completed inventory
    total_pending_quantity = sum(item['remaining_quantity'] for item in pending_inventory_data.values())
    total_completed_quantity = sum(item['remaining_quantity'] for item in completed_inventory_data.values())

    # Render the inventory template with the merged inventory data and pie chart data
    return render(request, 'inventory.html', {
        'pending_inventory_list': pending_inventory_data.values(),
        'completed_inventory_list': completed_inventory_data.values(),
        'total_pending_quantity': total_pending_quantity,
        'total_completed_quantity': total_completed_quantity
    })

#notification

from django.utils import timezone
from datetime import timedelta

def generate_notifications():
    now = timezone.now()
    due_date = now + timedelta(days=2)
    calibrations_due_soon = calibration.objects.filter(next_calibration_due_date__lte=due_date, next_calibration_due_date__gt=now)

    for calibration in calibrations_due_soon:
        message = f"Calibration due for {calibration.inst_name} on {calibration.next_calibration_due_date.strftime('%Y-%m-%d')}"
        Notification.objects.create(message=message, calibration=calibration)

def get_notifications(request):
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})        

'''
def apicall_items(request):
    access_token = "1000.10842b324091f265854f6ad694586a56.d0d58b87dcf1c7dd8ea867e25a6fd36c"
    api_key = "ae530111a097e271b8c051b25b3b59c7"
    url = "https://www.zohoapis.in/books/v3/items?organization_id=60004755614"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Api-Key": api_key,
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
          salesorders = data["items"]
       
        for apiitems_data in salesorders:
                # Your code to handle each salesorder
            
            apiitems.objects.create(
                item_id=apiitems_data["item_id"],
                name=apiitems_data["name"],
                status=apiitems_data['item_name'],
                unit=apiitems_data['unit'],
                status=apiitems_data["status"],
                source=apiitems_data["source"],
                is_linked_with_zohocrm=apiitems_data["is_linked_with_zohocrm"],
                  zcrm_product_id=apiitems_data["zcrm_product_id"],
                  description=apiitems_data["description"],
                  rate=apiitems_data["rate"],
                  tax_id=apiitems_data["tax_id"],
                  item_tax_preferences_tax_specification=apiitems_data["item_tax_preferences"],
                  item_tax_preferences_tax_name_formatted=apiitems_data[],
                  item_tax_preferences_tax_type=apiitems_data[],
                  item_tax_preferences_tax_name=apiitems_data[],
                  item_tax_preferences_tax_percentage=apiitems_data[],
                  item_tax_preferences_tax_id=apiitems_data[],
                  item_tax_preferences_tax_specification2=apiitems_data[],
                  item_tax_preferences_tax_name_formatted2=apiitems_data[],
                  item_tax_preferences_tax_type2=apiitems_data[],
                  item_tax_preferences_tax_name2=apiitems_data[],
                  item_tax_preferences_tax_percentage2=apiitems_data[],
                  item_tax_preferences_tax_id2=apiitems_data[],
                  tax_name=apiitems_data[],
                  tax_percentage=apiitems_data[],
                  purchase_account_id=apiitems_data[],
                  purchase_account_name=apiitems_data[],
                  account_id=apiitems_data[],
                  account_name=apiitems_data[],
                  purchase_description=apiitems_data[],
                  purchase_rate=apiitems_data[],
                  item_type=apiitems_data[],
                  product_type=apiitems_data[],
                  is_taxable=apiitems_data[],
                  tax_exemption_id=apiitems_data[],
                  tax_exemption_code=apiitems_data[],
                  has_attachment=apiitems_data[],
                  sku=apiitems_data[],
                  image_name=apiitems_data[],
                  image_type=apiitems_data[],
                  image_document_id=apiitems_data[],
                  created_time=apiitems_data[],
                  last_modified_time=apiitems_data[],
                  hsn_or_sac=apiitems_data[],
                  cf_design_hours=apiitems_data[],
                  cf_design_hours_unformatted=apiitems_data[]
                print("saved")
            return JsonResponse({"message": "Data saved successfully."})
            )
        
    else:
        error_data = {
            "error": f"Error: {response.status_code}",
            "error_message": response.text,
        }
        return JsonResponse(error_data, status=response.status_code) 
'''
#function for salesorder for api
def apicall_salesorder(request):
    token = "1000.de2dbd5217619fc816b1f608078e4902.7df2bbaa1f90bb99bb199ff14d8b0adaf"
    api_key = "ae530111a097e271b8c051b25b3b59c7"
    url = "https://www.zohoapis.in/books/v3/salesorders?organization_id=60004755614"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Api-Key": api_key,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
       
        if "salesorders" in data:
            salesorders = data["salesorders"]
       
            for salesorder_data in salesorders:
                # Check if the salesorder_id already exists in the database
                if not salesorder.objects.filter(salesorder_id=salesorder_data["salesorder_id"]).exists():
                    salesorder.objects.create(
                        salesorder_id=salesorder_data["salesorder_id"],
                        zcrm_potential_id=salesorder_data["zcrm_potential_id"],
                        zcrm_potential_name=salesorder_data["zcrm_potential_name"],
                        customer_name=salesorder_data["customer_name"],
                        customer_id=salesorder_data["customer_id"],
                        email=salesorder_data["email"],
                        delivery_date=salesorder_data["delivery_date"],
                        company_name=salesorder_data["company_name"],
                        color_code=salesorder_data["color_code"],
                        current_sub_status_id=salesorder_data["current_sub_status_id"],
                        current_sub_status=salesorder_data["current_sub_status"],
                        pickup_location_id=salesorder_data["pickup_location_id"],
                        salesorder_number=salesorder_data["salesorder_number"],
                        reference_number=salesorder_data["reference_number"],
                        date=salesorder_data["date"],
                        shipment_date=salesorder_data["shipment_date"],
                        shipment_days=salesorder_data["shipment_days"],
                        due_by_days=salesorder_data["due_by_days"],
                        due_in_days=salesorder_data["due_in_days"],
                        currency_id=salesorder_data["currency_id"],
                        source=salesorder_data["source"],
                        currency_code=salesorder_data["currency_code"],
                        total=salesorder_data["total"],
                        bcy_total=salesorder_data["bcy_total"],
                        total_invoiced_amount=salesorder_data["total_invoiced_amount"],
                        created_time=salesorder_data["created_time"],
                        last_modified_time=salesorder_data["last_modified_time"],
                        is_emailed=salesorder_data["is_emailed"],
                        quantity_invoiced=salesorder_data["quantity_invoiced"],
                        order_status=salesorder_data["order_status"],
                        invoiced_status=salesorder_data["invoiced_status"],
                        paid_status=salesorder_data["paid_status"],
                        status=salesorder_data["status"],
                        salesperson_name=salesorder_data["salesperson_name"],
                        branch_id=salesorder_data["branch_id"],
                        branch_name=salesorder_data["branch_name"],
                        has_attachment=salesorder_data["has_attachment"],
                        custom_fields_list=salesorder_data["custom_fields_list"],
                        delivery_method=salesorder_data["delivery_method"],
                        delivery_method_id=salesorder_data["delivery_method_id"])
                    print("saved")
                else:
                    print(f"Sales order with ID {salesorder_data['salesorder_id']} already exists.")
                    
        return JsonResponse({"message": "Data processed successfully."})   
    else:
        error_data = {
            "error": f"Error: {response.status_code}",
            "error_message": response.text,
        }
        print("Error in API request:", error_data)
        return JsonResponse(error_data, status=response.status_code)


def salesorderinfo(request):
    salesorderinfo = salesorder.objects.all().order_by('-date')
    
    # Pagination
    paginator = Paginator(salesorderinfo, 10)  # Show 10 sales orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'salesorder.html', {'page_obj': page_obj})

def field(request):
    field=fields.objects.all()
    for fieldes in field:
        print(fieldes.field)
    return render(request,'grnentry1.html',{'fields':field})    

#purchaseorder functions for api
def apicall_purchaseorder(request):
    access_token = "1000.1b2970bb4835a26c56535ddd9142a525.a7e5d78ef91106088fc7beeaa49c012a"
    api_key = "ae530111a097e271b8c051b25b3b59c7"
    url = "https://www.zohoapis.in/books/v3/purchaseorders?organization_id=60004755614"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Api-Key": api_key,
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        if "purchaseorders" in data:
          purchaseorder = data["purchaseorders"]
       
        for purchaseorder_data in purchaseorder:
            apipurchaseorder.objects.create(
                purchaseorder_id=purchaseorder_data["purchaseorder_id"],
                vendor_id=purchaseorder_data["vendor_id"],
                vendor_name=purchaseorder_data["vendor_name"],
                company_name=purchaseorder_data["company_name"],
                order_status=purchaseorder_data["order_status"],
                billed_status=purchaseorder_data["billed_status"],
                status=purchaseorder_data["status"],
                color_code=purchaseorder_data["color_code"],
                current_sub_status_id=purchaseorder_data["current_sub_status_id"],
                current_sub_status=purchaseorder_data["current_sub_status"],
                purchaseorder_number=purchaseorder_data["purchaseorder_number"],
                reference_number=purchaseorder_data["reference_number"],
                date=purchaseorder_data["date"],
                delivery_date=purchaseorder_data["delivery_date"],
                delivery_days=purchaseorder_data["delivery_days"],
                due_by_days=purchaseorder_data["due_by_days"],
                due_in_days=purchaseorder_data["due_in_days"],
                currency_id=purchaseorder_data["currency_id"],
                currency_code=purchaseorder_data["currency_code"],
                price_precision=purchaseorder_data["price_precision"],
                total= purchaseorder_data["total"],
                has_attachment=purchaseorder_data["has_attachment"],
                created_time=purchaseorder_data["created_time"],
                last_modified_time=purchaseorder_data["last_modified_time"],
                quantity_yet_to_receive=purchaseorder_data["quantity_yet_to_receive"],
                quantity_marked_as_received=purchaseorder_data["quantity_marked_as_received"],
                receives=purchaseorder_data["receives"],
                client_viewed_time=purchaseorder_data["client_viewed_time"],
                is_viewed_by_client=purchaseorder_data["is_viewed_by_client"],
                branch_id=purchaseorder_data["branch_id"],
                branch_name=purchaseorder_data["branch_name"])
            print("saved")
        return JsonResponse({"message": "Data saved successfully."})
    else:
        error_data = {
            "error": f"Error: {response.status_code}",
            "error_message": response.text,
        }
        return JsonResponse(error_data, status=response.status_code) 
def purchaseinfo(request):
   purchaseinfo=apipurchaseorder.objects.all().order_by('-date')
   print(purchaseinfo)
   for elements in purchaseinfo:
      print(elements.vendor_name)
   return render(request,'purchaseorder1.html',{'purchase':purchaseinfo})

def purchaseentryshow1(request):
    return render(request,'purchaseentryshow.html')

#dashboard

from django.db.models import Sum, F, FilteredRelation, Q
from django.db.models.functions import Coalesce

from django.db.models.functions import TruncMonth




def dashboard(request):
    # Calculate pending quantities by drawing number
    PENDING_orders = FormData.objects.filter(order_status='Pending')
    pending_by_drawing = PENDING_orders.values(
        'grn_entry__grnentry_DRAWINGNO'
    ).annotate(
        pending_quantity=Sum('grn_entry__grnentry_NOQUANTITY')
    ).order_by('-pending_quantity')

    # Calculate completed quantities by drawing number
    completed_by_drawing = FormData.objects.filter(order_status='Completed').values(
        'grn_entry__grnentry_DRAWINGNO'
    ).annotate(
        completed_quantity=Sum('grn_entry__grnentry_NOQUANTITY')
    ).order_by('-completed_quantity')

    # Get remaining inventory by drawing number
    remaining_inventory = Grnentry1.objects.values('grnentry_DRAWINGNO').annotate(
        total_quantity=Sum('grnentry_NOQUANTITY'),
        used_quantity=Sum('formdata__grn_entry__grnentry_NOQUANTITY', filter=F('formdata__order_status') == 'Completed'),
        remaining_quantity=F('total_quantity') - F('used_quantity')
    ).filter(remaining_quantity__gt=0)

    UPCOMING_orders = Grnentry1.objects.filter(status='Pending')

    processes = ProcessDetails.objects.all()

    # Calculate total accepted and rejected quantities across all processes
    total_accepted = sum(process.acc_qty for process in processes)
    total_rejected = sum(process.rej_qty for process in processes)

    # Calculate total quantity as sum of accepted and rejected quantities
    total_quantity = total_accepted + total_rejected

    # Initialize dictionaries for monthly data
    accepted_qty_by_month = {}
    rejected_qty_by_month = {}
    total_qty_by_month = {}

    # Query ProcessDetails aggregated by month
    processes_by_month = ProcessDetails.objects.annotate(
        month=TruncMonth('start_date')
    ).values('month').annotate(
        total_qty=Sum(F('acc_qty') + F('rej_qty')),
        accepted_qty=Sum('acc_qty'),
        rejected_qty=Sum('rej_qty')
    ).order_by('month')

    # Populate dictionaries with data by month
    for process in processes_by_month:
        month_label = process['month'].strftime('%B')  # Get month name
        total_qty_by_month[month_label] = process['total_qty']
        accepted_qty_by_month[month_label] = process['accepted_qty']
        rejected_qty_by_month[month_label] = process['rejected_qty']

    acceptance_rate = (total_accepted / total_quantity * 100) if total_quantity > 0 else 0
    rejection_rate = (total_rejected / total_quantity * 100) if total_quantity > 0 else 0

    # Format acceptance and rejection rates to two decimal places
    acceptance_rate_formatted = f"{acceptance_rate:.2f}"
    rejection_rate_formatted = f"{rejection_rate:.2f}"

    # Inventory Data
    form_data_list = FormData.objects.all().order_by('-dispatch_time')
    inventory_data = {}

    for form_data in form_data_list:
        drawing_no = form_data.grn_entry.grnentry_DRAWINGNO
        total_dispatched_quantity = form_data.delivery_set.aggregate(total_dispatched=Sum('TTL_QNT_DISPATCH'))['total_dispatched'] or 0
        total_quantity = form_data.grn_entry.grnentry_NOQUANTITY
        remaining_units = total_quantity - total_dispatched_quantity
        part_name = form_data.grn_entry.grnentry_PARTNAME
        material_grade = form_data.grn_entry.grnentry_MATERIALGRADE
        order_status = form_data.order_status
        key = drawing_no

        if key in inventory_data:
            inventory_data[key]['remaining_quantity'] += remaining_units
        else:
            inventory_data[key] = {
                'part_name': part_name,
                'drawing_no': drawing_no,
                'material_grade': material_grade,
                'remaining_quantity': remaining_units,
                'order_status': order_status
            }

    # Aggregate SKUs and remaining quantity
    total_SKUs = len(inventory_data)
    total_remaining_quantity = sum(data['remaining_quantity'] for data in inventory_data.values())

    context = {
        'PENDING_orders': PENDING_orders,
        'pending_by_drawing': pending_by_drawing,
        'completed_by_drawing': completed_by_drawing,
        'remaining_inventory': remaining_inventory,
        'UPCOMING_orders': UPCOMING_orders,
        'processes': processes,
        'total_accepted': total_accepted,
        'total_rejected': total_rejected,
        'total_quantity': total_quantity,  # Add total quantity to context
        'accepted_qty_by_month': accepted_qty_by_month,
        'rejected_qty_by_month': rejected_qty_by_month,
        'total_qty_by_month': total_qty_by_month,
        'acceptance_rate': acceptance_rate_formatted,
        'rejection_rate': rejection_rate_formatted,
        'total_qty_by_month_json': json.dumps(total_qty_by_month),
        'accepted_qty_by_month_json': json.dumps(accepted_qty_by_month),
        'rejected_qty_by_month_json': json.dumps(rejected_qty_by_month),
        'inventory_data': inventory_data,
        'total_SKUs': total_SKUs,
        'total_remaining_quantity': total_remaining_quantity
    }

    return render(request, 'dashboard.html', context)


def calender(request):
    return render(request,'calender.html')    

def calendar_view(request):
    tasks = ProcessDetails.objects.all()  # Example queryset, adjust as per your needs
    return render(request, 'calender.html', {'tasks': tasks})
from datetime import datetime
from django.views.decorators.http import require_GET
@require_GET
def calendar_events(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    operation = request.GET.get('operation')

    events = ProcessDetails.objects.filter(start_date__gte=start_date, end_date__lte=end_date)
    if operation:
        events = events.filter(process__icontains=operation)

    data = [{
        'id': event.id,
        'title': event.process,  # Use 'title' instead of 'process'
        'start': event.start_date.isoformat(),
        'end': event.end_date.isoformat(),
        'description': event.description,
        'acc_qty': event.acc_qty,
        'rej_qty': event.rej_qty,
        'completed': event.completed,
        'className': 'fc-event-' + str(event.id)  # Unique class based on event ID
    } for event in events]

    return JsonResponse(data, safe=False)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Replace 'home' with your homepage URL name
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')