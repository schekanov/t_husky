from django.contrib import admin

from register.models import Master, CarModel, CarBrand, Schedule, RegisterRecord


class RegisterRecordInline(admin.TabularInline):
    model = RegisterRecord


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [RegisterRecordInline]


class CarModelInline(admin.TabularInline):
    model = CarModel


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = []


admin.site.register(CarModel)
admin.site.register(Schedule)
admin.site.register(RegisterRecord)

