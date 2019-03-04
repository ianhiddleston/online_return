from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User
from character.models import Branch, Player, Race, Nationality, Language, Guild, GuildRank, Character, Brand, SocialPosition, Adventure, Transaction

# Register your models here.
admin.site.register(Branch)
admin.site.register(Player)
admin.site.register(Race)
admin.site.register(Nationality)
admin.site.register(Language)
admin.site.register(Guild)
admin.site.register(GuildRank)
admin.site.register(Character)
admin.site.register(Brand)
admin.site.register(SocialPosition)
admin.site.register(Adventure)
admin.site.register(Transaction)


class UserProfileInline(admin.StackedInline):
    model = Player
    max_num = 1
    can_delete = False
    verbose_name_plural = 'Player Profile'
    fk_name = 'user'

class UserAdmin(AuthUserAdmin):
   def add_view(self, *args, **kwargs):
      self.inlines = []
      return super(UserAdmin, self).add_view(*args, **kwargs)

   def change_view(self, *args, **kwargs):
      self.inlines = [UserProfileInline]
      return super(UserAdmin, self).change_view(*args, **kwargs)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
