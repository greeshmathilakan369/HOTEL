import imp
from django.shortcuts import render
from reservation.models import *
from .serializers import UserRegistrationSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from . serializers import *
import datetime
from datetime import datetime
from .tasks import *
import email
from rest_framework import permissions

# Create your views here.

#0) users
class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    def get(self,request,*args,**kwargs):
        user11=User.objects.all()
        serializer=UserRegistrationSerializer(user11,many=1)
        return Response(serializer.data)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }
            return Response(response, status=status_code)
    
#0.1) crud operations for user
class UserdetailView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except UserdetailView.DoesNotExist:
            raise Http404  
    def get(self, request, pk, format=None):
        user1 = self.get_object(pk)
        serializer = UserRegistrationSerializer(user1)
        return Response(serializer.data)  
    def put(self, request, pk, format=None):
        user2 = self.get_object(pk)
        serializer = UserRegistrationSerializer(user2, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        user3 = self.get_object(pk)
        user3.delete()
        return Response({'message': 'Successfully Deleted!'},status=status.HTTP_204_NO_CONTENT)
    

#1) view for roomtype [get and post]
class RoomtypeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        roomtype1=Roomtype.objects.all()
        serializer=Roomtype_serializer(roomtype1,many=1)
        return Response(serializer.data)
    def post(self,request,*args,**kwargs):
        serializer=Roomtype_serializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
   
       
       


#1.1) other crud operations   
class RoomtypedetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return Roomtype.objects.get(pk=pk)
        except RoomtypedetailView.DoesNotExist:
            raise Http404  

    def get(self, request, pk, format=None):
        roomtype1 = self.get_object(pk)
        serializer = Roomtype_serializer(roomtype1)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        roomtype2 = self.get_object(pk)
        serializer = Roomtype_serializer(roomtype2, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        roomtype3 = self.get_object(pk)
        roomtype3.delete()
        return Response({'message': 'Successfully Deleted!'},status=status.HTTP_204_NO_CONTENT)
               

# 2) view for rooms [get and post]
class RoomsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        rooms1=Rooms.objects.all()
        serializer=Rooms_serializer(rooms1,many=1)
        return Response(serializer.data)   
    def post(self,request,*args,**kwargs):
        serializer=Rooms_serializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    

#2.1) other crud operations
class Roomdetailview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self,pk):
        try:
            return Rooms.objects.get(pk=pk)
        except Roomdetailview.DoesNotExist:
            raise Http404 
    def get(self,request,pk,format=None):
        room1 = self.get_object(pk)
        serializer = Rooms_serializer(room1)
        return Response(serializer.data)
    def put(self,request,pk,format=None):
        room2=self.get_object(pk=pk) 
        
        serializer= Rooms_serializer(room2,data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        room3=self.get_object(pk)
        room3.delete()   
        return Response({'message':'Sucessfully Deleted'},status=status.HTTP_204_NO_CONTENT) 

#3) Booking
class BookingView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        booking1=Booking.objects.all()
        serializer=Booking_serializer(booking1,many=1)
        return Response(serializer.data)

    
    def post(self,request,*args,**kwargs):
        serializer=Booking_serializer(data=request.data) 
        room_id=request.data["room"]
        seats=Rooms.objects.get(id=room_id)
        c_in = request.data["check_in"]
        c_out = request.data["check_out"]
        rm_no= seats.roomno
        print(rm_no)
        print(c_in)
        print(c_out)
        id = request.data["user"]
        user_email = User.objects.get(id=id)
        email = user_email.email
        print("hello:",seats.room_type.available_rooms)
        msg1 = f"Your booking for room number {rm_no} from {c_in} to{c_out} has been reserved."
        print(msg1)
        if seats.room_type.available_rooms<=seats.room_type.total_rooms and seats.room_type.available_rooms!=0:
            if serializer.is_valid():
                res_object= serializer.save()
                print(res_object)
                res_object.total_amount=res_object.get_total()
                print(res_object.total_amount)
                res_object.save()
                seats.room_type.available_rooms= seats.room_type.available_rooms-1
                print("Availlable rooms:",seats.room_type.available_rooms)
                msg1 = f"Your booking for room number{rm_no}from {c_in} to{c_out} has been reserved."
                print(msg1)
                seats.room_type.save()
                send_mail_task.delay(email,msg1)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        return Response({"msg": "Rooms are unavailable"})
        



class Bookingdetailview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # def get_object(self,pk):
    #     try:
    #         return Booking.objects.get(pk=pk)
    #     except BookingView.DoesNotExist:
    #         raise Http404
    def get(self,request,**kwargs):
        room1 = kwargs.get("id")
        reservation = Booking.objects.get(id=room1)
        serializer = Booking_serializer(reservation)
        return Response(serializer.data)
    

    def put(self,request,*args,**kwargs):
        rs = kwargs.get("id") 
        print(rs)
        room_id=request.data["room"]
        print(room_id)
        seats=Rooms.objects.get(id=room_id)
        instance = Booking.objects.get(id=rs)
        print(instance)
        c_in = request.data["check_in"]
        c_out = request.data["check_out"]
        rm_no= seats.roomno
        id = request.data["user"]
        user_email = User.objects.get(id=id)
        email = user_email.email
        serializer= Booking_serializer(data=request.data, instance=instance)
        if serializer.is_valid():
            print("hai5")
            sts = serializer.validated_data.get("booking_sts")
            print(sts)
            instance.booking_sts = sts
            instance.save()
            if sts=="CANCELLD":
                seats.room_type.available_rooms = seats.room_type.available_rooms+1
                msg2 = f"Your booking for room number{rm_no}from {c_in} to{c_out} has been cancelled."
                print(msg2)
                seats.room_type.save()
                send_mail_cancel_task.delay(email,msg2)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    

    def delete(self,request,**kwargs):
        booking2=kwargs.get("id")
        reservation = Booking.objects.get(id=booking2)
        reservation.delete()
        return Response({'message':'Sucessfully Deleted'},status=status.HTTP_204_NO_CONTENT)            
