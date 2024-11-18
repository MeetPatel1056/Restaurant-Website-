from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.
USERSTATUS={
    ("Inactive","Inactive"),
    ("Active","Active"),
}

# Create your models here.
class Customer(models.Model):
    Name=models.CharField(max_length=25)
    Email_id=models.EmailField()
    Phone_no=models.BigIntegerField()
    Password=models.CharField(max_length=25)
    Status=models.CharField(max_length=25,choices=USERSTATUS)


    def __str__(self):
        return self.Name

class Contact_Us(models.Model):
    Name = models.CharField(max_length=250)
    Email = models.EmailField()
    Subject = models.CharField(max_length=250)
    Message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
       return self.Name
   
   
class Booking_Now(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Add this line
    Name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    phone_no = models.CharField(max_length=15)
    time = models.TimeField()
    date = models.DateField()
    people = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name


class Category(models.Model):
    Category_Name=models.CharField(max_length=25)

    def __str__(self):
        return self.Category_Name
   
class Restaurent_Menu_Items(models.Model):
    Category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    Name = models.CharField(max_length=30)
    desc = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    image=models.ImageField(upload_to='photos')

    def Menu_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))

    def __str__(self):
         return self.Name


class Add_To_Cart(models.Model):
    product = models.ForeignKey(Restaurent_Menu_Items, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Add this line

    def __str__(self):
        return f"{self.quantity} x {self.product.Name}"

    def get_total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(Add_To_Cart)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=True)

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Restaurent_Menu_Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.Name} - {self.quantity} pcs"

class ShippingAddress(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f"Shipping Address for {self.user}"

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('mobile_wallet', 'Mobile Wallet'),
    ]

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for {self.order}'



