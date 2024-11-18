import datetime
from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from myapp.models import *

def index(request):
    return render(request, 'index.html')

def Sign_Up(request):
    return render(request, 'Sign_Up.html')

def basic(request):
    try:
        pass
    except:
        pass


def Login(request):
    return render(request, 'Login.html')

def insertdata(request):
    if request.method == "POST":
        username = request.POST.get("Name")
        useremail = request.POST.get("Email")
        userphone = request.POST.get("Phone")
        userpwd = request.POST.get("Password")
        queary = Customer.objects.filter(Email_id=useremail)
        if queary.exists():
            messages.error(request,'Email already exists!!')
            return render(request,"Sign_Up.html")
        else:
            queary=Customer(Name=username,Email_id=useremail,Phone_no=userphone,Password=userpwd,Status="Active")
            queary.save()
            messages.success(request,'REGISTRATION SUCCESSFUL!!')
            return redirect(Login)
    else:
        messages.error(request, 'SORRY!! UNABLE TO INSERT!!')
        return render(request,"Sign_Up.html")

def CheckLogin(request):
     useremail=request.POST['Email']
     userpwd=request.POST['Password']
     try:
         query=Customer.objects.get(Email_id=useremail,Password=userpwd)
         request.session['useremail']=query.Email_id
         request.session['user_id'] = query.id
         request.session.save()
         print(request.session['user_id'])
     except Customer.DoesNotExist:
         query=None
     if query is not None:
         messages.success(request, 'LOGIN SUCCESSFUL!!')
         return redirect(index)
     else:
         messages.info(request,'Account Does Not Exists !! Please Sign Up')
     return render(request,"Sign_Up.html")

def Logout(request):
    if 'useremail' in request.session:
        request.session.flush()  # This will clear the session data
        messages.success(request, 'LOGOUT SUCCESSFUL!!')
    return redirect(index)

def editprofile(request):
    Login_Id = request.session['user_id']
    query=Customer.objects.get(id=Login_Id)
    return render(request,"edit_profile.html",{"user":query})

def updateprofile(request):
    Name=request.POST.get("name")
    Email=request.POST.get("email")
    Phone=request.POST.get("phone")
    Password = request.POST.get("password")
    Login_Id = request.session['user_id']
    query= Customer.objects.get(id=Login_Id)
    query.Name = Name
    query.Email_id = Email
    query.Phone_no = Phone
    query.Password = Password
    query.save()
    return redirect(index)

def Menu(request):
    # Fetch menu items by category
    starters = Restaurent_Menu_Items.objects.filter(Category_id__Category_Name='Starters')
    salads = Restaurent_Menu_Items.objects.filter(Category_id__Category_Name='Salads')
    specialty = Restaurent_Menu_Items.objects.filter(Category_id__Category_Name='Specialty')
    desserts = Restaurent_Menu_Items.objects.filter(Category_id__Category_Name='desserts')

    context = {
        'starters': starters,
        'salads': salads,
        'specialty': specialty,
        'desserts': desserts,
    }

    return render(request, 'Menu.html',context)


def product_details(request, product_id):
    # Fetch the product based on the ID
    product = Restaurent_Menu_Items.objects.get(id=product_id)

    context = {
        'product': product,
    }
    return render(request, 'Menu_Details.html', context)

def event(request):
    return render(request, 'event.html')

def Contact(request):
    return render(request,'contact.html')

def insert_contact(request):
    if request.method=="POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        sub = request.POST.get("subject")
        msz = request.POST.get("message")

        obj = Contact_Us(Name=name, Email=email,Subject=sub,Message=msz)
        obj.save()

        messages.success(request, 'DETAILS ARE SUCCESSFULLY ADDED WE WILL CONTACT YOU SOON!!')

    return redirect(Contact)

def Booking(request):
    return render(request,'Booking.html')

