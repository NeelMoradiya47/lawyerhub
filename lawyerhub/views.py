import os
from datetime import date, datetime
import uuid
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from .models import Administrator, Booking, Client, Lawyer, Feedback
from bson import json_util
import json
import requests

# Function to format data into JSON
def get_formatted_data(data):
    formatted_data = []
    for row in data:
          formatted_data.append(row)
    
    # Convert formatted_data list to JSON format
    json_data = json.dumps(formatted_data, default=json_util.default)
    return json_data

def index(request):
    lawyer_data = Lawyer.objects.filter(status='Active').values()
    
    msg = request.session.get('msg', '')
    if msg == 'lawyer':
        return render(request, 'index.html', {'lawyer_data': lawyer_data, 'msg': msg})
    elif msg == 'user':
        return render(request, 'index.html', {'lawyer_data': lawyer_data, 'msg': msg})
    elif msg == 'admin':
        return render(request, 'index.html', {'lawyer_data': lawyer_data, 'msg': msg})
    else:    
        return render(request, 'index.html', {'lawyer_data': lawyer_data})

def lawyers(request):
    lawyer_data = Lawyer.objects.filter(status='Active').values()
    
    msg = request.session.get('msg', '')
    if msg == 'lawyer' or msg == 'user' or msg == 'admin':
        return render(request, 'lawyers.html', {'lawyer_data': lawyer_data, 'msg': msg})
    else:
        return render(request, 'lawyers.html', {'lawyer_data': lawyer_data})

