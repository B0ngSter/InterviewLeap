from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
import pytz
from root.serializers import BookInterviewCreateSerializer


class BookInterviewView(CreateAPIView):
    """
        Book Interview   -- Authenticated Candidate can create/book interview  they are willing to interviewed!
        actions -- Post -- Book Interview
        Request params -- {
                    "company_type": "product","service","captive" (string)
                    "professional_status": (string)
                    "applied_designation" : "python developer" (string)
                    "date": "2020-06-21", (string)
                    "time_slots": [
                            "9am - 10am",
                            "2pm - 3pm"
                            "6pm - 7pm",
                    ] (array field)
                }
        Response Status -- 200 Ok along with booking interview details
        Error Code -- 400 Bad Request
        Error message -- Raise proper error messages
    """

    serializer_class = BookInterviewCreateSerializer

    def get(self, request, *args, **kwargs):
        response = {"timezone_list": pytz.all_timezones}
        return Response(response, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        interview_dict = request.data.dict()
        interview_dict['booked_by'] = request.user.id
        if 'skills' in interview_dict:
            interview_dict['skills'] = [{'title': skill} for skill in interview_dict['skills'].split(",")]
        interview_dict['time_slots'] = interview_dict['time_slots'].split(',')
        serializer = self.get_serializer(data=interview_dict)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            if serializer.errors.get('message'):
                error_message = serializer.errors.get('message')[0]
            else:
                error_message = ", ".join([error for error in serializer.errors.keys()])
                error_message = "Invalid value for {}".format(error_message)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)


class TimeSlotListView(APIView):
    """
       Retrieve -- Retrieve list of time slots.
       Actions -- GET method
       Response Status -- 200 Ok
    """

    def get(self, request, *args, **kwargs):
        time_slots = settings.CANDIDATE_TIME_SLOTS
        slots = [slot[0] for slot in time_slots]
        return Response({"time_slot": slots}, status=status.HTTP_200_OK)