def insert_booking(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in to add items to your cart.")
        return redirect('Login')  # Redirect to login if not logged in

    user = Customer.objects.get(id=request.session['user_id'])  # Get the logged-in user

    if request.method == "POST":
        name = request.POST['Name']
        email = request.POST['email']
        phone = request.POST['phone']
        date = request.POST['date']
        time = request.POST['time']
        people = request.POST['people']
        message = request.POST['message']

        # Save the booking data to the database
        booking = Booking_Now(
            user=user,
            Name=name,
            email=email,
            phone_no=phone,
            date=date,
            time=time,
            people=people,
            message=message
        )
        booking.save()

        # Send confirmation email
        subject = "Booking Confirmation"
        body = f"Dear {name},\n\nYour table reservation for {date} at {time} for {people} people has been successfully booked.\n\nThank you for choosing us!\n\nBest Regards,\nRestaurantly"
        send_mail(
            subject,
            body,
            'your_email@example.com',  # From email
            [email],  # To email
            fail_silently=False,
        )

        # Add a success message
        messages.success(request, 'Your booking has been confirmed and a confirmation email has been sent.')

        return redirect(booking_history)  # Redirect to booking page or a success page
    else:
        return render(request, 'booking.html')



def add_to_cart(request, product_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in to add items to your cart.")
        return redirect('Login')  # Redirect to login if not logged in

    product = Restaurent_Menu_Items.objects.get(id=product_id)
    user = Customer.objects.get(id=request.session['user_id'])  # Get the logged-in user

    cart_item, created = Add_To_Cart.objects.get_or_create(
        product=product,
        user=user,  # Use the user instance instead of session_key
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.Name} added to your cart.")
    return redirect('cart')


def cart(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in to view your cart.")
        return redirect('Login')  # Redirect to login if not logged in

    user = Customer.objects.get(id=request.session['user_id'])  # Get the logged-in user
    cart_items = Add_To_Cart.objects.filter(user=user)  # Filter cart items by user

    # Calculate total price
    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)


def update_cart(request, cart_id):
    if request.method == 'POST':
        if 'user_id' not in request.session:
            messages.error(request, "You need to be logged in to update your cart.")
            return redirect('Login')  # Redirect to login if not logged in

        cart_item = Add_To_Cart.objects.get(id=cart_id)
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully!")
        else:
            cart_item.delete()
            messages.success(request, "Item removed from cart!")

    return redirect('cart')


def remove_from_cart(request, cart_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in to remove items from your cart.")
        return redirect('Login')  # Redirect to login if not logged in

    cart_item = Add_To_Cart.objects.get(id=cart_id)
    cart_item.delete()
    messages.success(request, "Item removed from cart!")
    return redirect('cart')

def is_valid_card_number(card_number):
    return card_number.isdigit() and 13 <= len(card_number) <= 16

def is_valid_expiry_date(expiry_date):
    # Check if the expiry date is in MM/YY format and in the future
    try:
        exp_month, exp_year = expiry_date.split('/')
        exp_month = int(exp_month)
        exp_year = int(exp_year) + 2000  # Assuming YY format

        if 1 <= exp_month <= 12:
            current_date = datetime.datetime.now()
            expiry_date_obj = datetime.datetime(exp_year, exp_month, 1)
            return expiry_date_obj > current_date
        return False
    except (ValueError, IndexError):
        return False

def is_valid_cvv(cvv):
    return cvv.isdigit() and len(cvv) == 3

# Checkout view

def checkout_view(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in to proceed with the checkout.")
        return redirect('Login')

    user = Customer.objects.get(id=request.session['user_id'])
    cart_items = Add_To_Cart.objects.filter(user=user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty. Please add items before checking out.")
        return redirect('cart')

    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        # Collect shipping details
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')

        # Collect payment details
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        payment_method = request.POST.get('payment_method')

        if not all([name, phone, address, city, state, postal_code, card_number, expiry_date, cvv, payment_method]):
            messages.error(request, "Please fill in all shipping and payment details.")
            return redirect('checkout')

        # Payment validation (omitted here for brevity)
        if not is_valid_card_number(card_number):
            messages.error(request, "Please enter a valid card number.")
            return redirect('checkout')

        if not is_valid_expiry_date(expiry_date):
            messages.error(request, "Please enter a valid expiry date.")
            return redirect('checkout')

        if not is_valid_cvv(cvv):
            messages.error(request, "Please enter a valid CVV.")
            return redirect('checkout')

        # Create order
        order = Order.objects.create(user=user, total_price=total_price)

        # Create OrderItems
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.get_total_price()
            )

        # Save the shipping details
        shipping_address = ShippingAddress.objects.create(
            user=user,
            email=email,
            order=order,
            name=name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            postal_code=postal_code
        )

        # Process payment (omitted here for brevity)
        Payment.objects.create(
            user=user,
            order=order,
            payment_method=payment_method,
            card_number=card_number,
            expiry_date=expiry_date,
            cvv=cvv,
            paid=True
        )

        # Clear the cart
        cart_items.delete()

        # Send confirmation email
        subject = f"Order Confirmation - Order #{order.id}"
        message = render_to_string('order_confirmation_email.html', {
            'user': user,
            'order': order,
            'order_items': OrderItem.objects.filter(order=order),
            'shipping_address': shipping_address,
        })

        # Use the `html_message` parameter for HTML content
        send_mail(
            subject,
            "This is a plain text fallback message.",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=message,  # This should contain the rendered HTML
            fail_silently=False,
        )

        # Redirect to success page
        messages.success(request, "Order placed successfully!")
        return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })




def order_success_view(request, order_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in to view this page.")
        return redirect('Login')

    user = Customer.objects.get(id=request.session['user_id'])
    order = Order.objects.get(id=order_id, user=user)
    order_items = OrderItem.objects.filter(order=order)

    return render(request, 'order_success.html', {
        'order': order,
        'order_items': order_items
    })

def order_history_view(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in to view your order history.")
        return redirect('Login')

    user = Customer.objects.get(id=request.session['user_id'])
    orders = Order.objects.filter(user=user).order_by('-created_at')

    if not orders.exists():
        messages.info(request, "You have no order history.")
        return render(request, 'order_history.html', {'orders': None})

    return render(request, 'order_history.html', {'orders': orders})

from django.contrib.auth.decorators import login_required


def booking_history(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to be logged in to view your order history.")
        return redirect('Login')

    user = Customer.objects.get(id=request.session['user_id'])

    try:
        # Get bookings related to the logged-in user (assuming bookings are linked by email)
        bookings = Booking_Now.objects.filter(user=user).order_by('-timestamp')

        # Pass the bookings to the template
        context = {
            'bookings': bookings
        }

        return render(request, 'booking_history.html', context)

    except Exception as e:
        # In case of an error, add a message and redirect to another page or render an error template
        messages.error(request, f"An error occurred while fetching your bookings: {e}")
        return render(request, 'booking_history.html', {'bookings': None})

def forgotpassword(request):
    if request.method == 'POST':
        username = request.POST['email']
        try:
            user = Customer.objects.get(Email_id=username)

        except Customer.DoesNotExist:
            user = None
        #if user exist then only below condition will run otherwise it will give error as described in else condition.
        if user is not None:
            #################### Password Generation ##########################
            import random
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = 6
            nr_symbols = 1
            nr_numbers = 3
            password_list = []

            for char in range(1, nr_letters + 1):
                password_list.append(random.choice(letters))

            for char in range(1, nr_symbols + 1):
                password_list += random.choice(symbols)

            for char in range(1, nr_numbers + 1):
                password_list += random.choice(numbers)

            print(password_list)
            random.shuffle(password_list)
            print(password_list)

            password = ""  #we will get final password in this var.
            for char in password_list:
                password += char

            ##############################################################


            msg = "hello here it is your new password  "+password   #this variable will be passed as message in mail

            ############ code for sending mail ########################

            from django.core.mail import send_mail

            send_mail(
                'Your New Password',
                msg,
                'meet951018@gmail.com',
                [username],
                fail_silently=False,
            )
            # NOTE: must include below details in settings.py
            # detail tutorial - https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
            # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            # EMAIL_HOST = 'smtp.gmail.com'
            # EMAIL_USE_TLS = True
            # EMAIL_PORT = 587
            # EMAIL_HOST_USER = 'mail from which email will be sent'
            # EMAIL_HOST_PASSWORD = 'pjobvjckluqrtpkl'   #turn on 2 step verification and then generate app password which will be 16 digit code and past it here

            #############################################

            #now update the password in model
            cuser = Customer.objects.get(Email_id=username)
            cuser.Password = password
            cuser.save(update_fields=['Password'])

            print('Mail sent')
            messages.info(request, 'Mail Is Sent')
            return redirect(index)

        else:
            messages.info(request, 'This account does not exist')
    return redirect(index)

def forgot(request):
    return render(request,"forgot_password.html")




