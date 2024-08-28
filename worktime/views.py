from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models import F, Value, Func
from django.db.models.functions import TruncMonth, TruncDate, ExtractMonth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import datetime
from . import models, forms

class WorkView(ListView):
    template_name = "work.html"
    model = models.Work

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.form = request.session.get('form', "")

        if self.form:
            del request.session['form']

        category_id = request.session.get('category', "")
        if not category_id:
            self.category = models.Category.objects.first()
            request.session['category'] = self.category.id
        else:
            self.category = models.Category.objects.get(id=category_id)

        self.show_more = int(request.GET.get('more', "1"))

        return super(WorkView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        last_work = models.Work.objects.first()
        works = models.Work.objects.filter(category=self.category).exclude(type=models.Types.HOLIDAY)
        if last_work:
            ## GET parameter ?more is a multiple of 3 month
            offset = last_work.dateFrom-datetime.timedelta(days=31*3*self.show_more)
            works = works.filter(dateFrom__gte=offset)

        work_sum = models.Work.objects.filter(category=self.category).exclude(type=models.Types.HOLIDAY).annotate(month=TruncMonth('dateFrom')).values('month').annotate(duration_sum=Sum('duration')/60/60).order_by('-month')[:6]
        holiday_sum = models.Work.objects.filter(category=self.category).filter(type=models.Types.HOLIDAY).filter(dateFrom__year=timezone.now().year).aggregate(holiday_sum=((Sum('duration')) / Value(60*60)))['holiday_sum'] or 0
        holiday_total = 30

        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        #context['modals'] = self.modal_add
        #context['notify'] = self.notify
        context['works'] = works
        context['current'] = models.Work.objects.filter(category=self.category).filter(type=models.Types.WORK).filter(dateTo__isnull=True).first()
        context['graphData'] = {
            'holiday': {'data': [holiday_sum, holiday_total-holiday_sum], 'label': ['genommen', 'verbleibend']},
            'work': {'data': [w["duration_sum"] for w in work_sum], 'label': [l["month"].strftime("%B %Y") for l in work_sum]}
        }
        context['holidays'] =  models.Work.objects.filter(category=self.category).filter(type=models.Types.HOLIDAY).all()
        context['categories'] = models.Category.objects.all()
        context['current_category'] = self.category
        context['form'] = self.form
        context['more'] = self.show_more + 1
        return context


class WorkCreateView(CreateView):
    model = models.Work
    template_name = "work_form.html"
    form_class = forms.WorkCreateForm
    success_url = "/worktime"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        category_id = request.session.get('category', "")
        if category_id:
            self.current_category = models.Category.objects.get(id=category_id)
        else:
            self.current_category = models.Category.objects.first()

        if request.method == "POST":
            request.session['form'] = self.get_form(form_class=self.get_form_class()).non_field_errors()
        return super(WorkCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['current_category'] = self.current_category
        return initial

    def form_invalid(self, form):
        super(WorkCreateView, self).form_invalid(form)
        return redirect('worktime_index')

class WorkUpdateView(UpdateView):
    model = models.Work
    template_name = "work_form.html"
    form_class = forms.WorkUpdateForm
    success_url = "/worktime"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WorkUpdateView, self).dispatch(*args, **kwargs)

class WorkDeleteView(DeleteView):
    model = models.Work
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('worktime_index')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WorkDeleteView, self).dispatch(*args, **kwargs)

@login_required
def WorkEnd(request, id):
    try:
        work = models.Work.objects.get(id=id)
    except ObjectDoesNotExist:
        work = None

    if work:
        work.dateTo = timezone.now()
        work.duration = work.calculateDuration()
        work.save()

    return redirect('worktime_index')

@login_required
def change_category(request, id):
    request.session['category'] = id
    return redirect('worktime_index')

