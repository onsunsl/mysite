from django.http import HttpResponse
from django.http import Http404
from .models import Question
from django.template import loader
from django.shortcuts import render, get_object_or_404



def detial(request, question_id):
    # 1
    # return HttpResponse("You're looking at question {}.".format(question_id))

    # 2
    # try:
    #     question = Question.objects.get(pk = question_id)
    # except:
    #     raise Http404("Question does not exist!")
    # return render(request, 'polls/detail.html', dict(question = question))

    # 3
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/detail.html', dict(question = question))



def result(request, question_id):
    response = "You're looking at the results of question {}."
    return HttpResponse(response.format(question_id))

def vote(request, question_id):
    return HttpResponse("You're voting on question {}.".format(question_id))

def index(request):
    #第一个写法
    # return HttpResponse("Hello world. You're at the polls index.")

    #第二个写法
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)


    #第三种写法
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {
    #     "latest_question_list":latest_question_list,
    # }
    #
    # # print(template.render(context, request))
    # return HttpResponse(template.render(context, request))

    # 第四种写法
    latest_question_text = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list':latest_question_text
    }
    return render(request, 'polls/index.html', context)

