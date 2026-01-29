from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Riddle, UserProfile, SolvedRiddle
import random
from difflib import SequenceMatcher


def riddle_game(request):
    riddles = Riddle.objects.all()
    
    if not riddles.exists():
        return render(request, 'riddles/game.html', {'riddle': None, 'total_coins': 0})
    
    # თუ მომხმარებელი შესულია - მხოლოდ ამოუხსნელი თავსატეხები
    if request.user.is_authenticated:
        solved_ids = SolvedRiddle.objects.filter(user=request.user).values_list('riddle_id', flat=True)
        unsolved_riddles = riddles.exclude(id__in=solved_ids)
        
        if not unsolved_riddles.exists():
            # ყველა ამოხსნილია
            total_coins = request.user.profile.coins
            return render(request, 'riddles/game.html', {
                'riddle': None, 
                'total_coins': total_coins,
                'all_solved': True
            })
        
        available_riddles = unsolved_riddles
    else:
        # სტუმრებისთვის - ყველა თავსატეხი
        available_riddles = riddles
    
    riddle_id = request.session.get('current_riddle_id')
    
    if riddle_id:
        try:
            riddle = Riddle.objects.get(id=riddle_id)
            # შევამოწმოთ რომ ეს თავსატეხი ჯერ არ არის ამოხსნილი
            if request.user.is_authenticated and riddle not in available_riddles:
                riddle = random.choice(available_riddles)
                request.session['current_riddle_id'] = riddle.id
        except Riddle.DoesNotExist:
            riddle = random.choice(available_riddles)
            request.session['current_riddle_id'] = riddle.id
    else:
        riddle = random.choice(available_riddles)
        request.session['current_riddle_id'] = riddle.id
    
    if request.method == 'POST' and riddle:
        # გამოტოვების ღილაკი
        if 'skip' in request.POST:
            del request.session['current_riddle_id']
            messages.info(request, '⏭️ თავსატეხი გამოტოვებულია')
            return redirect('riddle_game')
        
        user_answer = request.POST.get('answer', '')
        
        if check_answer_smart(user_answer, riddle):
            # თუ მომხმარებელი შესულია
            if request.user.is_authenticated:
                profile = request.user.profile
                profile.coins += riddle.coins
                profile.save()
                
                # SolvedRiddle-ში შენახვა
                SolvedRiddle.objects.get_or_create(user=request.user, riddle=riddle)
                
                messages.success(request, f'🎉 სწორია! მიიღე {riddle.coins} კოინი!')
            else:
                # სტუმრებს - სესიაში
                coins = request.session.get('guest_coins', 0)
                request.session['guest_coins'] = coins + riddle.coins
                messages.success(request, f'🎉 სწორია! მიიღე {riddle.coins} კოინი!')
            
            del request.session['current_riddle_id']
            return redirect('riddle_game')
        else:
            messages.error(request, f'❌ არასწორია! სცადე კიდევ.')
    
    # კოინების ჩვენება
    if request.user.is_authenticated:
        total_coins = request.user.profile.coins
    else:
        total_coins = request.session.get('guest_coins', 0)
    
    context = {
        'riddle': riddle,
        'total_coins': total_coins
    }
    
    return render(request, 'riddles/game.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, '❌ პაროლები არ ემთხვევა!')
            return render(request, 'riddles/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, '❌ ეს სახელი უკვე დაკავებულია!')
            return render(request, 'riddles/register.html')
        
        user = User.objects.create_user(username=username, password=password)
        
        guest_coins = request.session.get('guest_coins', 0)
        
        profile = UserProfile.objects.create(
            user=user,
            coins=guest_coins,
            is_pro=True if guest_coins >= 500 else False
        )
        
        request.session['guest_coins'] = 0
        
        messages.success(request, f'🎉 გილოცავ! Pro სტატუსი მიღებულია! {guest_coins} კოინი გადაიტანა.')
        return redirect('riddle_game')
    
    total_coins = request.session.get('guest_coins', 0)
    return render(request, 'riddles/register.html', {'total_coins': total_coins})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'👋 მოგესალმები, {username}!')
            return redirect('riddle_game')
        else:
            messages.error(request, '❌ არასწორი სახელი ან პაროლი!')
    
    return render(request, 'riddles/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, '👋 ნახვამდის!')
    return redirect('riddle_game')


def check_answer_smart(user_answer, riddle):
    """
    ინტელექტუალური პასუხის შემოწმება:
    1. ნაწილობრივი დამთხვევა
    2. ნებისმიერი რიგით (სიტყვები)
    3. სინონიმები/ალტერნატიული პასუხები
    4. ორთოგრაფიული შეცდომების პატიება (80%+ მსგავსება)
    """
    user_answer = user_answer.strip().lower()
    correct_answer = riddle.answer.strip().lower()
    
    # ყველა შესაძლო პასუხის სია
    all_answers = [correct_answer]
    if riddle.alternative_answers:
        alternatives = [a.strip().lower() for a in riddle.alternative_answers.split(',') if a.strip()]
        all_answers.extend(alternatives)
    
    for correct in all_answers:
        # 1. ზუსტი დამთხვევა
        if user_answer == correct:
            return True
        
        # 2. ნაწილობრივი დამთხვევა - პასუხი შეიცავს სწორ სიტყვას
        if correct in user_answer or user_answer in correct:
            # თუ სწორი პასუხი მინიმუმ 3 სიმბოლოა და მომხმარებლის პასუხშია
            if len(correct) >= 3:
                return True
        
        # 3. ნებისმიერი რიგით - სიტყვების შედარება
        user_words = set(user_answer.split())
        correct_words = set(correct.split())
        if len(user_words) > 1 and len(correct_words) > 1:
            # თუ ყველა სიტყვა ემთხვევა (რიგის მიუხედავად)
            if user_words == correct_words:
                return True
        
        # 4. ორთოგრაფიული შეცდომების პატიება - 80%+ მსგავსება
        similarity = SequenceMatcher(None, user_answer, correct).ratio()
        if similarity >= 0.8:  # 80% მსგავსება
            return True
    
    return False


def landing(request):
    """Landing Page"""
    return render(request, 'riddles/landing.html')