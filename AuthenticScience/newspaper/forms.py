import profile
from django import forms
from django.contrib.auth.models import User
from .models import Article, ArticleDetailsRequest

# article order options
DATE_ORDER = [
    ('MOST RECENT','most recent'),
    ('LEAST RECENT','least recent'),
]

# creates a list of all authors and adds the "any" option
AUTHORS = [(author.id, author) for author in list(User.objects.all()) if author.profile.verified_author ]
AUTHORS.append(['any', 'any'])

# Search bar
class SearchBarForm(forms.Form):
    search_filter = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class':'form-control text-center',
            'placeholder':'Search an article'
            }
    ))
    
    articles_order = forms.ChoiceField(
        choices=DATE_ORDER,
        required=False,
        initial='MOST RECENT',
        widget=forms.Select(attrs={
            'class':'form-select',
            'placeholder':'',
            }
    ))
    author_filter = forms.ChoiceField(choices=AUTHORS,
        required=False,
        initial='any',
        widget=forms.Select(attrs={
            'class':'form-select',
            'placeholder':''
            }
    ) )

# login form
class AuthorLoginForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=18,widget=forms.TextInput(attrs={'class':'form-select','placeholder':'username'} ))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'class':'form-select','placeholder':'password'} ))

    def __init__(self, *args, **kwargs):
        super(AuthorLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

# registration form
class AuthorRegistrationForm(forms.Form):
    username = forms.CharField(label='Username:', max_length=18, widget=forms.TextInput(attrs={'placeholder':'name on this platform'}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder':'your password'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder':'first name'}))
    last_name = forms.CharField(max_length=20,  widget=forms.TextInput(attrs={'placeholder':'last name'}))
    email = forms.EmailField( widget=forms.EmailInput(attrs={'placeholder':'name@example.com'}))

    def __init__(self, *args, **kwargs):
        super(AuthorRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

# new article form
class NewArticleForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ('title', 'description', 'content')

    def __init__(self, *args, **kwargs):
        super(NewArticleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

# user id form, to get articles' data
class ArticleDetailsRequestForm(forms.ModelForm):

    class Meta:
        model = ArticleDetailsRequest
        fields = ('id_string',)

    def __init__(self, *args, **kwargs):
        super(ArticleDetailsRequestForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'identification string'
            