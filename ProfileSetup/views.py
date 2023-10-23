from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from ProfileSetup.models import PaymentOptionDetail, SettlementTypeDetail, SettlementModeDetail, OrderOptionDetail, PrivateInformation, PublicInformation, RestorantImage, WorkingTimeDetail
from Menu.models import PaymentOption, SettlementType, SettlementMode, OrderOption, WorkingTime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password
import re
from django.core.validators import RegexValidator

def index(request):
    items_per_page = 10
    profile_information = PublicInformation.objects.all()
    paginator = Paginator(profile_information, items_per_page)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    nums = 'a' * page.paginator.num_pages

    profileInformationCount = PrivateInformation.objects.count()

    return render(request, 'pages/profiles/index.html', {"profileInformationCount": profileInformationCount, "profiles": page, "nums": nums})

def create(request):

    settlement_modes = SettlementMode.objects.all()
    settlement_types = SettlementType.objects.all()
    order_options = OrderOption.objects.all()
    payment_options = PaymentOption.objects.all()
    working_times = WorkingTime.objects.all()

    return render(request, 'pages/profiles/create.html', {
        'settlement_types': settlement_types,
        'settlement_modes': settlement_modes,
        'order_options': order_options,
        'payment_options': payment_options,
        'working_times': working_times
    })

