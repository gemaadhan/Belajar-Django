# Mari tambahkan more views ke 'polls/views.py' views ini sedikit berbeda karena dia mengambil sebuah argument.

    def detail(request,question_id):
        return HttpResponse("You're looking at question %s" % question_id)

    def results(request,question_id):
        response = "You're looking at the results of question %s."
        return HttpResponse(response % question_id)

    def vote(request,question_id):
        return HttpResponse("You're voting on question %s" % question_id)

#hubungkan views di atas dengan polls.urls dengan membuat path() berikut :

    from django.urls import path
    from . import views

    urlpatterns=[
        path('', views.index, name='index'), #/polls/
        path('<int:question_id>/', views.detail, name='detail'), #/polls/5
        path('<int:question_id>/results/', views.results, name='results'), #polls/5/results
        path('<int:question_id>>/vote', views.vote, name='vote'),#polls/5/vote
    ]

# mari kita menampilkan sesuatu yang lain edit indeex di 'polls.views'

    from django.http import HttpResponse
    from .models import Question

    def index(request):
        latest_question_list = Question.objects.order_by('-pub_date')
        output = ', '.join([q.question_text for q in latest_question_list])
        return HttpResponse(output)

#code diatas memiliki masalah. jika kita ingin merubah tampilan, kita harus mengedit code python di atas. lebih baik gunakan template untuk memisahkan design pada python.

# pertama kita perlu membuat direktori polls/templates. (secara default APP_DIRS di set ke True, secara desain django akan mencari templates subdirektoru di setiap INSTALLED_APPS.) kemudian di dalam folder templates yang sudah dibuat bikin lagi folder dengan nama polls kemudian buat file index.html di dalamnya. karena app_directories loader bekerja seperti yang dijelaskan di atas, kita bisa merefer file kita hanya dengan 'polls/index.html'.

#kenapa kita buat folder polls lagi di dalam polls/templates ? karena django akan memilih folder template yang pertama ditemukan, jika kita punya folder template lagi di app lain, django ngga bisa membedakannya. sehingga kita perlu men-namespacing mereka. dengan meleltakan template tadi didalam direktoru yang dinamai dengan nama aplikasi tersebut.

#polls/templates/polls/index.html
    {% if latest_question_list %}
        <ul>
        {% for question in latest_question_list %}
            <li><a href="/polls/{{ question.id }}/">{{question.question_text}}</a></li>

        {% endfor %}
        </ul>
    {% else %}
        <p>No polls are available.</p>
    {% endif %}

#sekarang rubah polls/views.py biar bisa menggunakan template
    
