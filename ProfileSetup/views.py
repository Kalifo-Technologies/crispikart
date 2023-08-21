from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from ProfileSetup.models import PaymentOption, SettlementType, SettlementMode, OrderOption, PrivateInformation, PublicInformation, RestorantImage, WorkingTimeDetail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import re

def index(request):
    profile_information = PublicInformation.objects.all()
    paginator = Paginator(profile_information, 3)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    nums = 'a' * page.paginator.num_pages

    profileInformationCount = PrivateInformation.objects.count()

    return render(request, 'pages/profiles/index.html', {"profileInformationCount": profileInformationCount, "profiles": page, "nums": nums})

def create(request):
    return render(request, 'pages/profiles/create.html')

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
        payment_options = req.getlist('payment_options[]')
        settlement_types = req.getlist('settlement_types[]')
        settlement_modes = req.getlist('settlement_modes[]')
        restorant_images = request.FILES.getlist('restorant_images[]')
        restorant_name = req.get('restorant_name')
        address = req.get('address')
        working_times = req.getlist('working_times[]')
        order_options = req.getlist('order_options[]')
        public_contact_no = req.get('public_contact_no')
        public_whatsapp_no = req.get('public_whatsapp_no')
        restorant_email = req.get('restorant_email')

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
            "old_address": address
        }

        try:

            validation_errors = {}
            if not owner_name:
                validation_errors['owner_name'] = 'Owner name field is required'   
            if not private_contact_no:
                validation_errors['private_contact_no'] = 'Contact no field is required'
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
                validation_errors['manager_contact_no'] = 'Manager contact no is required'
            if not restorant_name:
                validation_errors['restorant_name'] = 'Restorant name field is required'    
            if not public_contact_no:
                validation_errors['public_contact_no'] = 'Contact no field is required'
            if not public_whatsapp_no:
                validation_errors['public_whatsapp_no'] = 'Whatsapp no field is required'
            if not restorant_email:
                validation_errors['restorant_email'] = 'Email field is required'
            if not re.match(r"[^@]+@[^@]+\.[^@]+", restorant_email):
                validation_errors['restorant_email'] = 'Invalid email address.'
            if validation_errors:
                return render(request, 'pages/profiles/create.html', {"validation_errors": validation_errors, "context": context})
            
            private_information = PrivateInformation.objects.create(
                user = request.user,
                profile = profile_pic,
                owner_name = owner_name,
                contact_no = private_contact_no,
                whatsapp_no = private_whatsapp_no,
                email = private_email,
                established_year = established_year,                
                no_of_employees = no_of_employees,
                manager_name = manager_name,
                manager_contact_no = manager_contact_no
            )

            # if payment_options is not None:
            for payment_option in payment_options:
                PaymentOption.objects.create(
                    private_information = private_information,
                    name = payment_option
                )

            # if settlement_types is not None:
            for settlement_type in settlement_types:         
                SettlementType.objects.create(
                    private_information = private_information,
                    name = settlement_type
                )

            # if settlement_modes is not None:
            for settlement_mode in settlement_modes:
                SettlementMode.objects.create(
                    private_information = private_information,
                    name = settlement_mode
                )


            public_information = PublicInformation.objects.create(
                user = request.user,
                private_information = private_information,
                restorant_name = restorant_name,
                address = address,
                contact_no = public_contact_no,
                whatsapp_no = public_whatsapp_no,
                email = restorant_email
            )    

            for resImage in restorant_images:
                RestorantImage.objects.create(
                    public_information = public_information,
                    images = resImage,
                )

            for workingTime in working_times:
                WorkingTimeDetail.objects.create(
                    public_information = public_information,
                    working_time = workingTime
                )       

            for option in order_options:
                 OrderOption.objects.create(
                    public_information = public_information,
                    name = option
                 )

            messages.success(request, 'Profile Information saved successfully')

            return redirect('profiles')  

        except ValidationError as e:
            error_message = e.message
            return render(request, 'pages/profiles/create.html', {"validation_errors": validation_errors})

        # return redirect('profiles')    
    
