from django.contrib import admin
from .models import Riddle, UserProfile, SolvedRiddle

@admin.register(Riddle)
class RiddleAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'difficulty', 'coins', 'created_at']
    list_filter = ['difficulty']
    search_fields = ['question', 'answer']
    fields = ['question', 'answer', 'alternative_answers', 'difficulty', 'coins']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'coins', 'level', 'is_pro', 'created_at']
    list_filter = ['is_pro', 'level']
    search_fields = ['user__username']

@admin.register(SolvedRiddle)
class SolvedRiddleAdmin(admin.ModelAdmin):
    list_display = ['user', 'riddle', 'solved_at']
    list_filter = ['solved_at']
    search_fields = ['user__username', 'riddle__question']