from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('nombre','email', 'foto_perfil', 'user_type', 'is_active', 'is_staff', 'create_date', 'update_date')
    list_filter = ('is_active', 'is_staff', 'user_type')  # Filtros rápidos en la interfaz de admin
    search_fields = ('email',) 
    ordering = ('email',)  
    filter_horizontal = ('groups', 'user_permissions') 
    
    fieldsets = (
        ('Información de cuenta', {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('nombre','user_type', 'foto_perfil')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('create_date', 'update_date')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type', 'is_active', 'is_staff'),
        }),
    )

    readonly_fields = ('create_date', 'update_date')

    def get_user_type(self, obj):
        return obj.user_type
    get_user_type.short_description = 'Tipo de usuario'

admin.site.register(MyUser, MyUserAdmin)