def addProfile(request):

    if request.method == "POST":
        
        req = request.POST
        profile_pic = request.FILES.get('profile_image')
        owner_name = req.get('owner_name')
        private_contact_no = req.get('private_contact_no')
        private_whatsapp_no = req.get('private_whatsapp_no')
        private_email = req.get('private_email')
        established_year = req.get('established_year')
        no_of_employees = req.get('no_of_employees')
        manager_name = req.get('manager_name')
        manager_contact_no = req.get('manager_contact_no')
        paymentOptions = req.getlist('payment_options[]')
        settlementTypes = req.getlist('settlement_types[]')
        settlementModes = req.getlist('settlement_modes[]')
        restorant_images = request.FILES.getlist('restorant_images[]')
        restorant_name = req.get('restorant_name')
        address = req.get('address')
        workingTimes = req.getlist('working_times[]')
        orderOptions = req.getlist('order_options[]')
        public_contact_no = req.get('public_contact_no')
        public_whatsapp_no = req.get('public_whatsapp_no')
        restorant_email = req.get('restorant_email')
        location = req.get('location')
        username = req.get('username')
        password = req.get('password')
        confirm_password = req.get('confirm_password')

        context = {
            "old_owner_name": owner_name,
            "old_private_contact_no": private_contact_no,
            "old_private_whatsapp_no": private_whatsapp_no,
            "old_private_email" : private_email,
            "old_established_year": established_year,
            "old_no_of_employees": no_of_employees,
            "old_manager_name": manager_name,
            "old_manager_contact_no": manager_contact_no,
            "old_private_whatsapp_no": private_whatsapp_no,
            "old_restorant_name": restorant_name,
            "old_public_contact_no": public_contact_no,
            "old_public_whatsapp_no": public_whatsapp_no,
            "old_restorant_email": restorant_email,
            "old_address": address,
            "old_location": location,
            "old_username": username,
            "old_restaurant_images": restorant_images
        }

        settlement_modes = SettlementMode.objects.all()
        settlement_types = SettlementType.objects.all()
        order_options = OrderOption.objects.all()
        payment_options = PaymentOption.objects.all()
        working_times = WorkingTime.objects.all()    

        validator = RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+1234567890'. Up to 15 digits allowed."
        )

        try:

            validation_errors = {}
            if not owner_name:
                validation_errors['owner_name'] = 'Owner name field is required'   
            if not private_contact_no:
                validation_errors['private_contact_no'] = 'Private Contact no field is required'
            if len(private_contact_no) > 10 and not private_contact_no.isdigit():
                validation_errors['private_contact_no'] = 'Invalid Private Contact no format.'    
            if not private_email:
                validation_errors['private_email'] = 'Email ID field is required'
            if not re.match(r"[^@]+@[^@]+\.[^@]+", private_email):
                validation_errors['private_email'] = 'Invalid email address.'    
            if not established_year:
                validation_errors['established_year'] = 'Established year field is required'
            if not no_of_employees:
                validation_errors['no_of_employees'] = 'No of employees is required'    
            if not manager_name:
                validation_errors['manager_name'] = 'Manager name field is required'
            if not manager_contact_no:
                validation_errors['manager_contact_no'] = 'Manager contact no field is required'
            if len(manager_contact_no) > 10 and not manager_contact_no.isdigit():
                validation_errors['manager_contact_no'] = 'Invalid Manager Contact no format.'    
            if not restorant_name:
                validation_errors['restorant_name'] = 'Restorant name field is required'    
            if not public_contact_no:
                validation_errors['public_contact_no'] = 'Public Contact no field is required'
            if len(public_contact_no) > 10 and not public_contact_no.isdigit():
                validation_errors['public_contact_no'] = 'Invalid Public Contact no format.'      
            if not public_whatsapp_no:
                validation_errors['public_whatsapp_no'] = 'Whatsapp no field is required'
            if not restorant_email:
                validation_errors['restorant_email'] = 'Email field is required'
            if not re.match(r"[^@]+@[^@]+\.[^@]+", restorant_email):
                validation_errors['restorant_email'] = 'Invalid email address.'
            if not username:
                validation_errors['username'] = 'username field is required'
            if User.objects.filter(username=username).exists():
                validation_errors['username'] = 'username is already exist with same name'
            if not password:
                validation_errors['password'] = 'password field is required'   
            if password != confirm_password:
                validation_errors['password'] = 'passwords do not match'         
            if validation_errors:
                return render(request, 'pages/profiles/create.html', 
                    {
                        "validation_errors": validation_errors, 
                        "context": context,
                        'settlement_types': settlement_types,
                        'settlement_modes': settlement_modes,
                        'order_options': order_options,
                        'payment_options': payment_options,
                        'working_times': working_times
                    }
                )

            user = User.objects.create_user(
                username = username,
                email = restorant_email,
                password = password
            )    
            
            private_information = PrivateInformation.objects.create(
                super_admin = request.user.id,
                user = user,
                profile = profile_pic,
                owner_name = owner_name,
                contact_no = private_contact_no,
                whatsapp_no = private_whatsapp_no,
                email = private_email,
                established_year = established_year,                
                no_of_employees = no_of_employees,
                manager_name = manager_name,
                manager_contact_no = manager_contact_no,
                is_active = True
            )

            # if payment_options is not None:
            for payment_option in paymentOptions:
                PaymentOptionDetail.objects.create(
                    private_information = private_information,
                    payment_option = payment_option
                )

            # if settlement_types is not None:
            for settlement_type in settlementTypes:         
                SettlementTypeDetail.objects.create(
                    private_information = private_information,
                    settlement_type = settlement_type
                )

            # if settlement_modes is not None:
            for settlement_mode in settlementModes:
                SettlementModeDetail.objects.create(
                    private_information = private_information,
                    settlement_mode = settlement_mode
                )


            public_information = PublicInformation.objects.create(
                super_admin = request.user.id,
                user = user,
                private_information = private_information,
                restorant_name = restorant_name,
                address = address,
                contact_no = public_contact_no,
                whatsapp_no = public_whatsapp_no,
                email = restorant_email,
                location = location
            )    

            for resImage in restorant_images:
                RestorantImage.objects.create(
                    public_information = public_information,
                    images = resImage,
                )

            for workingTime in workingTimes:
                WorkingTimeDetail.objects.create(
                    public_information = public_information,
                    working_time = workingTime
                )       

            for option in orderOptions:
                 OrderOptionDetail.objects.create(
                    public_information = public_information,
                    order_option = option
                 )

            messages.success(request, 'Profile saved successfully')

            return redirect('profiles')  

        except ValidationError as e:
            error_message = e.message
            return render(request, 'pages/profiles/create.html', {"validation_errors": validation_errors, "context": context})

        # return redirect('profiles')    
    
