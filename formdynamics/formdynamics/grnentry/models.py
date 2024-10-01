from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


# Create your models here.

class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=100)
    user_agent = models.TextField()

    def __str__(self):
        return f"Login by {self.user.username} at {self.login_time}"
    
    
class Grnentry1(models.Model):
    QUANTITY_TYPE_CHOICES = [
        ('KG', 'KG'),
        ('NO_S', 'NO\'S'),
    ]
    ORDER_TYPE_CHOICES = [
        ('WITH MATERIAL', 'With Material'),
        ('JOB WORK', 'Job Work'),
    ]
    STORE_OWNER_CHOICES = [
        ('YOGESH PALKAR','YOGESH PALKAR'),
        ('PRANAV PATIL','PRANAV PATIL'),
        ('SHUBHAM BHALERAO','SHUBHAM BHALERAO')
    ]

    grnentry_GRNNO = models.CharField(max_length=200)
    grnentry_MATERIALDESCRIPTION = models.TextField(max_length=200)
    grnentry_MATERIALGRADE = models.CharField(max_length=200)  # Changed to a simple CharField
    grnentry_QUANTITYTYPE = models.CharField(max_length=200, choices=QUANTITY_TYPE_CHOICES)
    grnentry_NOQUANTITY = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    grnentry_DATETIME = models.DateField(max_length=200, auto_now_add=True)
    grnentry_STOREOWNER = models.CharField(max_length=200, choices=STORE_OWNER_CHOICES)
    grnentry_ORDERTYPE = models.CharField(max_length=200, choices=ORDER_TYPE_CHOICES)
    grnentry_PONO = models.CharField(max_length=200)
    grnentry_CHALLANNO = models.CharField(max_length=200)
    grnentry_COMMENTS = models.TextField(max_length=200)
    grnentry_SONO = models.CharField(max_length=200)
    grnentry_PARTNAME = models.CharField(max_length=200)
    grnentry_DRAWINGNO = models.CharField(max_length=200)
    REVISIONNO = models.CharField(max_length=200)
    grnentry_EXPTIME = models.DateField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending')
    FILE = models.FileField(upload_to='grnentryfile/')
    customername=models.CharField(max_length=200)

    def __str__(self):
        return self.grnentry_GRNNO
from django.db.models import Sum     

class FormData(models.Model):
    vendor_name = models.CharField(max_length=100)
    order_status = models.CharField(max_length=50, default='Pending')
    dispatch_time = models.DateTimeField(null=True, blank=True)
    grn_entry = models.ForeignKey(Grnentry1, on_delete=models.CASCADE)
    ttl_rejected_qty = models.IntegerField(default=0)
    ttl_accepted_qty=models.IntegerField(default=0)
    ttl_dispatch_qty=models.IntegerField(default=0)
    rem_qty_dispatch=models.IntegerField(default=0)

    def update_ttl_rejected_qty(self):
         rejected_sum = self.processdetails_set.aggregate(total_rejected=Sum('rej_qty'))['total_rejected'] or 0
         print(f"Rejected Sum: {rejected_sum}")  # Debug print statement
    
         self.ttl_rejected_qty = rejected_sum
         self.save()
         print(f"Updated ttl_rejected_qty to: {self.ttl_rejected_qty}") 
   
   
    def update_ttl_accepted_qty(self):
        # Calculate accepted quantity as grnentry_NOQUANTITY - ttl_rejected_qty
        self.ttl_accepted_qty = max(self.grn_entry.grnentry_NOQUANTITY - self.ttl_rejected_qty, 0)
        self.save()

    def update_rem_qty_dispatch(self):
        self.rem_qty_dispatch = max(self.grn_entry.grnentry_NOQUANTITY - self.ttl_dispatch_qty, 0)
        print(f"Updating rem_qty_dispatch: {self.rem_qty_dispatch}")  # Debug statement
        self.save()

    def update_order_status(self):
        # Get all process details associated with this form data
        process_details = self.processdetails_set.all()
        
        # Check if all process details are completed
        if process_details.filter(completed=False).exists():
            self.order_status = 'Pending'
        else:
            self.order_status = 'Completed'
        
        self.save()

    def update_form_data(self):
        # Perform any additional updates or calculations specific to FormData
        self.update_ttl_rejected_qty()
        self.update_order_status()
        # Add more updates as needed for other attributes or related models

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set default for new instances
            self.ttl_accepted_qty = self.grn_entry.grnentry_NOQUANTITY
            self.rem_qty_dispatch = self.grn_entry.grnentry_NOQUANTITY
        super().save(*args, **kwargs)    

    def update_ttl_dispatch_qty(self):
        dispatch_sum = self.delivery_set.aggregate(total_dispatch=Sum('TTL_QNT_DISPATCH'))['total_dispatch'] or 0
        self.ttl_dispatch_qty = dispatch_sum
        self.save()    

    def __str__(self):
        return self.vendor_name


