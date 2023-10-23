from django.core.management.base import BaseCommand
from Menu.models import PaymentOption, SettlementType, SettlementMode, OrderOption, WorkingTime   # Import your PaymentOptions model here
from User.models import Roles

class Command(BaseCommand):
    help = 'Seed Roles, Payment Methods and others data'

    def handle(self, *args, **kwargs):
        # Define the PaymentOptions data
        payment_options_data = [
            {'name': 'Cash on Delivary'},
            {'name': 'Online Payment'},
            {'name': 'UPI Payment'}
        ]

        # Loop through the data and create PaymentOptions objects
        for option_data in payment_options_data:
            PaymentOption.objects.create(**option_data)

        settlement_types_data = [
            {'name': 'Daily'},
            {'name': 'Weekly'}
        ]

        # Loop through the data and create PaymentOptions objects
        for option_data in settlement_types_data:
            SettlementType.objects.create(**option_data)  

        settlement_modes_data = [
            {'name': 'Cash'},
            {'name': 'Bank Transfer'}
        ]

        # Loop through the data and create PaymentOptions objects
        for option_data in settlement_modes_data:
            SettlementMode.objects.create(**option_data)      

        order_options_data = [
            {'name': 'Pick-Up'},
            {'name': 'Home Delivary'}
        ]

        # Loop through the data and create PaymentOptions objects
        for option_data in order_options_data:
            OrderOption.objects.create(**option_data)  

        working_times_data = [
            {'name': 'Hotel Available Time'},
            {'name': 'Breakfast Time'},
            {'name': 'Lunch Time'},
            {'name': 'Dinner Time'}
        ]

        # Loop through the data and create PaymentOptions objects
        for option_data in working_times_data:
            WorkingTime.objects.create(**option_data) 

        roles = [
            {'name': 'Super Admin'},
            {'name': 'Manager'},
            {'name': 'Delivery Boy'},
            {'name': 'Customer'}
        ]

        for role in roles:
            Roles.objects.create(**role)                  

        self.stdout.write(self.style.SUCCESS('Seeding Data All Completed'))
