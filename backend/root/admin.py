from django.contrib import admin
from .models import BookInterview, PaymentDetails, PaymentStatusLog

admin.site.register(BookInterview)
admin.site.register(PaymentDetails)
admin.site.register(PaymentStatusLog)
