import os
import django

# Django-ს კონფიგურაცია
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logiclink_project.settings')
django.setup()

from riddles.models import Riddle

# თავსატეხების სია
riddles_data = [
    # მარტივი (10 კოინი)
    {
        'question': 'თუ ყველა კატა ცხოველია და ზოგი ცხოველი ძაღლია, არის თუ არა ზოგი კატა ძაღლი?',
        'answer': 'არა',
        'difficulty': 'easy',
        'coins': 10
    },
    {
        'question': 'ოთახში სამი ნათურაა და მეორე ოთახში სამი ჩამრთველი. მხოლოდ ერთხელ შეგიძლია შეხვიდე ნათურების ოთახში. როგორ გაიგებ რომელი ჩამრთველი რომელ ნათურას აკონტროლებს?',
        'answer': 'სითბოთი',
        'difficulty': 'easy',
        'coins': 10
    },
    {
        'question': 'რომელი რიცხვი იზრდება, როცა მას 180 გრადუსით ატრიალებ?',
        'answer': '6',
        'difficulty': 'easy',
        'coins': 10
    },
    {
        'question': 'რამდენჯერ შეიძლება ათიდან ერთის გამოკლება?',
        'answer': 'ერთხელ',
        'difficulty': 'easy',
        'coins': 10
    },
    {
        'question': 'რა მოდის ერთხელ წუთში, ორჯერ წამში და არასდროს საათში?',
        'answer': 'წ',
        'difficulty': 'easy',
        'coins': 10
    },
    {
        'question': 'თუ გუშინწინ იყო ხვალ, დღეს რა დღე იქნებოდა?',
        'answer': 'პარასკევი',
        'difficulty': 'easy',
        'coins': 10
    },
    {
        'question': 'რამდენ თვეს აქვს 28 დღე?',
        'answer': 'ყველას',
        'difficulty': 'easy',
        'coins': 10
    },
    {
        'question': 'რა იშლება, როდესაც მას დაასახელებ?',
        'answer': 'სიჩუმე',
        'difficulty': 'easy',
        'coins': 10
    },
    {
        'question': 'რა ეკუთვნის შენ, მაგრამ სხვები უფრო ხშირად იყენებენ?',
        'answer': 'სახელი',
        'difficulty': 'easy',
        'coins': 10
    },
    {
        'question': 'რა მოძრაობს მხოლოდ წინ და არასდროს უკან?',
        'answer': 'დრო',
        'difficulty': 'easy',
        'coins': 10
    },
    
    # საშუალო (20 კოინი)
    {
        'question': 'რა იზრდება, როდესაც მას ხარჯავ?',
        'answer': 'გამოცდილება',
        'difficulty': 'medium',
        'coins': 20
    },
    {
        'question': 'თუ ხუთი ადამიანი დგას რიგში, რამდენი ადამიანი დგას მეოთხის წინ?',
        'answer': 'სამი',
        'difficulty': 'medium',
        'coins': 20
    },
    {
        'question': 'რა არის უფრო მძიმე - ერთი კილოგრამი რკინა თუ ერთი კილოგრამი ბამბა?',
        'answer': 'ერთნაირი',
        'difficulty': 'medium',
        'coins': 20
    },
    {
        'question': 'რას აქვს გასაღებები, მაგრამ კარს ვერ აღებს?',
        'answer': 'კლავიატურა',
        'difficulty': 'medium',
        'coins': 20
    },
    {
        'question': 'რამდენი კუთხე აქვს წრეს?',
        'answer': 'არცერთი',
        'difficulty': 'medium',
        'coins': 20
    },
    {
        'question': 'რა შეიძლება გქონდეს, მაგრამ ვერ ნახავ?',
        'answer': 'მომავალი',
        'difficulty': 'medium',
        'coins': 20
    },
    {
        'question': 'რა ივსება, როდესაც მას ამცირებ?',
        'answer': 'ნაგვის ურნა',
        'difficulty': 'medium',
        'coins': 20
    },
    {
        'question': 'რა ეცემა ყოველ საღამოს, მაგრამ არასდროს იმტვრევა?',
        'answer': 'ღამე',
        'difficulty': 'medium',
        'coins': 20
    },
    {
        'question': 'რა ჩნდება კითხვის დროს და ქრება პასუხის შემდეგ?',
        'answer': 'ეჭვი',
        'difficulty': 'medium',
        'coins': 20
    },
    {
        'question': 'რა იზრდება, რაც უფრო მეტს ჭრი?',
        'answer': 'თმა',
        'difficulty': 'medium',
        'coins': 20
    },
    
    # რთული (50 კოინი)
    {
        'question': 'რა შეგიძლია აჩუქო სხვას და თავადაც შეინარჩუნო?',
        'answer': 'ცოდნა',
        'difficulty': 'hard',
        'coins': 50
    },
    {
        'question': 'რა ხედავს ყველაფერს, მაგრამ არაფერი ახსოვს?',
        'answer': 'კამერა',
        'difficulty': 'hard',
        'coins': 50
    },
    {
        'question': 'რას აქვს დასაწყისი, მაგრამ არ აქვს დასასრული?',
        'answer': 'წრე',
        'difficulty': 'hard',
        'coins': 50
    },
    {
        'question': 'რა გჭირდება რომ რამე გააკეთო, სანამ დაიწყებ?',
        'answer': 'გადაწყვეტილება',
        'difficulty': 'hard',
        'coins': 50
    },
    {
        'question': 'რა არსებობს მხოლოდ მაშინ, როდესაც მას ყურადღებას აქცევ?',
        'answer': 'პრობლემა',
        'difficulty': 'hard',
        'coins': 50
    },
    {
        'question': 'რა არის ყველაზე მოკლე გზა შეცდომამდე?',
        'answer': 'აჩქარება',
        'difficulty': 'hard',
        'coins': 50
    },
    {
        'question': 'რა მუშაობს მხოლოდ მაშინ, როდესაც წესებს აკისრებს?',
        'answer': 'სისტემა',
        'difficulty': 'hard',
        'coins': 50
    },
    {
        'question': 'რა არის ლოგიკის მთავარი მტერი?',
        'answer': 'ემოცია',
        'difficulty': 'hard',
        'coins': 50
    },
    {
        'question': 'ორი დედა და ორი ქალიშვილი გავიდნენ სადილზე და სამი ბურგერი შეუკვეთეს. თითოეულმა სრული ბურგერი შეჭამა. როგორ არის ეს შესაძლებელი?',
        'answer': 'ბებია დედა შვილი',
        'difficulty': 'hard',
        'coins': 50
    },
    {
        'question': 'თუ ხუთმა პროგრამისტმა ხუთი კოდი დაწერა ხუთ დღეში, რამდენ დღეში დაწერს ათმა პროგრამისტმა ათი კოდი?',
        'answer': '5',
        'difficulty': 'hard',
        'coins': 50
    },
]

# თავსატეხების დამატება
print("🚀 თავსატეხების დამატება იწყება...")
added = 0

for riddle_data in riddles_data:
    # შევამოწმოთ არსებობს თუ არა უკვე
    exists = Riddle.objects.filter(question=riddle_data['question']).exists()
    
    if not exists:
        Riddle.objects.create(**riddle_data)
        added += 1
        print(f"✅ დამატებულია: {riddle_data['question'][:50]}...")
    else:
        print(f"⏭️  უკვე არსებობს: {riddle_data['question'][:50]}...")

print(f"\n🎉 დასრულდა! დამატებულია {added} ახალი თავსატეხი!")