################ Writing your first Django app part 1 -2 ######################


# 'django-admin startproject mysite' untuk Membuat Project
# 'python manage.py startapp polls' untuk membuat app namanya pool
# masuk 'polls/views.py' kemudian edit :

	from django.http import HttpResponse

	def index(request)
	    return HttpResponse("Halo bro")

# Selanjutnya untuk melakukan route kita perlu menambahkan pada file 'polls/urls.py'

	from django.urls import path
	from . import views

	urlpatterns = [
	    path('',views.index, name='index'),
	]

# bikin juga urls.py di root project kita di 'mysite/urls.py' dan diarahkan ke urls milik polls

	from django.contrib import admin
	from djangi.urls import include, path

	urlpatterns = [
	    path('polls/',include('polls.urls')),
	    path('admin/',admin.site.urls),
	]

# fungsi path() melewatkan 4 argumen, yang wajib adalah route dan view, yang boleh ngga ada adalah kwargs dan name. url pattern tidak mengenal adanya GET POST https://www.example.com/myapp/?page=3 akan sama aja dengan https://www.example.com/myapp
# INSTALLED_APPS setting memuat app app yang ada di django, ada beberapa app default. mereka memerlukan database table sehingga kita perlu membuatkan database supaya app tersebut bisa digunakan. gunakan 'python manage.py migrate'. command migrate akan mencari setting INSTALLED_APPS dan membuatkan table dari app app tersebut. dalam beberapa kasus ngga semua app dibutuhkan, kita bisa bisa mengcomment app app yang ngga dibutuhkan di INSTALLED_APPS
#
# membuat model, model akan mewakili table di database edit 'polls/models.py'

	from django.db import models

	class Question(models.Model):
	    question_text = models.CharField(max_length=200)
	    pub_date = models.DataTimeField('date published')

	class Choice(models.Model):
	    question = models.ForeignKey(Question, on_delete=models.CASCADE)
	    choice_text = models.CharField(max_length=200)
	    votes = models.IntegerField(default=0)

# variabel2 di dalam model class mewakili field database. setiap variabel menggunakan field yang menandaakan setiap tipe data field field yang ada di dalam table. nama variable mewakili nama pada colom table, tapi kamu bisa juga menggunakan nama lain untuk kolom dengan melwatkan argument paling depan di fungsi field beberapa argunment pada field wajib ada contohnya max_length pada CharField. atau argument opsional seperti pada IntegerField untuk mendefinisikan default value.


# dengan mengaktifkan model django bisa membuat schema database dan juga membuat database access API untuk mengakses model model yang sudah dibuat. Pertama jangan lupa menginclude kan app kita di setting INSTALLED_APPS.tambahkan nama aplikasi kita dalam hal ini diwakili oleh PollsConfig di dalam 'polls/apps.py' sehingga kita bisa panggil dengan 'polls.apps.PollsConfig'. Edit setting :

	INSTALLED_APPS = [
	    'polls.apps.PollsConfig',
	    ...
	]

# selanjutanya jalanakn python manage.py makemigrations Polls. command diatas ngasih tau django kalau kamu baru saja melakukan perubahan di models mu, dan perubahan ini bakal disimpan sebagai migration command makemigrations akan menggenerate fungsi untuk membuat schema di database kita. fungsi tersebut akan terbentuk di dalam 'polls/migrations/0001_initial.py', setelah itu kita akan mengapply file hasil migrations tadi dan membuat kan schema untukmu. kalau mau ngecek SQL nya bisa dengan command python manage.py sqlmigrate polls 0001. kalau mau ngecek aja ada error apa ngga gunakan python manage.py check. okee.. commit menggunakan python manage.py migrate


# mari kita coba access api nya pake python shell dulu 'python manage.py shell'
	>>>from polls.models import Choice, Question
	<QuerySet []>

	>>> from django.utils import timezone
	>>> q = Question(question_text="What's new?", pub_date=timezone.now())
	>>> q.save()
# check object q akan memiliki values
	>>> q.id
	1
	>>> q.question_text
	"What's new?"
	>>> q.pub_date
	datetime.datetime(2019, 12, 29, 2, 29, 44, 166640, tzinfo=<UTC>)
	>>>
	>>> q.question_text="what's up dude ?" #merubah value
	>>> Question.objects.all() #menampilkan semua question di databases
	<QuerySet [<Question: Question object (1)>]> #tampilan nya ngga bagus jadi tambahin __str__()methode ke class Question dan choice_text

	from django.db import models

	class Question(models.Model):
	    ...
	    def __str__(self):
		return self.question_text

	class Choice(models.Mode):
	    def __str__(self):
		return self.choice_text

# tambahkan method was published recently di class Question
	import datetime
	...
	import django.utils import timezone
	...
	def was_published_recently(self):
	    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


# check lagi di shell, python manage.py shell
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

# membuat admin mysite, 'python manage.py createsuperuser' admin site punya editable content group dan user. they are provided by django.contrib.auth. MANA polls nya ? kita harus meregister nya dulu. kita harus memberi tahu admin bahwa Question objects memiliki admin interface. to do this buka 'polls/admin.py' file. dan edit

	from django.contrib import admin
	from .models import Question

	admin.site.register(Question)
	
################ Writing your first Django app part 1 -2 ######################
