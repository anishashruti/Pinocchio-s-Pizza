from django.contrib import admin
from .models import (Pasta,Sicilian_pizza,Regular_pizza,Salad,Sub,Topping,Dinnerplatter,
                        Order2,Transaction)

# Register your models here.
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Topping)
admin.site.register(Regular_pizza)
admin.site.register(Sicilian_pizza)
admin.site.register(Dinnerplatter)
admin.site.register(Sub)
admin.site.register(Order2)
admin.site.register(Transaction)


