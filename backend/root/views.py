from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        interview_dict = request.data.dict()
        interview_dict['booked_by'] = request.user.id
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
