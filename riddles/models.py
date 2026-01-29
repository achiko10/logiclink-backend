from django.db import models
from django.contrib.auth.models import User


class Riddle(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'მარტივი'),
        ('medium', 'საშუალო'),
        ('hard', 'რთული'),
    ]
    
    question = models.TextField(verbose_name="თავსატეხი")
    answer = models.CharField(max_length=200, verbose_name="მთავარი პასუხი")
    alternative_answers = models.TextField(blank=True, null=True, verbose_name="ალტერნატიული პასუხები (მძიმით გამოყავით)")
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy',
        verbose_name="სირთულე"
    )
    coins = models.IntegerField(default=10, verbose_name="კოინები")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.question[:50]}..."
    
    class Meta:
        verbose_name = "თავსატეხი"
        verbose_name_plural = "თავსატეხები"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    coins = models.IntegerField(default=0, verbose_name="კოინები")
    level = models.IntegerField(default=1, verbose_name="დონე")
    is_pro = models.BooleanField(default=False, verbose_name="Pro სტატუსი")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.coins} კოინი"
    
    class Meta:
        verbose_name = "მომხმარებლის პროფილი"
        verbose_name_plural = "მომხმარებლების პროფილები"


class SolvedRiddle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solved_riddles')
    riddle = models.ForeignKey(Riddle, on_delete=models.CASCADE)
    solved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "ამოხსნილი თავსატეხი"
        verbose_name_plural = "ამოხსნილი თავსატეხები"
        unique_together = ['user', 'riddle']
    
    def __str__(self):
        return f"{self.user.username} - {self.riddle.question[:30]}"