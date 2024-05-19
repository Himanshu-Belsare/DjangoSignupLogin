from rest_framework import viewsets,status
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from datetime import timezone, timedelta
import random
from UserAuth import utils

class UserAuthViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    @action(detail=True,methods=['PATCH'])
    def verify_otp(self,request,pk=None):
        instance = self.get_object()

        if(
            not instance.is_active
            and instance.otp == request.data.get("otp")
            and instance.otp_expiry
            and timezone.now() < instance.otp_expiry
        ):
            instance.is_active = True
            instance.otp_expiry = None
            instance.max_otp_try = settings.MAX_OTP_TRY
            instance.otp_max_out = None
            instance.save()
            return Response("Successfully verified the user",status=status.HTTP_200_OK)
        return Response("something went wrong", status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True,methods=['PATCH'])
    def regenerate_otp(self,request,pk=None):
        breakpoint()
        instance = self.get_object()
        if int(instance.max_otp_try) == 0 and timezone.now() < instance.otp_max_out:
            return Response("Max otp try reached, try after one hour", status=status.HTTP_400_BAD_REQUEST)
        otp = random.randint(1000,9999)
        otp_expiry = timezone.now() + timedelta(minutes=10)
        max_otp_try = int(instance.max_otp_try) - 1

        instance.otp =otp
        instance.otp_expiry = otp_expiry
        instance.max_otp_try = max_otp_try

        if max_otp_try == 0:
            instance.otp_max_out = timezone.now() + timedelta(hours=1)
        elif max_otp_try == -1:
            instance.max_otp_try = settings.MAX_OTP_TRY 
        else:
            instance.max_otp_try = max_otp_try
            instance.otp_max_out = None
        instance.save()
        breakpoint()
        utils.send_otp(instance.phone_number,otp)
        return Response("successfully regenerated the new OTP", status=status.HTTP_200_OK)
        

    