# Writing your first Django app part 1 - 2


`django-admin startproject mysite` untuk buat Project baru dengan nama mysite. `python manage.py startapp polls` untuk buat app dengan nama pool
## Menampilkan Halo
edit `polls/views.py`
```python
from django.http import HttpResponse

def index(request)
	return HttpResponse("Halo bro")
```

Selanjutnya untuk mengarahkan ke app polls kita perlu buat route di ```polls/urls.py```

from django.urls import path
from . import views
```python
urlpatterns = [
	path('',views.index, name='index'),
]
```

tapi untuk mengarahkan ke pattern di atas kita juga perlu buat ```mystite/urls.py``` di root project kita.

```python
from django.contrib import admin
from djangi.urls import include, path

urlpatterns = [
	path('polls/',include('polls.urls')),
	path('admin/',admin.site.urls),
]
```

fungsi path() melewatkan 4 argumen, argumen yang wajib adalah route dan view, yang boleh ngga ada adalah kwargs dan name. url pattern tidak mengenal adanya GET POST sehingga https://127.0.0.1/polls/?page=3 akan sama aja dengan https://127.0.0.1/polls

```
$python manage.py runserver
```

coba akses http://127.0.0.1/polls

## Models
`INSTALLED_APPS` setting memuat app app yang ada di django, ada beberapa app default disana. Mereka perlu database table sehingga kita perlu buatkan database supaya app tersebut bisa digunakan. Gunakan
```
python manage.py migrate
```
untuk membuat database. command migrate akan melihat value setting `INSTALLED_APPS` dan membuatkan table dari app app tersebut. Dalam beberapa kasus ngga semua app dibutuhkan, kita bisa bisa mengcomment app app yang ngga dibutuhkan di `INSTALLED_APPS`.Model akan mewakili table di database. edit `polls/models.py`
```python
from django.db import models

class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DataTimeField('date published')

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
```
variabel2 di dalam model class mewakili field database. Di dalam variabel kita memanggil fungsi yang juga menandakan setiap tipe data field field yang ada di dalam table. Nama variable mewakili nama pada coloumn table, tapi kita bisa juga menggunakan nama lain untuk kolom dengan melewatkan argument paling depan di fungsi field.(seperti pada date published). Beberapa argument pada field sifatnya wajib, contohnya max_length pada CharField. atau argument opsional seperti pada IntegerField untuk mendefinisikan default value.

Dengan mengaktifkan model, django akan buat schema database dan juga buat database access API untuk mengakses model model yang sudah dibuat. Jangan lupa menginclude kan app kita di setting `INSTALLED_APPS`.Tambahkan nama app kita, dalam hal ini app kita diwakili dengan nama `PollsConfig` di dalam `polls/apps.py` sehingga kita bisa include kan app kita dengan :

```python
	INSTALLED_APPS = [
	    'polls.apps.PollsConfig',
	    ...
	]
```
selanjutanya jalankan
```
$python manage.py makemigrations Polls
```
command di atas ngasih tau django kalau kita baru saja melakukan perubahan di models kita, dan command tersebut akan menggenerate fungsi untuk buat schema di database kita. fungsi tersebut akan terbentuk di dalam 'polls/migrations/0001_initial.py', setelah itu kita akan mengapply file hasil migrations tadi dan buat kan schemanya. kalau mau ngecek bentuk SQL nya seperti apa bisa dengan command
```
$python manage.py sqlmigrate polls 0001
```
kalau mau ngecek aja ada error apa ngga gunakan
```
$python manage.py check
```
okee.. apply menggunakan python manage.py migrate

## Access API Database

mari kita coba access api nya pake python shell dulu
```
$python manage.py shell
```
```python
>>>from polls.models import Choice, Question
<QuerySet []>

>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
>>> q.save()
```


```python
>>> q.id #check object q akan memiliki values
1
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2019, 12, 29, 2, 29, 44, 166640, tzinfo=<UTC>)
>>>
>>> q.question_text="what's up dude ?" #merubah value
>>> Question.objects.all() #menampilkan semua question di databases
<QuerySet [<Question: Question object (1)>]>
```

biar output nya mengeluarkan value tambahin __str__()method ke class Question dan Choice

```python
from django.db import models

class Question(models.Model):
		...
		def __str__(self):
	return self.question_text

class Choice(models.Mode):
		def __str__(self):
	return self.choice_text
```
tambahkan method was published recently di
```python
class Question
	import datetime
	...
	import django.utils import timezone
	...
	def was_published_recently(self):
	    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
```
check lagi di shell, python manage.py shell

```python
>>>Question.objects.all()
<QuerySet [<Question: What's up dude?>]>

>>>question.object.filter(id=1)
<QuerySet [<Question: What's up dude?>]>

>>>Question.objects.filter(question_text__startswith='What')
<QuerySet [<Question: What's up dude?>]>

>>>q=Question.objects.get(pk=1)
>>>q.choice_set.create(choice_text='The sky',votes=0)
>>>q.choice_set.create(choice_text='Not much',votes=0)
>>>c = q.choice_set.create(choice_text='Just hacking again',votes=0)
>>>c.question
>>><Question: What's up dude?>
```

buat admin mysite, ```python manage.py createsuperuser```. admin site punya editable content group dan user. they are provided by django.contrib.auth. terus dimana polls nya ? kita harus meregister nya dulu. kita harus memberi tahu admin bahwa Question objects memiliki admin interface. to do this buka ```polls/admin.py``` file. dan edit

```python
	from django.contrib import admin
	from .models import Question

	admin.site.register(Question)
```

###### lanjut ke part 3...
