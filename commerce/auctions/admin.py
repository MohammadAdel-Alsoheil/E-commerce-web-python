from django.contrib import admin

from .models import *

# Register your models here.


admin.site.register(User)
admin.site.register(Category)
admin.site.register(listing)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Bids)
