import re
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from app.models import CustomUser, Question, Tag, QuestionTag, Answer

User = get_user_model()

class LoginForm(forms.Form):
    login = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_login(self):
        login = self.cleaned_data.get('login')
        # Проверяем наличие пользователя с таким login или email
        user = User.objects.filter(login=login).first() or User.objects.filter(email=login).first()
        if not user:
            raise ValidationError("No account found with this login or email.")

        return login

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        password = cleaned_data.get('password')

        if login and password:
            # Пытаемся найти пользователя по login или email
            user = User.objects.filter(login=login).first() or User.objects.filter(email=login).first()

            if user:
                # Проверяем пароль
                if not user.check_password(password):
                    self.add_error('password', 'Incorrect password.')
            else:
                # Если пользователь не найден, ошибка уже добавлена в clean_login
                pass

        return cleaned_data
class RegisterForm(forms.ModelForm):
    login = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['login', 'email', 'username', 'password']

    def clean_login(self):
        login = self.cleaned_data.get('login')
        user = User.objects.filter(username=login).first()
        if user:
            raise ValidationError("This login is already registered.")

        return login

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            raise ValidationError("This email is already registered.")

        return email

    def clean_nickname(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(nickname=username).first()
        if user:
            raise ValidationError("This nickname is already registered.")

        return username

    def clean_repeat_password(self):
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')

        if repeat_password != password:
            self.add_error('password', 'Passwords do not match.')
            self.add_error('repeat_password', 'Passwords do not match.')

        else:
            return repeat_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class AddQuestionForm(forms.ModelForm):
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a question title',
            'maxlength': 100,
        })
    )
    text = forms.CharField(
        label="Some text",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe your question',
            'rows': 5,
        })
    )
    tags = forms.CharField(
        label="Tags",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (for example: Apple, Tree)',
        }),
        required=False
    )

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            self.add_error('title', 'Title cannot be empty.')

        question = Question.objects.filter(title=title).first()
        if question:
            self.add_error('title', 'This title is already exists.')
        else:
            return title

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            self.add_error('text', 'This text is required.')
        else:
            return text

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        return tags

    def save(self, commit=True, author=None):
        question = super().save(commit=False)
        if author:
            question.author = author
        if commit:
            question.save()

        tags = self.cleaned_data.get('tags', '')
        if tags:
            tag_names = [tag.strip() for tag in tags.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                QuestionTag.objects.get_or_create(question=question, tag=tag)

        return question

class AddAnswerForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your answer here..',
            'rows': 2,
        }),
        required=False
    )

    class Meta:
        model = Answer
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            self.add_error('text', 'Answer cannot be empty.')
        return text

    def save(self, commit=True, author=None, question=None):
        answer = super().save(commit=False)
        if author:
            answer.author = author
        if question:
            answer.question = question
        if commit:
            answer.save()
        return answer