def editProfile(request, id):
    profile_information = PublicInformation.objects.get(private_information_id = id)
    settlementModes = SettlementModeDetail.objects.filter(private_information_id = id)
    paymentOptions = PaymentOptionDetail.objects.filter(private_information_id = id)
    settlementTypes = SettlementTypeDetail.objects.filter(private_information_id = id)
    workingTimeDetails = WorkingTimeDetail.objects.filter(public_information_id = profile_information.id)
    orderOptions = OrderOptionDetail.objects.filter(public_information_id = profile_information.id)
    restorantFirstImage = RestorantImage.objects.filter(public_information_id = profile_information.id).first()
    restorant_images = RestorantImage.objects.filter(public_information_id = profile_information.id)

    settlement_modes = SettlementMode.objects.all()
    settlement_types = SettlementType.objects.all()
    order_options = OrderOption.objects.all()
    payment_options = PaymentOption.objects.all()
    working_times = WorkingTime.objects.all()
    

    return render(request, 'pages/profiles/edit.html', {
                                                            "profile": profile_information, 
                                                            "settlementModes": settlementModes, 
                                                            "paymentOptions": paymentOptions,
                                                            "settlementTypes": settlementTypes, 
                                                            "workingTimeDetails": workingTimeDetails,
                                                            "orderOptions": orderOptions,
                                                            "restorantFirstImage": restorantFirstImage,
                                                            "restorant_images": restorant_images,
                                                            'settlement_types': settlement_types,
                                                            'settlement_modes': settlement_modes,
                                                            'order_options': order_options,
                                                            'payment_options': payment_options,
                                                            'working_times': working_times
                                                        }
    )


