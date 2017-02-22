from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.template import loader

from .models import Question, Choice

from django.http import Http404


from django.views import generic

# def index(request):
# 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
# 	template = loader.get_template('polls/index.html')
# 	context = {
# 		'latest_question_list': latest_question_list,
# 	}
# 	# output = ', '.join([q.question_text for q in latest_question_list])
# 	return HttpResponse(template.render(context, request))
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	template = loader.get_template('polls/index.html')
	context = {
		'latest_question_list': latest_question_list,
	}
	return render(request, 'polls/index.html', context)

# def detail(request, question_id):
# 	try:
# 		quesiton = Question.objects.get(pk=question_id)
# 	except quesiton.DoesNotExist:
# 		raise Http404("Question does not exist")
# 	# return HttpResponse("You're looking at quesiton %s." % question_id)
# 	return render(request, 'polls/detail.html', {'quesiton' : quesiton})

# def detail(request, question_id):
# 	quesiton = get_object_or_404(Question, pk=question_id)
# 	return render(request, 'polls/detail.html', {'quesiton' : quesiton})

# # def results(request, question_id):
# # 	response = "You're looking at the results of quesiton %s."
# # 	return HttpResponse(response % question_id)
# def results(request, question_id):
# 	quesiton = get_object_or_404(Question, pk=question_id)
# 	return render(request, 'polls/results.html', {'question': question})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question':question,
			'error_message': "You didn't select a choice.",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
