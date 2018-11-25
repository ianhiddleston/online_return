from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Branch, Player, Race, Nationality, Language, Guild, GuildRank, Character

# Register your models here.
admin.site.register(Branch)
admin.site.register(Player)
admin.site.register(Race)
admin.site.register(Nationality)
admin.site.register(Language)
admin.site.register(Guild)
admin.site.register(GuildRank)
admin.site.register(Character)


class ProfileInline(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'Player Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
