from django.contrib import admin
from .models import User, OTP,UserLockout


admin.site.register(User)
admin.site.register(OTP)
admin.site.register(UserLockout)
