from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic


def detail(request, question_id):
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




def results(request, question_id):
    # response = "You're looking at the results of question {}."
    # return HttpResponse(response.format(question_id))
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/results.html', dict(question = question))

def vote(request, question_id):
    # return HttpResponse("You're voting on question {}.".format(question_id))
    question = get_object_or_404(Question, pk = question_id)
    try:
        seleted_choice = question.choice_set.get(pk = request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            "question":question,
            "error_message":"You didn't select a choice.",
        })
    else:
        seleted_choice.votes += 1
        seleted_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


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



class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