class CategoryView(ListView):
    template_name = 'category.html'
    model = models.Category

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.form = request.session.get('form', "")
        if self.form:
            del request.session['form']
        return super(CategoryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['form'] = self.form
        return context

class CategoryCreateView(CreateView):
    model = models.Work
    template_name = "category_form.html"
    form_class = forms.CategoryForm
    success_url = "/worktime/category"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            request.session['form'] = self.get_form(form_class=self.get_form_class()).non_field_errors()
        return super(CategoryCreateView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        super(CategoryCreateView, self).form_invalid(form)
        return redirect('category_index')

class CategoryUpdateView(UpdateView):
    model = models.Category
    template_name = "category_form.html"
    form_class = forms.CategoryForm
    success_url = "/worktime/category"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CategoryUpdateView, self).dispatch(*args, **kwargs)

class CategoryDeleteView(DeleteView):
    model = models.Category
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('category_index')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WorkDeleteView, self).dispatch(*args, **kwargs)

def install(request):
    pass
#     data = [("2019-08-22 10:51:00","2019-08-22 14:54:00"),
# ("2019-08-23 10:53:00","2019-08-23 13:41:57"),
# ("2019-09-05 10:55:00","2019-09-05 14:14:17"),
# ("2019-09-06 05:34:00","2019-09-06 06:52:58"),
# ("2019-09-06 09:40:00","2019-09-06 13:36:00"),
# ("2019-09-09 19:24:00","2019-09-09 23:05:00"),
# ("2019-09-12 10:30:00","2019-09-12 14:59:00"),
# ("2019-09-13 11:12:05","2019-09-13 14:49:54"),
# ("2019-09-19 11:50:06","2019-09-19 15:50:07"),
# ("2019-09-20 11:01:00","2019-09-20 13:08:00"),
# ("2019-09-26 10:45:49","2019-09-26 15:18:00"),
# ("2019-09-27 10:38:46","2019-09-27 13:55:14"),
# ("2019-10-03 11:56:29","2019-10-03 14:25:56"),
# ("2019-10-04 10:14:09","2019-10-04 15:03:40"),
# ("2019-10-07 08:00:00","2019-10-07 15:23:00"),
# ("2019-10-10 09:23:00","2019-10-10 14:46:00"),
# ("2019-10-17 09:36:00","2019-10-17 12:46:00"),
# ("2019-10-18 09:47:49","2019-10-18 15:04:33"),
# ("2019-10-24 11:30:00","2019-10-24 15:49:00"),
# ("2019-10-25 09:00:00","2019-10-25 13:58:00"),
# ("2019-10-31 12:10:00","2019-10-31 15:48:00"),
# ("2019-11-01 13:51:02","2019-11-01 17:03:40"),
# ("2019-11-06 10:29:07","2019-11-06 10:59:32"),
# ("2019-11-07 14:16:00","2019-11-07 17:59:00"),
# ("2019-11-08 13:01:23","2019-11-08 16:41:24"),
# ("2019-11-14 14:38:00","2019-11-14 15:35:00"),
# ("2019-11-18 11:17:00","2019-11-18 13:01:10"),
# ("2019-11-21 13:00:00","2019-11-21 16:15:18"),
# ("2019-11-22 09:00:00","2019-11-22 13:42:12"),
# ("2019-11-26 17:30:00","2019-11-26 18:46:36"),
# ("2019-11-27 10:34:00","2019-11-27 12:34:51"),
# ("2019-11-28 12:48:26","2019-11-28 16:52:22"),
# ("2019-12-05 13:30:00","2019-12-05 15:00:00"),
# ("2019-12-06 12:40:00","2019-12-06 14:57:05"),
# ("2019-12-12 13:13:03","2019-12-12 17:12:26"),
# ("2019-12-13 10:41:17","2019-12-13 12:55:46"),
# ("2019-12-13 13:59:00","2019-12-13 17:29:06"),
# ("2019-12-16 14:03:00","2019-12-16 16:03:41"),
# ("2019-12-19 13:52:43","2019-12-19 15:37:05"),
# ("2019-12-20 10:15:49","2019-12-20 17:53:14"),
# ("2019-12-27 12:00:00","2019-12-27 19:55:40"),
# ("2020-01-02 10:48:24","2020-01-02 18:56:09"),
# ("2020-01-07 11:21:00","2020-01-07 15:36:54"),
# ("2020-01-09 13:39:30","2020-01-09 17:30:04"),
# ("2020-01-15 10:59:00","2020-01-15 12:49:03"),
# ("2020-01-16 08:43:00","2020-01-16 09:43:00"),
# ("2020-01-16 13:43:00","2020-01-16 17:53:28"),
# ("2020-01-17 08:51:00","2020-01-17 16:41:00"),
# ("2020-01-18 07:35:00","2020-01-18 16:36:00"),
# ("2020-01-27 14:55:00","2020-01-27 16:22:43"),
# ("2020-01-30 13:25:00","2020-01-30 15:43:00"),
# ("2020-02-03 16:48:00","2020-02-03 17:59:00"),
# ("2020-02-06 13:27:00","2020-02-06 18:17:40"),
# ("2020-02-07 13:07:00","2020-02-07 17:07:45"),
# ("2020-02-13 13:07:07","2020-02-13 18:04:41"),
# ("2020-02-14 13:46:17","2020-02-14 17:37:53"),
# ("2020-02-21 10:32:08","2020-02-21 16:22:54"),
# ("2020-02-27 11:02:00","2020-02-27 17:35:58"),
# ("2020-02-28 11:13:00","2020-02-28 16:50:42"),
# ("2020-03-03 11:12:17","2020-03-03 12:53:44"),
# ("2020-03-05 11:35:00","2020-03-05 16:26:13"),
# ("2020-03-06 09:43:00","2020-03-06 15:43:58"),
# ("2020-03-12 10:05:00","2020-03-12 15:20:00"),
# ("2020-03-13 06:50:00","2020-03-13 12:45:42"),
# ("2020-03-22 18:45:55","2020-03-22 21:17:13"),
# ("2020-03-16 08:26:00","2020-03-16 14:38:00"),
# ("2020-03-17 07:38:00","2020-03-17 09:39:00"),
# ("2020-03-19 10:27:00","2020-03-19 12:40:00"),
# ("2020-03-20 06:59:00","2020-03-20 09:34:00"),
# ("2020-03-24 17:43:00","2020-03-24 19:43:28"),
# ("2020-03-30 10:46:00","2020-03-30 14:46:21"),
# ("2020-04-02 07:37:24","2020-04-02 11:04:31"),
# ("2020-04-10 11:00:00","2020-04-10 17:27:00"),
# ("2020-04-15 10:00:00","2020-04-15 12:38:10"),
# ("2020-04-17 07:47:20","2020-04-17 10:01:23"),
# ("2020-04-17 11:02:00","2020-04-17 13:43:54"),
# ("2020-04-21 15:47:00","2020-04-21 17:47:56"),
# ("2020-04-22 12:55:00","2020-04-22 15:56:08"),
# ("2020-04-23 11:18:00","2020-04-23 17:34:00"),
# ("2020-04-28 10:07:00","2020-04-28 13:07:14"),
# ("2020-04-29 13:07:00","2020-04-29 15:07:42"),
# ("2020-04-29 18:40:00","2020-04-29 21:40:25"),
# ("2020-05-02 09:55:00","2020-05-02 13:34:00"),
# ("2020-05-04 09:35:00","2020-05-04 13:35:23"),
# ("2020-05-04 14:36:33","2020-05-04 15:30:09"),
# ("2020-05-05 09:05:00","2020-05-05 11:42:00"),
# ("2020-05-05 13:24:00","2020-05-05 15:05:00"),
# ("2020-05-07 21:21:00","2020-05-07 22:21:00"),
# ("2020-05-11 07:31:00","2020-05-11 12:43:45"),
# ("2020-05-14 09:29:00","2020-05-14 11:46:26"),
# ("2020-05-15 10:28:00","2020-05-15 13:18:00"),
# ("2020-05-15 16:18:00","2020-05-15 20:19:14"),
# ("2020-05-18 07:42:14","2020-05-18 11:39:58"),
# ("2020-05-18 13:25:00","2020-05-18 15:19:42"),
# ("2020-05-22 08:18:55","2020-05-22 14:17:17"),
# ("2020-05-25 08:02:04","2020-05-25 12:39:53"),
# ("2020-05-25 16:00:00","2020-05-25 17:56:30"),
# ("2020-05-26 13:20:43","2020-05-26 17:01:34"),
# ("2020-05-29 12:35:00","2020-05-29 16:51:41"),
# ("2020-06-03 12:30:00","2020-06-03 16:39:00"),
# ("2020-06-05 07:13:00","2020-06-05 14:00:00"),
# ("2020-06-08 04:22:00","2020-06-08 05:23:00"),
# ("2020-06-08 07:05:00","2020-06-08 15:33:37"),
# ("2020-06-10 09:00:00","2020-06-10 11:31:47"),
# ("2020-06-11 09:53:00","2020-06-11 14:00:00"),
# ("2020-06-12 12:00:00","2020-06-12 15:24:40"),
# ("2020-06-15 09:12:34","2020-06-15 17:24:47"),
# ("2020-06-22 08:59:00","2020-06-22 12:00:00"),
# ("2020-06-29 08:05:32","2020-06-29 13:38:55"),
# ("2020-07-03 10:19:57","2020-07-03 15:12:58"),
# ("2020-07-06 08:45:13","2020-07-06 15:26:30"),
# ("2020-07-10 12:09:00","2020-07-10 15:55:44"),
# ("2020-07-13 08:26:00","2020-07-13 12:46:52"),
# ("2020-07-13 13:31:00","2020-07-13 16:32:43"),
# ("2020-07-17 08:03:32","2020-07-17 16:02:13"),
# ("2020-07-20 08:48:55","2020-07-20 16:26:26"),
# ("2020-07-23 09:12:03","2020-07-23 13:07:12"),
# ("2020-07-27 08:36:00","2020-07-27 15:04:31"),
# ("2020-08-01 18:19:00","2020-08-01 21:54:30"),
# ("2020-08-03 09:28:52","2020-08-03 15:01:54"),
# ("2020-08-06 06:08:00","2020-08-06 11:32:14"),
# ("2020-08-10 08:41:27","2020-08-10 14:39:22"),
# ("2020-08-14 06:30:12","2020-08-14 09:37:51"),
# ("2020-08-17 09:45:52","2020-08-17 16:32:15"),
# ("2020-08-21 06:46:00","2020-08-21 10:11:40"),
# ("2020-08-31 08:41:06","2020-08-31 12:52:22"),
# ("2020-08-31 17:19:12","2020-08-31 19:48:35"),
# ("2020-09-04 07:01:16","2020-09-04 11:50:52"),
# ("2020-09-07 08:21:19","2020-09-07 14:21:39"),
# ("2020-09-09 11:07:02","2020-09-09 12:23:38"),
# ("2020-09-11 06:18:58","2020-09-11 08:13:22"),
# ("2020-09-14 10:00:00","2020-09-14 15:31:01"),
# ("2020-09-18 06:12:53","2020-09-18 11:45:42"),
# ("2020-09-21 08:30:00","2020-09-21 14:00:00"),
# ("2020-09-25 08:19:17","2020-09-25 13:40:16"),
# ("2020-09-28 06:53:00","2020-09-28 14:40:00"),
# ("2020-10-02 16:19:14","2020-10-02 18:52:08"),
# ("2020-10-05 08:36:58","2020-10-05 14:36:19"),
# ("2020-10-09 07:11:47","2020-10-09 12:07:20"),]

#     for d in data:
#         day = models.Work()
#         day.dateFrom = datetime.datetime.strptime(d[0], "%Y-%m-%d %H:%M:%S")
#         day.dateTo = datetime.datetime.strptime(d[1], "%Y-%m-%d %H:%M:%S")
#         day.category = models.Category.objects.first()
#         day.type = models.Types.WORK
#         diff = day.dateTo - day.dateFrom
#         day.duration = diff.total_seconds()
#         day.save()
