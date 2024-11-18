from typing import Optional
from random import choice, randint
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike, QuestionTag

fake = Faker()


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными"

    def add_arguments(self, parser):
        parser.add_argument(
            '--ratio',
            type=int,
            required=True,
            help="Коэффициент для генерации данных",
        )

    def handle(self, *args, **options):
        ratio: Optional[int] = options.get('ratio')
        if not ratio:
            raise ValueError("Не указан параметр --ratio")

        # Генерация пользователей
        num_users = ratio
        users = [User(username=fake.user_name(), email=fake.email()) for _ in range(num_users)]
        User.objects.bulk_create(users, ignore_conflicts=True)
        self.stdout.write(f"Создано {num_users} пользователей.")

        # Создаем профили
        user_Profile = [
            Profile(user=user, description=fake.text(max_nb_chars=50))
            for user in User.objects.filter(profile__isnull=True)  # отфильтровываем пользователей без профиля
        ]
        Profile.objects.bulk_create(user_Profile)
        self.stdout.write(f"Создано {len(user_Profile)} профилей пользователей.")

        # Генерация тегов
        num_Tag = ratio
        tag = [Tag(name=fake.word(), views=randint(0, 1000)) for _ in range(num_Tag)]
        Tag.objects.bulk_create(tag)
        self.stdout.write(f"Создано {num_Tag} тегов.")

        # Генерация вопросов
        num_Question = ratio * 10
        Questions = [
            Question(
                author=choice(User.objects.all()),
                title=fake.sentence(),
                text=fake.paragraph(nb_sentences=5),
                views=randint(0, 1000),
            ) for _ in range(num_Question)
        ]
        Question.objects.bulk_create(Questions)
        self.stdout.write(f"Создано {num_Question} вопросов.")

        # Генерация связи многих ко многим QuestionTag
        QuestionTags = [
            QuestionTag(
                question=choice(Question.objects.all()),
                tag=choice(Tag.objects.all())
            ) for _ in range(num_Question * 10)
        ]
        QuestionTag.objects.bulk_create(QuestionTags)

        # Генерация ответов
        num_Answer = ratio * 100
        Answers = [
            Answer(
                question=choice(Question.objects.all()),
                author=choice(User.objects.all()),
                text=fake.paragraph(nb_sentences=3)
            ) for _ in range(num_Answer)
        ]
        Answer.objects.bulk_create(Answers)
        self.stdout.write(f"Создано {num_Answer} ответов.")

        # Генерация оценок для вопросов и ответов
        num_question_likes = ratio * 200
        question_likes = [
            QuestionLike(
                user=choice(User.objects.all()),
                question=choice(Question.objects.all())
            ) for _ in range(num_question_likes)
        ]
        QuestionLike.objects.bulk_create(question_likes, ignore_conflicts=True)

        num_answer_likes = ratio * 200
        answer_likes = [
            AnswerLike(
                user=choice(User.objects.all()),
                answer=choice(Answer.objects.all())
            ) for _ in range(num_answer_likes)
        ]
        AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True)

        self.stdout.write(f"Создано {num_question_likes} оценок для вопросов и {num_answer_likes} оценок для ответов.")
