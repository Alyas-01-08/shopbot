from django.contrib import admin

from users.models import UserBot, Address


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0


@admin.register(UserBot)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name',
                    'created_at', 'updated_at', 'phone')
    list_display_links = ('id',)
    inlines = [AddressInline]
    ordering = ('-created_at',)


admin.site.register(Address)


#     fieldsets = (
#         # (None, {'fields': ('username', 'password')}),
#         (_('Personal info'), {'fields': ('tg_user_id', 'first_name', 'last_name', 'profession', 'bio', 'avatar')}),
#         (_('Permissions'), {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')})
#     )


# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ('id', 'created_at', 'updated_at')
#     list_display_links = ('id',)
#     ordering = ('-created_at',)


# admin.site.register(Strengths)
# admin.site.register(UserBotAction)
