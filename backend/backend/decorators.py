from authentication.models import CandidateProfile, InterviewerProfile
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


def profile_complete(func):

    def is_profile_complete(request, *args, **kwargs):
        if request.user.role == 'Candidate':
            try:
                CandidateProfile.objects.get(user=request.user.id)
                return func(request, *args, **kwargs)
            except ObjectDoesNotExist:
                message = "Please complete your profile"
                return JsonResponse({"message": message}, status=403)
        elif request.user.role == 'Interviewer':
            try:
                InterviewerProfile.objects.get(user=request.user.id)
                return func(request, *args, **kwargs)
            except ObjectDoesNotExist:
                message = "Please complete your profile"
                return JsonResponse({"message": message}, status=403)
        else:
            raise ValidationError("Invalid role/Anonymous user")
    return is_profile_complete