def updateProfile(request, id):

    if request.method == "POST":
        
        req = request.POST
        owner_name = req.get('owner_name')
        private_contact_no = req.get('private_contact_no')
        private_whatsapp_no = req.get('private_whatsapp_no')
        private_email = req.get('private_email')
        established_year = req.get('established_year')
        no_of_employees = req.get('no_of_employees')
        manager_name = req.get('manager_name')
        manager_contact_no = req.get('manager_contact_no')
        payment_options = req.getlist('payment_options[]')
        settlement_types = req.getlist('settlement_types[]')
        settlement_modes = req.getlist('settlement_modes[]')

        editRestorantImagesField = req.getlist('editRestorantImagesField[]')
        restorant_name = req.get('restorant_name')
        address = req.get('address')
        working_times = req.getlist('working_times[]')
        order_options = req.getlist('order_options[]')
        public_contact_no = req.get('public_contact_no')
        public_whatsapp_no = req.get('public_whatsapp_no')
        restorant_email = req.get('restorant_email')
        location = req.get('location')
        publicInfo = get_object_or_404(PublicInformation, private_information=id)

        context = {
            "old_owner_name": owner_name,
            "old_private_contact_no": private_contact_no,
            "old_private_whatsapp_no": private_whatsapp_no,
            "old_private_email" : private_email,
            "old_established_year": established_year,
            "old_no_of_employees": no_of_employees,
            "old_manager_name": manager_name,
            "old_manager_contact_no": manager_contact_no,
            "old_private_whatsapp_no": private_whatsapp_no,
            "old_restorant_name": restorant_name,
            "old_public_contact_no": public_contact_no,
            "old_public_whatsapp_no": public_whatsapp_no,
            "old_restorant_email": restorant_email,
            "old_address": address,
            "old_location": location
        }

        try:

            validation_errors = {}
            if not owner_name:
                validation_errors['owner_name'] = 'Owner name field is required'   
            if not private_contact_no:
                validation_errors['private_contact_no'] = 'Private Contact no field is required'
            if len(private_contact_no) > 10 and not private_contact_no.isdigit():
                validation_errors['private_contact_no'] = 'Invalid Private Contact no format.'    
            if not private_email:
                validation_errors['private_email'] = 'Email ID field is required'
            if not re.match(r"[^@]+@[^@]+\.[^@]+", private_email):
                validation_errors['private_email'] = 'Invalid email address.'    
            if not established_year:
                validation_errors['established_year'] = 'Established year field is required'
            if not no_of_employees:
                validation_errors['no_of_employees'] = 'No of employees is required'    
            if not manager_name:
                validation_errors['manager_name'] = 'Manager name field is required'
            if not manager_contact_no:
                validation_errors['manager_contact_no'] = 'Manager contact no field is required'
            if len(manager_contact_no) > 10 and not manager_contact_no.isdigit():
                validation_errors['manager_contact_no'] = 'Invalid Manager Contact no format.'      
            if not restorant_name:
                validation_errors['restorant_name'] = 'Restorant name field is required'    
            if not public_contact_no:
                validation_errors['public_contact_no'] = 'Public Contact no field is required'
            if len(public_contact_no) > 10 and not public_contact_no.isdigit():
                validation_errors['public_contact_no'] = 'Invalid Public Contact no format.'     
            if not public_whatsapp_no:
                validation_errors['public_whatsapp_no'] = 'Whatsapp no field is required'
            if not restorant_email:
                validation_errors['restorant_email'] = 'Email field is required'
            if not re.match(r"[^@]+@[^@]+\.[^@]+", restorant_email):
                validation_errors['restorant_email'] = 'Invalid email address.'
                  
            if validation_errors:
                return render(request, 'pages/profiles/edit.html', 
                              {
                                  "validation_errors": validation_errors, 
                                  "context": context,
                                  "settlement_types": settlement_types,
                                  "settlement_modes": settlement_modes,
                                  "order_options": order_options,
                                  "payment_options": payment_options,
                                  "working_times": working_times
                              }
                            )
            
            private_information = PrivateInformation.objects.get(id = id)
            profile_pic = request.FILES.get('profile_image', private_information.profile)
            private_information.user_id = request.user
            private_information.profile = profile_pic
            private_information.owner_name = owner_name
            private_information.contact_no = private_contact_no
            private_information.whatsapp_no = private_whatsapp_no
            private_information.email = private_email
            private_information.established_year = established_year                
            private_information.no_of_employees = no_of_employees
            private_information.manager_name = manager_name
            private_information.manager_contact_no = manager_contact_no
            private_information.save()
            
            

            PaymentOptionDetail.objects.filter(private_information = id).delete()
            # if payment_options is not None:
            for payment_option in payment_options:
                PaymentOptionDetail.objects.create(
                    private_information = private_information,
                    payment_option = payment_option
                )

            SettlementTypeDetail.objects.filter(private_information = id).delete()
            # if settlement_types is not None:
            for settlement_type in settlement_types:         
                SettlementTypeDetail.objects.create(
                    private_information = private_information,
                    settlement_type = settlement_type
                )

            SettlementModeDetail.objects.filter(private_information = id).delete()
            # if settlement_modes is not None:
            for settlement_mode in settlement_modes:
                SettlementModeDetail.objects.create(
                    private_information = private_information,
                    settlement_mode = settlement_mode
                )


            public_information = PublicInformation.objects.get(private_information = id)
            public_information.user = request.user
            public_information.private_information = private_information
            public_information.restorant_name = restorant_name
            public_information.address = address
            public_information.contact_no = public_contact_no
            public_information.whatsapp_no = public_whatsapp_no
            public_information.email = restorant_email
            public_information.location = location
            public_information.save()

            restorant_images = []    
            if 'restorant_images[]' in request.FILES and request.FILES['restorant_images[]']:
                rImages = RestorantImage.objects.filter(public_information = publicInfo)
                if len(rImages) > 0:
                    for im in rImages:
                        restorant_images = request.FILES.getlist('restorant_images[]', im.images)
                    
                        RestorantImage.objects.filter(public_information = public_information).delete()
                        for resImage in restorant_images:
                            RestorantImage.objects.create(
                                public_information = public_information,
                                images = resImage
                            )
                else:

                    restorant_images = request.FILES.getlist('restorant_images[]')
                    for resImage in restorant_images:
                        RestorantImage.objects.create(
                            public_information = public_information,
                            images = resImage
                        )


            WorkingTimeDetail.objects.filter(public_information = public_information).delete()
            for workingTime in working_times:
                WorkingTimeDetail.objects.create(
                    public_information = public_information,
                    working_time = workingTime
                )       
            OrderOptionDetail.objects.filter(public_information = public_information).delete()
            for option in order_options:
                 OrderOptionDetail.objects.create(
                    public_information = public_information,
                    order_option = option
                 )

            messages.success(request, 'Profile updated successfully')

            return redirect('profiles')  

        except ValidationError as e:
            error_message = e.message
            return render(request, 'pages/profiles/edit.html', {"validation_errors": validation_errors, "context": context})


def deleteProfile(request):
    delete_id = request.POST.get('id')
    profile = PrivateInformation.objects.get(id = delete_id)
    profile.delete()
    return JsonResponse({"message": "Profile deleted successfully"})