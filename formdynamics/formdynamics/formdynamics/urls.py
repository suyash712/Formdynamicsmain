"""
URL configuration for formdynamics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import master_component_form, show_master_component, update_master_component
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('login', views.login_view, name='login_view'),
    path('', views.dashboard_page, name='dashboard'),
    path('admin/', admin.site.urls),
    path('grnentry1',views.grnentry, name='grnentry'),
    path('grnentry',views.savegrndata,name='savegrndata'),
    path('grnmainpage',views.grninfo,name='grninfo'),
    path('apicall_salesorder',views.apicall_salesorder,name='apicall'),
    path('apicall_purchaseorder',views.apicall_purchaseorder,name='apicall_purchaseorder'),
    path('salesorder1',views.salesorderinfo,name="salesorderinfo"),
    path('purchaseinfo',views.purchaseinfo,name='purchaseinfo'),
   
    path("purchaseinfoshow",views.purchaseinfoshow),
    path('trackentry',views.trackentry),
    path('inventory',views.inventory_view,name='inventory'),
    path('trackmainpage',views.trackmainpage),
    path('purchaseentryshow',views.purchaseentryshow1),
        path('dispatch-details/<int:entry_id>/', views.dispatch_details1, name='dispatch_details'),
  
  path('save-field/', views.save_field, name='save_field'),
    path('displayformdata',views.display_form_data, name='display_form_data'),
    path('display_form_data', views.display_form_data, name='display_form_data'),
    path('entry_details<int:entry_id>', views.display_entry_details, name='display_entry_details'),
    path('form-view<int:entry_id>', views.form_view1, name='form_view1'),
    path('field',views.field,name='field'),
    path("field",views.save_field,name='savefield'),
    path('savefield/', views.save_field, name='savefield'),
    path('materialinfo1',views.display_material,name='display_material'),
     path('get_material/', views.get_material, name='get_material'),
    path('edit_material/', views.edit_material, name='editmaterial'),
    # URL for editing material (POST request)
    path('edit_material/', views.edit_material, name='edit_material'),
    path('savematerial',views.savematerial,name='savematerial'),
    path('saveemployee/', views.saveemployee, name='saveemployee'),
    # URL pattern for displaying all employees
   path('employees', views.showemployee,name='employees'),
    path('update_employee/<int:employee_id>/', views.update_employee, name='update_employee'),
    path('saveemployee/', views.saveemployee, name='saveemployee'),
    # URL for showing instruction calibration page
     path('instruction_calibration', views.show_ins_cal,name='instruction_calibration'),
    # URL for adding new calibration instruction
    path('cal/', views.ins_cal_form, name='cal'),
    # URL for updating existing calibration instruction
    path('update_cal/<int:pk>/', views.update_cal, name='update_cal'),
    path('i/', views.inventory_view, name='inventory_view'),
   path('show_master_component',views.show_master_component,name='show_master_component'),
   path('master_component_form',views.master_component_form,name='master_component_form'),
   path('update_master_component/<int:component_id>/', views.update_master_component, name='update_master_component'),
   path('pdf/<path:file_path>/', views.serve_pdf, name='serve_pdf'),
    path('outsourse',views.outsourse),
    path('showoutsourse',views.showoutsourse,name='showoutsourse'),
    path('outsourseform',views.outsourseform,name='outsourseform'),
    path('mark_complete/<int:pk>/', views.mark_complete, name='mark_complete'),
    path('notifications/', views.get_notifications, name='notifications'),
    path('dashboard', views.dashboard,name='dashboard' ),
    path('form<int:entry_id>', views.form_view, name='form_view'),
    path('trackingentry<int:entry_id>', views.tracking_entry_view, name='tracking_entry_view'),
    path('display_form_data', views.display_form_data, name='display_form_data'),
  path('edit_grnentry/<int:pk>/', views.edit_grnentry, name='edit_grnentry'),
      path('save_supplier/', views.save_supplier, name='save_supplier'),
      path('ins_cal_form',views.ins_cal_form,name='ins_cal_form'),
       path('get_suppliers/', views.get_suppliers, name='get_suppliers'),
       path('save_completion/<int:entry_id>/', views.save_completion, name='save_completion'),
      path('calender', views.calendar_view, name='calendar'),
        path('calendar_events/', views.calendar_events, name='calendar_events'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])