class ProcessDetails(models.Model):
    form_data = models.ForeignKey(FormData, on_delete=models.CASCADE)
    process = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    quantity = models.IntegerField()
    completed = models.BooleanField(default=False)
    completed_time = models.DateTimeField(blank=True, null=True)
    grn_entry = models.ForeignKey(Grnentry1, on_delete=models.CASCADE)
    acc_qty = models.IntegerField(default=0)
    rej_qty = models.IntegerField(default=0)

    def mark_as_completed(self):
        self.completed_time = timezone.now()
        self.completed = True
        self.save()

    def total_accepted_quantity(self):
        # Calculate total accepted quantity for this process
        total = self.acc_qty
        return total

    @property
    def total_rejected_quantity(self):
        # Calculate total rejected quantity for this process
        total = self.rej_qty
        return total    


class Delivery(models.Model):
    form_data = models.ForeignKey(FormData, on_delete=models.CASCADE)
    FINISHEDQTY = models.IntegerField()
    PDIREPORT = models.FileField(upload_to='pdireports/')
    TTL_QNT_DISPATCH = models.IntegerField()
    INVOICENO = models.CharField(max_length=100)
    DELIVERYCHALLAN=models.CharField(max_length=200)
    OPTIONDC=models.CharField(max_length=200)
    BUYERNAME = models.CharField(max_length=100)
    SALESREPRESENT = models.CharField(max_length=100)
    PARTCOST = models.DecimalField(max_digits=10, decimal_places=2)
    DATE=models.DateField()
   
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.form_data.update_ttl_dispatch_qty()
        self.form_data.update_rem_qty_dispatch()
        
   
class Inventory(models.Model):
    delivery =models.ForeignKey(Delivery, on_delete=models.CASCADE)
    form_data = models.ForeignKey(FormData, on_delete=models.CASCADE)
    remaining_quantity = models.IntegerField(default=0)

class fields(models.Model):
    field=models.CharField(max_length=200)

class Supplier(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class material(models.Model):
        part_description=models.CharField(max_length=200)
        DRAW_NO=models.CharField(max_length=200)
        Material_Grade=models.CharField(max_length=200)
        Finish_size=models.CharField(max_length=200)
        Raw_material_size=models.CharField(max_length=200)
        order_size=models.CharField(max_length=200)
        DRAWING_PDF=models.FileField(upload_to='materialpdf/')



class Employee_info(models.Model):
    name=models.CharField(max_length=200)
    Designation=models.CharField(max_length=200)
    aadhar_no=models.CharField(max_length=200)
    mobile_no=models.CharField(max_length=200)

make = [
        ('mithutoyo', 'mithutoyo'),
        ('insize', 'insize'),
        ('bakers', 'bakers'),
        ('ensons', 'ensons'),
        ('aerospace', 'aerospace'),
        ('workzone', 'workzone'),
        ]

UNIT_CHOICES = [
    ('mm', 'mm'),
    ('cm', 'cm'),
    ('m', 'm'),
    ('km', 'km'),
    ('in', 'in'),
    ('ft', 'ft'),
    ('yd', 'yd'),
    ('mi', 'mi'),
]

class calibration(models.Model):
    inst_name=models.CharField(max_length=200)
    make=models.CharField(max_length=200,choices=make) 
    least_count=models.IntegerField()
    least_count_unit=models.CharField(max_length=200,choices=UNIT_CHOICES)
    least_range=models.IntegerField()
    max_range=models.IntegerField()
    range_unit=models.CharField(max_length=200,choices=UNIT_CHOICES)
    location=models.CharField(max_length=200)
    calibrated_date=models.DateTimeField()
    next_calibration_due_date=models.DateTimeField()
    remark=models.CharField(max_length=200)

class master_component(models.Model):
    description=models.CharField(max_length=200)
    drawing_no=models.CharField(max_length=200)
    revision_no=models.CharField(max_length=200)
    drawing_pdf=models.FileField(upload_to='master_drawing/')    

status=[
    ('pending','pending'),
    ('completed','completed')
]




class Outsourse1(models.Model):
    grnno = models.CharField(max_length=200)
    supplier_name = models.CharField(max_length=200)
    supplier_process_name = models.CharField(max_length=200)
    operation_name = models.CharField(max_length=200)
    part_desc = models.CharField(max_length=200)
    quantity = models.IntegerField()
    out_date = models.DateField()
    receive_date = models.DateField(null=True, blank=True)
    accepted_qty = models.IntegerField(default=0)
    rejected_qty = models.IntegerField(default=0)
    rate = models.IntegerField()
    status = models.CharField(max_length=200, default='pending')
    completed_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.grnno

    def set_date(self, date_str):
        try:
            self.date_field = parse_date(date_str)  # Ensure date_str is a valid string
        except Exception as e:
            print(f"Error setting date: {e}")



class Notification(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    calibration = models.ForeignKey(calibration, on_delete=models.CASCADE)