def about_us(request):
    msg = request.session.get('msg', '')
    if msg == 'lawyer' or msg == 'user' or msg == 'admin':
        return render(request, 'about_us.html', {'msg': msg})
    else:
        return render(request, 'about_us.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedback = request.POST.get('feedback')
        
        fb = Feedback(name=name, email=email, feedback=feedback)
        fb.save()
        
        thk = "Thank you for providing us your feedback."
        return render(request, 'contact_us.html', {'thk': thk})

    msg = request.session.get('msg', '')
    if msg == 'lawyer' or msg == 'user' or msg == 'admin':
        return render(request, 'contact_us.html', {'msg': msg})
    else:
        return render(request, 'contact_us.html')

def search_lawyer(request):
    if request.method == 'POST':
        experience = request.POST.get('experience')
        speciality = request.POST.get('speciality')
        location = request.POST.get('location')

        lawyer_data = Lawyer.objects.filter(practise_length=experience, speciality=speciality, city=location, status='Active')
        
        if not lawyer_data.exists():
            message = "No matching data found."
            return render(request, 'search_lawyer.html', {'message': message})

        formatted_lawyer_data = get_formatted_data(lawyer_data.values())
        
        return render(request, 'search_lawyer.html', {'lawyer_data': formatted_lawyer_data})
    
    msg = request.session.get('msg', '')
    if msg == 'lawyer' or msg == 'user' or msg == 'admin':
        return render(request, 'search_lawyer.html', {'msg': msg})
    else:
        return render(request, 'search_lawyer.html')

def single_lawyer(request, l_id):
    lawyer_data = Lawyer.objects.filter(lawyer_id=l_id, status='Active').values().first()
    
    msg = request.session.get('msg', '')
    if msg == 'lawyer' or msg == 'user' or msg == 'admin':
        if request.method == 'POST':
            f_date = request.POST.get('date')
            description = request.POST.get('description')
            client_id = request.session.get('client_id')
            lawyer_id = request.POST.get('lawyer_id')
        
            client_names = Client.objects.filter(client_id=client_id).values().first()
            user_first_name = client_names.get('first_name', 'first_name not available')
            user_last_name = client_names.get('last_name', 'last_name not available')
            user_contact_no = client_names.get('contact_number', 'contact_number not available')
            user_email = client_names.get('email', 'email not available')
            
            lawyer_names = Lawyer.objects.filter(lawyer_id=lawyer_id).values().first()
            lawyer_first_name = lawyer_names.get('first_name', 'first_name not available')
            lawyer_last_name = lawyer_names.get('last_name', 'last_name not available')
            lawyer_contact_no = lawyer_names.get('contact_number', 'contact_number not available')
            lawyer_email = lawyer_names.get('email', 'email not available')

            booking_data = Booking.objects.create(date=f_date, description=description, client_id=client_id, lawyer_id=lawyer_id, status='Pending', user_first_name=user_first_name, user_last_name=user_last_name, user_contact_number=user_contact_no, user_email=user_email, lawyer_first_name=lawyer_first_name, lawyer_last_name=lawyer_last_name, lawyer_contact_number=lawyer_contact_no, lawyer_email=lawyer_email)
            
            if booking_data:
                subject = "Notification For Account Information"
                message = f"{lawyer_first_name} {lawyer_last_name} you get one booking request by {user_first_name} {user_last_name}."

                email_message = EmailMessage(
                    subject,
                    message,
                    "neelmoradiya56@gmail.com",
                    [lawyer_email],
                )

                try:
                    email_message.send()
                    # print("mail sent")
                except Exception as e:
                    # print(e)
                    # print("mail not sent")
                    pass
        
                request.session['success'] = "Your booking request is successfully booked"
                return redirect('lawyerhub:user_booking')
        
        return render(request, 'single_lawyer.html', {'lawyer_data': lawyer_data, 'msg': msg})
    else:
        return render(request, 'single_lawyer.html', {'lawyer_data': lawyer_data})

def send_message_admin(request):
    # Nexmo credentials
    nexmo_api_key = '6f78714d'
    nexmo_api_secret = 'TYmzVMqIrf7rihCr'
    nexmo_phone_number = '+917574020228'
    recipient_phone_number = '+917574020228'
    
    # User information
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name', '')
    contact_number = request.POST.get('contact_number')
    email = request.POST.get('email')    

    # Construct SMS body
    body = f'{first_name} {last_name} registered as Lawyer, Email: {email}, and contact number: {contact_number}'
    
    # Nexmo API endpoint
    nexmo_api_url = 'https://rest.nexmo.com/sms/json'
    
    # Create payload for the API request
    params = {
        'api_key': nexmo_api_key,
        'api_secret': nexmo_api_secret,
        'from': nexmo_phone_number,
        'to': recipient_phone_number,
        'text': body,
    }

    # Send SMS using Nexmo API
    requests.post(nexmo_api_url, data=params)
    # response = requests.post(nexmo_api_url, data=params)

    # if response.status_code == 200:
    #     print("Message sent successfully.")
    # else:
    #     print(f"Failed to send message. Status code: {response.status_code}")
    #     print(response.text)
    
def send_email_lawyer_and_user(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')

    subject = "Notification For Account Information"
    message = render_to_string('send_email_lawyer_and_user.html', {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
    })

    email_message = EmailMessage(
        subject,
        message,
        "neelmoradiya56@gmail.com",
        [email],
    )
    
    email_message.content_subtype = 'html'

    try:
        email_message.send()
    except Exception as e:
        pass

def lawyer_register(request):
    passing_years = range(datetime.now().year, 1999, -1)

    if request.method == 'POST':
        lawyer_id = f"Lawyer_{uuid.uuid4().hex[:8]}"
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name', '')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        university_college = request.POST.get('university_college')
        degree = request.POST.get('degree')
        passing_year = request.POST.get('passing_year')
        full_address = request.POST.get('full_address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        practise_length = request.POST.get('practise_length')
        case_handle = request.POST.getlist('case_handle')
        speciality = request.POST.get('speciality')
        
        if Lawyer.objects.filter(email=email).exists():
            error = "Sorry Lawyer!! This Email already exists. Please fill up the form again."
            return render(request, 'lawyer_register.html', {'passing_years': passing_years, 'error': error})
        
        if 'image' in request.FILES and image:
            target_dir = "lawyerhub/static/images/upload/"
            new_name = f"{date.today().strftime('%Y%m%d%H%M%S')}_{image.name}"
            target_file = os.path.join(target_dir, new_name)
            upload_ok = 1
            image_file_type = image.name.split('.')[-1].lower()
            
            if not image.content_type.startswith('image'):
                upload_ok = 0
                message = "File must be an image"
                return render(request, 'lawyer_register.html', {'passing_years': passing_years, 'message': message})  
            elif os.path.exists(target_file):
                upload_ok = 0
                message = "File name is already occupied"
                return render(request, 'lawyer_register.html', {'passing_years': passing_years, 'message': message})  
            elif image.size > 5000000:
                upload_ok = 0
                message = "File size must be less than 5MB"
                return render(request, 'lawyer_register.html', {'passing_years': passing_years, 'message': message})  
            elif image_file_type not in ["jpg", "jpeg", "png"]:
                upload_ok = 0
                message = "File extension must be 'jpg', 'jpeg', and 'png'"
                return render(request, 'lawyer_register.html', {'passing_years': passing_years, 'message': message})  
            elif upload_ok == 0:
                message = "Error occurred while uploading image please try again!!!"
                return render(request, 'lawyer_register.html', {'passing_years': passing_years, 'message': message})
            else:
                if upload_ok == 1:
                    with open(target_file, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
                else:
                    message = "Error occurred while uploading image please try again!!!"
                    return render(request, 'lawyer_register.html', {'passing_years': passing_years, 'message': message})
        else:
            new_name = request.POST.get['image']
        
        lawyer = Lawyer.objects.create(lawyer_id=lawyer_id, contact_number=contact_number, university_college=university_college, degree=degree, passing_year=passing_year, full_address=full_address, city=city, zip_code=zip_code, practise_length=practise_length, case_handle=','.join(case_handle), speciality=speciality, image=new_name, first_name=first_name, last_name=last_name, email=email, password=password, status='Pending', role='Lawyer')
            
        if lawyer:
            send_email_lawyer_and_user(request)
            send_message_admin(request)
            success = "Thank you lawyer! You are successfully registered as Lawyer"
            return render(request, 'lawyer_register.html', {'passing_years': passing_years, 'success': success})
    else:
        return render(request, 'lawyer_register.html', {'passing_years': passing_years})

def user_register(request):
    if request.method == 'POST':
        client_id = f"Client_{uuid.uuid4().hex[:8]}"
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact_number = request.POST.get('contact_number')
        image = request.FILES.get('image')
        full_address = request.POST.get('full_address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        
        if Client.objects.filter(email=email).exists():
            error = "Sorry User!! This Email already exists. Please fill up the form again."
            return render(request, 'user_register.html', {'error': error})
        
        if 'image' in request.FILES and image:
            target_dir = "lawyerhub/static/images/upload/"
            new_name = f"{date.today().strftime('%Y%m%d%H%M%S')}_{image.name}"
            target_file = os.path.join(target_dir, new_name)
            upload_ok = 1
            image_file_type = image.name.split('.')[-1].lower()
            
            if not image.content_type.startswith('image'):
                upload_ok = 0
                message = "File must be an image"
                return render(request, 'user_register.html', {'message': message})  
            elif os.path.exists(target_file):
                upload_ok = 0
                message = "File name is already occupied"
                return render(request, 'user_register.html', {'message': message})  
            elif image.size > 5000000:
                upload_ok = 0
                message = "File size must be less than 5MB"
                return render(request, 'user_register.html', {'message': message})  
            elif image_file_type not in ["jpg", "jpeg", "png"]:
                upload_ok = 0
                message = "File extension must be 'jpg', 'jpeg', and 'png'"
                return render(request, 'user_register.html', {'message': message})  
            elif upload_ok == 0:
                message = "Error occurred while uploading image please try again!!!"
                return render(request, 'user_register.html', {'message': message})
            else:
                if upload_ok == 1:
                    with open(target_file, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)
                else:
                    message = "Error occurred while uploading image please try again!!!"
                    return render(request, 'user_register.html', {'message': message})
        else:
            new_name = request.POST.get['image']
        
        client = Client.objects.create(client_id=client_id, contact_number=contact_number, full_address=full_address, city=city, zip_code=zip_code, image=new_name, email=email, first_name=first_name, last_name=last_name, password=password, role='User', status='Active')
            
        if client:
            send_email_lawyer_and_user(request)
            success = "Thank you user! You are successfully registered as User"
            return render(request, 'user_register.html', {'success': success})
    else:
        return render(request, 'user_register.html')

def login(request):
    no = request.session.get('no')
    if 'no' in request.session:
        del request.session['no']
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        lawyer_user = Lawyer.objects.filter(email=email, password=password, status='Active').first()
        if lawyer_user:
            request.session['lawyer_id'] = lawyer_user.lawyer_id
            request.session['login'] = True
            
            if request.session['login'] == True:
                request.session['msg'] = "lawyer"
                request.session['suc'] = "success"
                return redirect('lawyerhub:lawyer_profile')

        client_user = Client.objects.filter(email=email, password=password, status='Active').first()
        if client_user:
            request.session['client_id'] = client_user.client_id
            request.session['login'] = True
            
            if request.session['login'] == True:
                request.session['msg'] = "user"
                request.session['suc'] = "success"
                return redirect('lawyerhub:user_profile')

        admin_user = Administrator.objects.filter(email=email, password=password, status='Active').first()
        if admin_user:
            request.session['login'] = True
            
            if request.session['login'] == True:
                request.session['msg'] = "admin"
                request.session['suc'] = "success"
                return redirect('lawyerhub:admin_dashboard')
    
        message = 'Incorrect email or password'
        return render(request, 'login.html', {'message': message})

    return render(request, 'login.html', {'no': no})

def logout(request):
    request.session['login'] = False
    if request.session['login'] == False:
        request.session['msg'] = "logout"
        
    return redirect('lawyerhub:login')

def lawyer_profile(request):
    msg = request.session.get('msg', '')
    if msg == "lawyer":
        lawyer_id = request.session.get('lawyer_id')
        suc = request.session.get('suc')
        if 'suc' in request.session:
            del request.session['suc']
        
        lawyer_data = Lawyer.objects.filter(lawyer_id=lawyer_id).values().first()
        
        return render(request, 'lawyer_profile.html', {'lawyer_data': lawyer_data, 'suc': suc, 'msg': msg})
    # elif msg == 'logout':
    #     return render(request, 'lawyer_profile.html')
    else:
        request.session['no'] = "lawyer"
        return redirect('lawyerhub:login')

def lawyer_edit_profile(request):
    msg = request.session.get('msg', '')
    if msg == "lawyer":
        passing_years = range(datetime.now().year, 1999, -1)
        
        lawyer_id = request.session.get('lawyer_id')
        
        if request.method == 'POST':
            form_data = {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name', ''),
                'contact_number': request.POST.get('contact_number'),
                'email': request.POST.get('email'),
                'image': request.FILES.get('image'),
                'university_college': request.POST.get('university_college'),
                'degree': request.POST.get('degree'),
                'passing_year': request.POST.get('passing_year'),
                'full_address': request.POST.get('full_address'),
                'city': request.POST.get('city'),
                'zip_code': request.POST.get('zip_code'),
                'practise_length': request.POST.get('practise_length'),
                'case_handle': ','.join(request.POST.getlist('case_handle')),
                'speciality': request.POST.get('speciality'),
            }
            
            if Lawyer.objects.filter(email=form_data['email']).exists():
                error = "Sorry Lawyer!! This Email already exists. Please fill up the form again."
                return render(request, 'lawyer_edit_profile.html', {'passing_years': passing_years, 'error': error, 'msg': msg})
            
            if form_data['image']:
                img = Lawyer.objects.filter(lawyer_id=lawyer_id).values().first()
                img_name = img.get('image', 'Image not available')
                target_dir = "lawyerhub/static/images/upload/"
                target_file = os.path.join(target_dir, img_name)
                
                if os.path.exists(target_file):
                    os.remove(target_file)
            
            if 'image' in request.FILES and form_data['image']:
                target_dir = "lawyerhub/static/images/upload/"
                new_name = f"{date.today().strftime('%Y%m%d%H%M%S')}_{form_data['image'].name}"
                target_file = os.path.join(target_dir, new_name)
                upload_ok = 1
                image_file_type = form_data['image'].name.split('.')[-1].lower()
                
                if not form_data['image'].content_type.startswith('image'):
                    upload_ok = 0
                    message = "File must be an image"
                    return render(request, 'lawyer_edit_profile.html', {'passing_years': passing_years, 'message': message, 'msg': msg})  
                elif os.path.exists(target_file):
                    upload_ok = 0
                    message = "File name is already occupied"
                    return render(request, 'lawyer_edit_profile.html', {'passing_years': passing_years, 'message': message, 'msg': msg})  
                elif form_data['image'].size > 5000000:
                    upload_ok = 0
                    message = "File size must be less than 5MB"
                    return render(request, 'lawyer_edit_profile.html', {'passing_years': passing_years, 'message': message, 'msg': msg})  
                elif image_file_type not in ["jpg", "jpeg", "png", "gif"]:
                    upload_ok = 0
                    message = "File extension must be 'jpg', 'jpeg', 'png', and 'gif'"
                    return render(request, 'lawyer_edit_profile.html', {'passing_years': passing_years, 'message': message, 'msg': msg})  
                elif upload_ok == 0:
                    message = "Error occurred while uploading image please try again!!!"
                    return render(request, 'lawyer_edit_profile.html', {'passing_years': passing_years, 'message': message, 'msg': msg})
                else:
                    if upload_ok == 1:
                        with open(target_file, 'wb+') as destination:
                            for chunk in form_data['image'].chunks():
                                destination.write(chunk)
                    else:
                        message = "Error occurred while uploading image please try again!!!"
                        return render(request, 'lawyer_edit_profile.html', {'passing_years': passing_years, 'message': message, 'msg': msg})
            else:
                new_name = form_data.get('image', '')
                    
            form_data['image'] = new_name
            
            non_empty_fields = {key: value for key, value in form_data.items() if value != '' and value is not None}

            lawyer = Lawyer.objects.filter(lawyer_id=lawyer_id).update(**non_empty_fields)
            if lawyer > 0:
                done = "done"
                return render(request, 'lawyer_edit_profile.html', {'passing_years': passing_years, 'done': done, 'msg': msg})
        else:    
            return render(request, 'lawyer_edit_profile.html', {'passing_years': passing_years, 'msg': msg})
    else:
        request.session['no'] = "lawyer"
        return redirect('lawyerhub:login')

def lawyer_booking(request):
    msg = request.session.get('msg', '')
    if msg == "lawyer":
        lawyer_id = request.session.get('lawyer_id')
        booking_data = Booking.objects.filter(lawyer_id=lawyer_id).all().values()
        
        return render(request, 'lawyer_booking.html', {'booking_data': booking_data, 'msg': msg})
    else:
        request.session['no'] = "lawyer"
        return redirect('lawyerhub:login')

def accept_request(request, booking_id):
    get_ci = Booking.objects.filter(booking_id=booking_id).all()
    Booking.objects.filter(booking_id=booking_id).update(status='Accepted')
    
    for i in get_ci.values():
        ci = i['client_id']
        
    if ci:
        cl = Client.objects.filter(client_id=ci).all()
        
        for j in cl.values():
            first_name = j['first_name']
            last_name = j['last_name']
            email = j['email']
            
            subject = "Notification For Account Information"
            message = f"{first_name} {last_name} your booking request is accepted."

            email_message = EmailMessage(
                subject,
                message,
                "neelmoradiya56@gmail.com",
                [email],
            )

            try:
                email_message.send()
            except Exception as e:
                pass
            
    return redirect('lawyerhub:lawyer_booking')

def update_password_lawyer(request):
    msg = request.session.get('msg', '')
    if msg == "lawyer":
        lawyer_id = request.session.get('lawyer_id')
        if lawyer_id:
            lawyer_data = Lawyer.objects.filter(lawyer_id=lawyer_id).values().first()
            password = lawyer_data.get('password', 'Password not available')
        
        if request.method == 'POST':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if current_password != password:
                error = "Not valid"
                return render(request, 'update_password_lawyer.html', {'error': error, 'msg': msg})
            elif new_password == password:
                error2 = "already exists"
                return render(request, 'update_password_lawyer.html', {'error2': error2, 'msg': msg})
            elif new_password != confirm_password:
                error3 = "must be same"
                return render(request, 'update_password_lawyer.html', {'error3': error3, 'msg': msg})
            else:
                lawyer = Lawyer.objects.filter(lawyer_id=lawyer_id).update(password=new_password)
                
                if lawyer > 0:
                    done = "done"
                    return render(request, 'update_password_lawyer.html', {'done': done, 'msg': msg})
        else:
            return render(request, 'update_password_lawyer.html', {'msg': msg})
    else:
        request.session['no'] = "lawyer"
        return redirect('lawyerhub:login')

def user_profile(request):
    msg = request.session.get('msg', '')
    if msg == "user":
        client_id = request.session.get('client_id')
        suc = request.session.get('suc')
        if 'suc' in request.session:
            del request.session['suc']
        
        client_data = Client.objects.filter(client_id=client_id).values().first()
        
        return render(request, 'user_profile.html', {'client_data': client_data, 'suc': suc, 'msg': msg})
    else:
        request.session['no'] = "user"
        return redirect('lawyerhub:login')

def user_edit_profile(request):
    msg = request.session.get('msg', '')
    if msg == "user":
        client_id = request.session.get('client_id')
        
        if request.method == 'POST':
            form_data = {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name', ''),
                'contact_number': request.POST.get('contact_number'),
                'email': request.POST.get('email'),
                'image': request.FILES.get('image'),
                'full_address': request.POST.get('full_address'),
                'city': request.POST.get('city'),
                'zip_code': request.POST.get('zip_code'),
            }
            
            if Client.objects.filter(email=form_data['email']).exists():
                error = "Sorry User!! This Email already exists. Please fill up the form again."
                return render(request, 'user_edit_profile.html', {'error': error, 'msg': msg})
            
            if form_data['image']:
                img = Client.objects.filter(client_id=client_id).values().first()
                img_name = img.get('image', 'Image not available')
                target_dir = "lawyerhub/static/images/upload/"
                target_file = os.path.join(target_dir, img_name)
                
                if os.path.exists(target_file):
                    os.remove(target_file)
                    
            if 'image' in request.FILES and form_data['image']:
                target_dir = "lawyerhub/static/images/upload/"
                new_name = f"{date.today().strftime('%Y%m%d%H%M%S')}_{form_data['image'].name}"
                target_file = os.path.join(target_dir, new_name)
                upload_ok = 1
                image_file_type = form_data['image'].name.split('.')[-1].lower()
                
                if not form_data['image'].content_type.startswith('image'):
                    upload_ok = 0
                    message = "File must be an image"
                    return render(request, 'user_edit_profile.html', {'message': message, 'msg': msg})  
                elif os.path.exists(target_file):
                    upload_ok = 0
                    message = "File name is already occupied"
                    return render(request, 'user_edit_profile.html', {'message': message, 'msg': msg})  
                elif form_data['image'].size > 5000000:
                    upload_ok = 0
                    message = "File size must be less than 5MB"
                    return render(request, 'user_edit_profile.html', {'message': message, 'msg': msg})  
                elif image_file_type not in ["jpg", "jpeg", "png", "gif"]:
                    upload_ok = 0
                    message = "File extension must be 'jpg', 'jpeg', 'png', and 'gif'"
                    return render(request, 'user_edit_profile.html', {'message': message, 'msg': msg})  
                elif upload_ok == 0:
                    message = "Error occurred while uploading image please try again!!!"
                    return render(request, 'user_edit_profile.html', {'message': message, 'msg': msg})
                else:
                    if upload_ok == 1:
                        with open(target_file, 'wb+') as destination:
                            for chunk in form_data['image'].chunks():
                                destination.write(chunk)
                    else:
                        message = "Error occurred while uploading image please try again!!!"
                        return render(request, 'user_edit_profile.html', {'message': message, 'msg': msg})
            else:
                new_name = form_data.get('image', '')
                    
            form_data['image'] = new_name
            
            non_empty_fields = {key: value for key, value in form_data.items() if value != '' and value is not None}

            client = Client.objects.filter(client_id=client_id).update(**non_empty_fields)
            if client > 0:
                done = "done"
                return render(request, 'user_edit_profile.html', {'done': done, 'msg': msg})
        else:
            return render(request, 'user_edit_profile.html', {'msg': msg})
    else:
        request.session['no'] = "user"
        return redirect('lawyerhub:login')

def user_booking(request):
    msg = request.session.get('msg', '')
    if msg == "user":
        client_id = request.session.get('client_id')
        success = request.session.get('success')
        if 'success' in request.session:
            del request.session['success']
        
        booking_data = Booking.objects.filter(client_id=client_id).all().values()
        
        return render(request, 'user_booking.html', {'booking_data': booking_data, 'success': success, 'msg': msg})
    else:
        request.session['no'] = "user"
        return redirect('lawyerhub:login')

def update_password_user(request):
    msg = request.session.get('msg', '')
    if msg == "user":
        client_id = request.session.get('client_id')
        
        if client_id:
            client_data = Client.objects.filter(client_id=client_id).values().first()
            password = client_data.get('password', 'Password not available')
            
        if request.method == 'POST':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if current_password != password:
                error = "Not valid"
                return render(request, 'update_password_user.html', {'error': error, 'msg': msg})
            elif new_password == password:
                error2 = "already exists"
                return render(request, 'update_password_user.html', {'error2': error2, 'msg': msg})
            elif new_password != confirm_password:
                error3 = "must be same"
                return render(request, 'update_password_user.html', {'error3': error3, 'msg': msg})
            else:
                client = Client.objects.filter(client_id=client_id).update(password=new_password)
                if client > 0:
                    done = "done"
                    return render(request, 'update_password_user.html', {'done': done, 'msg': msg})
        else:
            return render(request, 'update_password_user.html', {'msg': msg})
    else:
        request.session['no'] = "user"
        return redirect('lawyerhub:login')

def admin_dashboard(request):
    msg = request.session.get('msg', '')
    if msg == "admin":
        suc = request.session.get('suc')
        if 'suc' in request.session:
            del request.session['suc']
            
        lawyer_data = Lawyer.objects.all().values()
        user_data = Client.objects.all().values()
        booking_data = Booking.objects.all().values()
        
        formatted_lawyer_data = get_formatted_data(lawyer_data.values())
        formatted_user_data = get_formatted_data(user_data.values())
        
        # Convert dates to string format for display
        booking_data = list(booking_data)
        for entry in booking_data:
            for key, value in entry.items():
                if isinstance(value, date):
                    entry[key] = value.strftime('%Y-%m-%d')
                    
        formatted_booking_data = get_formatted_data(booking_data)
        
        return render(request, 'admin_dashboard.html', {'lawyer_data': formatted_lawyer_data, 'user_data': formatted_user_data, 'booking_data': formatted_booking_data, 'suc': suc, 'msg': msg})
    else:
        request.session['no'] = "admin"
        return redirect('lawyerhub:login')

def admin_user(request):
    msg = request.session.get('msg', '')
    if msg == "admin":
        user_data = Client.objects.all().values()
        
        return render(request, 'admin_user.html', {'user_data': user_data, 'msg': msg})
    else:
        request.session['no'] = "admin"
        return redirect('lawyerhub:login')
 
def block_user(request, c_id):
    client = Client.objects.filter(client_id=c_id).all()
    update = Client.objects.filter(client_id=c_id).update(status='Block')
    if update:
        for i in client.values():
            first_name = i['first_name']
            last_name = i['last_name']
            email = i['email']
            
        subject = "Notification For Account Information"
        message = f"{first_name} {last_name} your are Blocked by administrator."

        email_message = EmailMessage(
            subject,
            message,
            "neelmoradiya56@gmail.com",
            [email],
        )

        try:
            email_message.send()
        except Exception as e:
            pass
        
        return redirect('lawyerhub:admin_user')

def unblock_user(request, c_id):
    client = Client.objects.filter(client_id=c_id).all()
    update = Client.objects.filter(client_id=c_id).update(status='Active')
    if update:
        for i in client.values():
            first_name = i['first_name']
            last_name = i['last_name']
            email = i['email']
            
        subject = "Notification For Account Information"
        message = f"{first_name} {last_name} your are Unblocked by administrator."

        email_message = EmailMessage(
            subject,
            message,
            "neelmoradiya56@gmail.com",
            [email],
        )

        try:
            email_message.send()
        except Exception as e:
            pass
        
        return redirect('lawyerhub:admin_user')

def admin_lawyer(request):
    msg = request.session.get('msg', '')
    if msg == "admin":
        lawyer_data = Lawyer.objects.all().values()
        
        return render(request, 'admin_lawyer.html', {'lawyer_data': lawyer_data, 'msg': msg})
    else:
        request.session['no'] = "admin"
        return redirect('lawyerhub:login')

def send_confirm_mail_lawyer(request, lawyer):
    first_name = lawyer.get('first_name', 'first_name not available')
    last_name = lawyer.get('last_name', 'last_name not available')
    email = lawyer.get('email', 'email not available')
    password = lawyer.get('password', 'password not available')

    subject = "Notification For Account Information"
    message = render_to_string('send_confirm_mail_lawyer.html', {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
    })

    email_message = EmailMessage(
        subject,
        message,
        "neelmoradiya56@gmail.com",
        [email],
    )
    
    email_message.content_subtype = 'html'

    try:
        email_message.send()
    except Exception as e:
        pass

def approve_lawyer(request, law_id):
    lawyer = Lawyer.objects.filter(lawyer_id=law_id).values().first()
    if lawyer:            
        send_confirm_mail_lawyer(request, lawyer)
        Lawyer.objects.filter(lawyer_id=law_id).update(status='Active')
        return redirect('lawyerhub:admin_lawyer')

def feedbacks(request):
    msg = request.session.get('msg', '')
    if msg == "admin":
        feedbacks = Feedback.objects.all().values()
        
        return render(request, 'feedbacks.html', {'feedbacks': feedbacks, 'msg': msg})
    else:
        request.session['no'] = "admin"
        return redirect('lawyerhub:login')
