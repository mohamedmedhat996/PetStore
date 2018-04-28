from django.contrib import admin
from Home.models import Pet, PaymentMethod, PetCategory, PetCategoryKind, HistoryRecord

admin.site.register(Pet)
admin.site.register(PaymentMethod)
admin.site.register(PetCategory)
admin.site.register(PetCategoryKind)
admin.site.register(HistoryRecord)
