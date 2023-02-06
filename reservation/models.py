from django.db import models
from django.contrib.auth.models import PermissionsMixin,AbstractBaseUser
from django.utils import timezone
from .managers import CustomUserManager
from datetime import datetime

# Create your models here.
#1) model for role settings
class User(AbstractBaseUser, PermissionsMixin):

    ADMIN = 1
    CUSTOMER = 2
    RECEPTIONIST = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (CUSTOMER, 'Customer'),
        (RECEPTIONIST, 'Receptionist')
    )
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


    # Roles created here
   
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.DateTimeField(auto_now_add=True)
    modified_by =models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
      return self.email

    @property
    def is_staff(self):
        return self.is_admin
 



#2) model for roomtype      
class Roomtype(models.Model):
    room_category = (
        ('AC','AC'),
        ('NONAC','NONAC'),
        ('Dulux','Dulux'))
    room_type = models.CharField(choices=room_category, default="AC", max_length=20)
    price=models.FloatField()
    total_rooms=models.PositiveIntegerField()
    available_rooms=models.PositiveIntegerField()
    
    def __str__(self):
        return self.room_type
    class Meta:
        unique_together=("room_type",)


#3) model for rooms
class Rooms(models.Model):
    room_type=models.ForeignKey(Roomtype,on_delete=models.CASCADE)
    roomno=models.CharField(max_length=50)
    def __str__(self):
        return self.roomno

#4) model for Bookings
class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Rooms,on_delete=models.CASCADE)
    check_in=models.DateField()
    check_out=models.DateField()
    total_amount = models.FloatField(blank=True,null=True)
    booking_status = (
        ('BOOKED','BOOKED'),
        ('CANCELLD','CANCELLD'))
    booking_sts = models.CharField(choices=booking_status, default="BOOKED", max_length=20)

    class Meta:
        unique_together=("user","room")

    def date_diff(self):
        date_format = "%Y-%m-%d"

        a = datetime.strptime(str(self.check_in),date_format)
        b = datetime.strptime(str(self.check_out),date_format)
        dt = b - a
        print (dt.days)
        return dt.days

    def get_total(self):
        rm =self.room
        print(rm)
        total_amount=0
        total_amount+=rm.room_type.price*(self.date_diff())
        return total_amount