def editProfile(request, id):
    profile_information = PublicInformation.objects.get(private_information_id = id)
    settlementModes = SettlementMode.objects.filter(private_information_id = id)
    paymentOptions = PaymentOption.objects.filter(private_information_id = id)
    settlementTypes = SettlementType.objects.filter(private_information_id = id)
    workingTimeDetails = WorkingTimeDetail.objects.filter(public_information_id = profile_information.id)
    orderOptions = OrderOption.objects.filter(public_information_id = profile_information.id)
    restorantFirstImage = RestorantImage.objects.filter(public_information_id = profile_information.id).first()
    restorant_images = RestorantImage.objects.filter(public_information_id = profile_information.id)


    return render(request, 'pages/profiles/edit.html', {
                                                            "profile": profile_information, 
                                                            "settlementModes": settlementModes, 
                                                            "paymentOptions": paymentOptions,
                                                            "settlementTypes": settlementTypes, 
                                                            "workingTimeDetails": workingTimeDetails,
                                                            "orderOptions": orderOptions,
                                                            "restorantFirstImage": restorantFirstImage,
                                                            "restorant_images": restorant_images,
                                                        
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
        restorant_images = request.FILES.getlist('restorant_images[]')
        editRestorantImagesField = req.getlist('editRestorantImagesField[]')
        restorant_name = req.get('restorant_name')
        address = req.get('address')
        working_times = req.getlist('working_times[]')
        order_options = req.getlist('order_options[]')
        public_contact_no = req.get('public_contact_no')
        public_whatsapp_no = req.get('public_whatsapp_no')
        restorant_email = req.get('restorant_email')

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
            "old_address": address
        }

        try:

            validation_errors = {}
            if not owner_name:
                validation_errors['owner_name'] = 'Owner name field is required'   
            if not private_contact_no:
                validation_errors['private_contact_no'] = 'Contact no field is required'
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
                validation_errors['manager_contact_no'] = 'Manager contact no is required'
            if not restorant_name:
                validation_errors['restorant_name'] = 'Restorant name field is required'    
            if not public_contact_no:
                validation_errors['public_contact_no'] = 'Contact no field is required'
            if not public_whatsapp_no:
                validation_errors['public_whatsapp_no'] = 'Whatsapp no field is required'
            if not restorant_email:
                validation_errors['restorant_email'] = 'Email field is required'
            if not re.match(r"[^@]+@[^@]+\.[^@]+", restorant_email):
                validation_errors['restorant_email'] = 'Invalid email address.'
            if validation_errors:
                return render(request, 'pages/profiles/create.html', {"validation_errors": validation_errors, "context": context})
            
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
            

            PaymentOption.objects.filter(private_information = id).delete()
            # if payment_options is not None:
            for payment_option in payment_options:
                PaymentOption.objects.create(
                    private_information = private_information,
                    name = payment_option
                )

            SettlementType.objects.filter(private_information = id).delete()
            # if settlement_types is not None:
            for settlement_type in settlement_types:         
                SettlementType.objects.create(
                    private_information = private_information,
                    name = settlement_type
                )

            SettlementMode.objects.filter(private_information = id).delete()
            # if settlement_modes is not None:
            for settlement_mode in settlement_modes:
                SettlementMode.objects.create(
                    private_information = private_information,
                    name = settlement_mode
                )


            public_information = PublicInformation.objects.get(private_information = id)
            public_information.user = request.user
            public_information.private_information = private_information
            public_information.restorant_name = restorant_name
            public_information.address = address
            public_information.contact_no = public_contact_no
            public_information.whatsapp_no = public_whatsapp_no
            public_information.email = restorant_email
            public_information.save()

            if len(editRestorantImagesField) > 0:
                RestorantImage.objects.filter(public_information = public_information).delete()
                for resImage in editRestorantImagesField:
                    RestorantImage.objects.create(
                        public_information = public_information,
                        images = resImage,
                    )
            else:
                for resImage in restorant_images:
                    RestorantImage.objects.create(
                        public_information = public_information,
                        images = resImage,
                    )

            WorkingTimeDetail.objects.filter(public_information = public_information).delete()
            for workingTime in working_times:
                WorkingTimeDetail.objects.create(
                    public_information = public_information,
                    working_time = workingTime
                )       
            OrderOption.objects.filter(public_information = public_information).delete()
            for option in order_options:
                 OrderOption.objects.create(
                    public_information = public_information,
                    name = option
                 )

            messages.success(request, 'Profile Information updated successfully')

            return redirect('profiles')  

        except ValidationError as e:
            error_message = e.message
            return render(request, 'pages/profiles/create.html', {"validation_errors": validation_errors})


def deleteProfile(request):
    delete_id = request.POST.get('id')
    profile = PrivateInformation.objects.get(id = delete_id)
    profile.delete()
    return JsonResponse({"message": "Order Status deleted successfully"})