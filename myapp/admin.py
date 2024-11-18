from django.contrib import admin
from .models import *

class Show_User(admin.ModelAdmin):
    list_display = ["Name","Email_id","Phone_no","Password","Status"]
admin.site.register(Customer,Show_User)

class Show_Booking(admin.ModelAdmin):
    list_display = ('user','Name', "phone_no", "time", "email", "date", "people", "message","timestamp")
admin.site.register(Booking_Now,Show_Booking)


class Show_Contact(admin.ModelAdmin):
    list_display = ["Name","Email","Subject","Message","timestamp"]
admin.site.register(Contact_Us,Show_Contact)

class Show_Category(admin.ModelAdmin):
    list_display = ["Category_Name"]
admin.site.register(Category,Show_Category)

class Show_Menu(admin.ModelAdmin):
    list_display = ["Category_id","Name","desc","price","image","Menu_photo"]
admin.site.register(Restaurent_Menu_Items,Show_Menu)

class Show_Order(admin.ModelAdmin):
     list_display = ["user","total_price","created_at","is_paid"]
admin.site.register(Order,Show_Order)

class Show_Order_Item(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "price"]
admin.site.register(OrderItem, Show_Order_Item)

class Show_Checkout(admin.ModelAdmin):
     list_display = ["user","email","order","name","phone","address","city","state","postal_code"]
admin.site.register(ShippingAddress,Show_Checkout)

class Show_Payment(admin.ModelAdmin):
    list_display = ('user', 'order', 'payment_method', 'payment_date', 'paid')
    list_filter = ('payment_method', 'paid')
    search_fields = ('user__email', 'order__id')
    ordering = ('-payment_date',)

admin.site.register(Payment,Show_Payment)