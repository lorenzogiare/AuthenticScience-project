from django.contrib import admin
from .models import Article, IpAddress, ArticleDetailsRequest, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from django.contrib.auth.models import User


#-----ACTIONS-IN-THE-ADMIN-PANEL----------------------------------------

# defines the publish action in the admin panel
def make_published(modeladmin, request, queryset,):
    queryset.update(status='P')
    queryset.update(published_date=timezone.now())
make_published.short_description = 'Publish selected articles'

# defines the author verification action in the admin panel 
def verify_authors(modeladmin, request, queryset,):
    for obj in queryset:
        obj.profile.verified_author = True
        obj.save()
verify_authors.short_description = 'Verify selected users as authors'


#------MODELS-IN-THE-ADMIN-PANEL----------------------------------------

# defines the Article model's appearence in the admin panel
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','author','status']
    ordering = ['title']
    actions = [make_published]

# defines the IpAddress model's appearence in the admin panel
class IpAddressAdmin(admin.ModelAdmin):
    list_display = ['ip_address','city', 'country', 'user_logged', 'login_date']
    ordering = ['login_date']

# defines the ArticleDetailsRequest model's appearance in the admin panel
class ArticleDetailsRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'title_requested', 'id_string','pk_requested']
    ordering = ['title_requested']


# registers the models in the admin section
admin.site.register(Article, ArticleAdmin)
admin.site.register(IpAddress, IpAddressAdmin)
admin.site.register(ArticleDetailsRequest,ArticleDetailsRequestAdmin)


#------EXSTENSION-OF-THE-USER-MODEL-------------------------------------

# connects the Profile Model to the admin panel
class InlineProfile(admin.StackedInline):
    model = Profile

# re-defines the User model appearance in the admin panel (adds verified_author field)
class UserAdmin(admin.ModelAdmin):

    def verified_author(obj, user):
        return user.profile.verified_author

    verified_author.boolean = True

    actions=[verify_authors]
    inlines=[InlineProfile]
    list_display=['username', 'first_name', 'last_name', 'is_staff', 'verified_author',]

# updates the registration of User and UserAdmin models
admin.site.unregister(User)
admin.site.register(User,UserAdmin)

