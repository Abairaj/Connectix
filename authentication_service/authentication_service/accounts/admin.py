from django.contrib import admin

from .models import JoinRequest, Organization, User

admin.site.register(Organization)
admin.site.register(JoinRequest)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "phone_number",
        "is_active",
        "is_staff",
    )
    search_fields = ("email", "username")
    list_filter = ("is_active", "is_staff")
