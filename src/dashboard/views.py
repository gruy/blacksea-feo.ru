# -*- coding: utf-8 -*-
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms import CheckboxSelectMultiple, ModelForm, SelectMultiple
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import DetailView, FormView, RedirectView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView


from src.dashboard.forms import ContactsForm, IndexPageForm
from src.dashboard.models import IndexPage
from src.rooms.models import Comfort, Photo, Price, Room
from src.photos.models import Photo as PhotoGallery, Slider
from src.services.models import Service, ServicePhoto


class LoginView(FormView):
    success_url = '/dashboard/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'dashboard/login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(LoginView, self).get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs['class'] = 'form-control'
        return form

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    url = '/dashboard/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            data = {
                'result': 'error',
                'html': render_to_string(self.template_name, self.get_context_data(), context_instance=RequestContext(self.request)),
            }
            return JsonResponse(data, safe=False, status=200)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'result': 'success',
                'success_url': self.get_success_url(),
                'html': render_to_string(self.template_name, self.get_context_data(), context_instance=RequestContext(self.request)),
            }
            return JsonResponse(data)
        else:
            return response

    def get(self, request, *args, **kwargs):
        response = super(AjaxableResponseMixin, self).get(request, *args, **kwargs)
        if self.request.is_ajax():
            data = {
                'result': 'success',
                'html': render_to_string(self.template_name, self.get_context_data(**kwargs), context_instance=RequestContext(self.request)),
            }
            return JsonResponse(data)
        else:
            return response


class IndexPageView(LoginRequiredMixin, FormView):
    form_class = IndexPageForm
    template_name = 'dashboard/index-page.html'

    def get(self, request, *args, **kwargs):
        self.sliders = Slider.objects.all()
        super(IndexPageView, self).get(request, *args, **kwargs)
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['active_section'] = 'index-page'
        context['sliders'] = self.sliders
        return context

    def get_initial(self):
        page, created = IndexPage.objects.get_or_create(pk=1)
        return {'text': page.text, 'order_text': page.order_text, }

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files[]')
        if files:
            for file in files:
                slider = Slider()
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(file.read())
                img_temp.flush()
                slider.image.save(file.name, File(img_temp))
                slider.save()

            return JsonResponse({'result': 'ok', });
        else:
            page, created = IndexPage.objects.get_or_create(pk=1)
            page.text = request.POST.get('text')
            page.order_text = request.POST.get('order_text')
            page.save()
            return HttpResponseRedirect(reverse('dashboard:index-page'))


class RoomsListView(LoginRequiredMixin, ListView):
    context_object_name = 'rooms'
    model = Room
    template_name = 'dashboard/rooms.html'

    def get_context_data(self, **kwargs):
        context = super(RoomsListView, self).get_context_data(**kwargs)
        context['active_section'] = 'rooms'
        return context


class RoomAddView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    context_object_name = 'room'
    fields = ['title', 'quantity', 'rooms', 'persons', 'places', 'places_additional']
    model = Room
    template_name = 'dashboard/room_add.html'

    def get_context_data(self, **kwargs):
        context = super(RoomAddView, self).get_context_data(**kwargs)
        context['active_section'] = 'rooms'
        context['active_menu'] = 'room_edit'
        return context

    def get_success_url(self):
        return reverse('dashboard:room-edit', args=[self.object.id, ])


class RoomEditView(LoginRequiredMixin, UpdateView):
    context_object_name = 'room'
    fields = ['title', 'is_visible', 'quantity', 'numbers', 'rooms', 'persons', 'places', 'places_additional', 'comforts', 'text']
    model = Room
    template_name = 'dashboard/room_edit.html'

    def get_form(self, form_class):
        form = super(RoomEditView, self).get_form(form_class)
        form.fields['comforts'].widget = CheckboxSelectMultiple()
        form.fields['comforts'].queryset = Comfort.objects.all()
        for field_name, field in form.fields.items():
            if field_name in ['comforts', 'is_visible']:
                continue
            field.widget.attrs['class'] = 'form-control'
        return form

    def get_context_data(self, **kwargs):
        context = super(RoomEditView, self).get_context_data(**kwargs)
        context['active_section'] = 'rooms'
        context['active_menu'] = 'room_edit'
        return context

    def get_success_url(self):
        return reverse('dashboard:room-edit', args=[self.object.id, ])


class RoomPhotoView(LoginRequiredMixin, DetailView):
    context_object_name = 'room'
    model = Room
    template_name = 'dashboard/room_photo.html'

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files[]')
        object = self.get_object()
        try:
            i = Photo.objects.filter(room=object).order_by('-order')[:1].get().order
        except Photo.DoesNotExist:
            i = 1
        for file in files:
            photo = Photo(room=object, order=i)
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(file.read())
            img_temp.flush()
            photo.image.save(file.name, File(img_temp))
            photo.save()
            i += 1

        return JsonResponse({'result': 'ok', });
#        return HttpResponseRedirect(reverse('dashboard:room-photo', args=[object.id, ]))

    def get_context_data(self, **kwargs):
        context = super(RoomPhotoView, self).get_context_data(**kwargs)
        context['active_section'] = 'rooms'
        context['active_menu'] = 'room_photo'
        return context

    def get_success_url(self):
        return reverse('dashboard:room-photo', args=[self.object.id, ])


class RoomPriceView(LoginRequiredMixin, DetailView):
    context_object_name = 'room'
    model = Room
    success_url = reverse_lazy('dashboard:rooms')
    template_name = 'dashboard/room_price.html'

    def get_context_data(self, **kwargs):
        context = super(RoomPriceView, self).get_context_data(**kwargs)
        context['active_section'] = 'rooms'
        context['active_menu'] = 'room_price'
        return context

    def get_success_url(self):
        return reverse('dashboard:room-price', args=[self.object.id, ])


class RoomPhotoSortView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        sorts = request.GET.getlist('photo[]')
        i = 1
        for s in sorts:
            photo = Photo.objects.get(pk=s)
            photo.order = i
            photo.save()
            i += 1
        return HttpResponse('ok')


class RoomPhotoEditView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        ctx = {'result': 'error'}

        photo = Photo.objects.get(pk=kwargs['photo_id'])

        if 'delete' in request.GET:
            ctx['action'] = 'delete'
            photo.delete()
            ctx['result'] = 'ok'


        if 'main' in request.GET:
            ctx['action'] = 'main'
            Photo.objects.filter(room=photo.room).update(cover=False)
            photo.cover = True
            photo.save()
            ctx['result'] = 'ok'

#        context = self.get_context_data(**kwargs)
        return self.render_to_response(ctx)

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, **response_kwargs)


class RoomPriceAddView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    model = Price
    fields = ['title', 'date_start', 'date_end', 'price_min', 'price_max']
    template_name = 'dashboard/room_price_form.html'

    def get_form(self, form_class):
        form = super(RoomPriceAddView, self).get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs['class'] = 'form-control'
        return form

    def get_initial(self):
        try:
            self.room = Room.objects.get(pk=self.kwargs['pk'])
        except Room.DoesNotExist:
            self.room = None

        return {'room': self.room, }

    def get_context_data(self, **kwargs):
        context = super(RoomPriceAddView, self).get_context_data(**kwargs)
        context['room'] = self.room
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.room = self.room
        return super(RoomPriceAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse('dashboard:room-price', args=[self.room.id, ])


class RoomPriceEditView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    model = Price
    fields = ['title', 'date_start', 'date_end', 'price_min', 'price_max']
    context_object_name = 'price'
    pk_url_kwarg = 'pk'
    template_name = 'dashboard/room_price_edit.html'

    def get_form(self, form_class):
        form = super(RoomPriceEditView, self).get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs['class'] = 'form-control'
        return form

    def get_success_url(self):
        return reverse('dashboard:room-price', args=[self.object.room_id, ])


class RoomPriceDeleteView(LoginRequiredMixin, DeleteView):
    context_object_name = 'price'
    model = Price
    pk_url_kwarg = 'pk'
    template_name = 'dashboard/room_price_delete.html'

    def get_success_url(self):
        return reverse('dashboard:room-price', args=[self.object.room_id, ])


class PhotoForm(ModelForm):
    fields = ['image', ]
    model = PhotoGallery


class PhotoView(LoginRequiredMixin, ListView):
    context_object_name = 'photos'
    model = PhotoGallery
    template_name = 'dashboard/photos.html'

    def get_context_data(self, **kwargs):
        context = super(PhotoView, self).get_context_data(**kwargs)
        context['active_section'] = 'photos'
        return context

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files[]')
        for file in files:
            photo = PhotoGallery(tag=0)
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(file.read())
            img_temp.flush()
            photo.image.save(file.name, File(img_temp))
            photo.save()

        return JsonResponse({'result': 'ok', });


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    context_object_name = 'photo'
    model = PhotoGallery
    pk_url_kwarg = 'pk'
    template_name = 'dashboard/photo_delete.html'

    def get_success_url(self):
        return reverse('dashboard:photos')


class PhotoSortView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        sorts = request.GET.getlist('photo[]')
        i = 1
        for s in sorts:
            photo = PhotoGallery.objects.get(pk=s)
            photo.order = i
            photo.save()
            i += 1
        return HttpResponse('ok')


class SliderSortView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        sorts = request.GET.getlist('photo[]')
        i = 1
        for s in sorts:
            slider = Slider.objects.get(pk=s)
            slider.order = i
            slider.save()
            i += 1
        return HttpResponse('ok')


class SliderDeleteView(LoginRequiredMixin, DeleteView):
    context_object_name = 'slider'
    model = Slider
    pk_url_kwarg = 'pk'
    template_name = 'dashboard/slider_delete.html'

    def get_success_url(self):
        return reverse('dashboard:index-page')


class ServicesView(LoginRequiredMixin, ListView):
    context_object_name = 'services'
    model = Service
    template_name = 'dashboard/services.html'

    def get_context_data(self, **kwargs):
        context = super(ServicesView, self).get_context_data(**kwargs)
        context['active_section'] = 'services'
        return context


class ServiceAddView(LoginRequiredMixin, CreateView):
    model = Service
    fields = ['title', 'image', 'mini_text', 'text']
    success_url = reverse_lazy('dashboard:services')
    template_name = 'dashboard/service_form.html'

    def get_form(self, form_class):
        form = super(ServiceAddView, self).get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs['class'] = 'form-control'
        return form

    def get_context_data(self, **kwargs):
        context = super(ServiceAddView, self).get_context_data(**kwargs)
        context['active_section'] = 'services'
        return context


class ServiceEditView(LoginRequiredMixin, UpdateView):
    model = Service
    fields = ['title', 'image', 'mini_text', 'text']
    context_object_name = 'service'
    pk_url_kwarg = 'pk'
    template_name = 'dashboard/service_edit.html'

    def get_form(self, form_class):
        form = super(ServiceEditView, self).get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs['class'] = 'form-control'
        return form

    def get_context_data(self, **kwargs):
        context = super(ServiceEditView, self).get_context_data(**kwargs)
        context['active_section'] = 'services'
        context['active_menu'] = 'service_edit'
        return context

    def get_success_url(self):
        return reverse('dashboard:service-edit', args=[self.object.id, ])


class ServicePhotoView(LoginRequiredMixin, DetailView):
    context_object_name = 'service'
    model = Service
    template_name = 'dashboard/service_photo.html'

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files[]')
        object = self.get_object()
        try:
            i = ServicePhoto.objects.filter(service=object).order_by('-order')[:1].get().order
        except ServicePhoto.DoesNotExist:
            i = 1
        for file in files:
            photo = ServicePhoto(service=object, order=i)
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(file.read())
            img_temp.flush()
            photo.image.save(file.name, File(img_temp))
            photo.save()
            i += 1

        return JsonResponse({'result': 'ok', });

    def get_context_data(self, **kwargs):
        context = super(ServicePhotoView, self).get_context_data(**kwargs)
        context['active_section'] = 'services'
        context['active_menu'] = 'service_photo'
        return context

    def get_success_url(self):
        return reverse('dashboard:service-photo', args=[self.object.id, ])



class ServicePhotoSortView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        sorts = request.GET.getlist('photo[]')
        i = 1
        for s in sorts:
            photo = ServicePhoto.objects.get(pk=s)
            photo.order = i
            photo.save()
            i += 1
        return HttpResponse('ok')


class ServicePhotoEditView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        ctx = {'result': 'error'}

        photo = ServicePhoto.objects.get(pk=kwargs['photo_id'])

        if 'delete' in request.GET:
            ctx['action'] = 'delete'
            photo.delete()
            ctx['result'] = 'ok'

        return self.render_to_response(ctx)

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, **response_kwargs)


class ContactsView(LoginRequiredMixin, FormView):
    form_class = ContactsForm
    success_url = reverse_lazy('dashboard:contacts')
    template_name = 'dashboard/contacts.html'

    def get_context_data(self, **kwargs):
        context = super(ContactsView, self).get_context_data(**kwargs)
        context['active_section'] = 'contacts'
        page, created = IndexPage.objects.get_or_create(pk=1)
        context['obj'] = page
        return context

    def get_form(self, form_class):
        form = super(ContactsView, self).get_form(form_class)
        for field_name, field in form.fields.items():
            if field_name in ['contacts_text', ]:
                continue
            field.widget.attrs['class'] = 'form-control'
        return form

    def get_initial(self):
        c, created = IndexPage.objects.get_or_create(pk=1)
        return {
            'contacts_text': c.contacts_text,
            'phone_1': c.phone_1,
            'phone_2': c.phone_2,
            'phone_3': c.phone_3,
            'address': c.address,
            'email': c.email,
            'skype': c.skype,
            'map': c.map,
        }

    def post(self, request, *args, **kwargs):
        page, created = IndexPage.objects.get_or_create(pk=1)
        page.contacts_text = request.POST.get('contacts_text')
        page.phone_1 = request.POST.get('phone_1')
        page.phone_2 = request.POST.get('phone_2')
        page.phone_3 = request.POST.get('phone_3')
        page.address = request.POST.get('address')
        page.skype = request.POST.get('skype')
        page.email = request.POST.get('email')
        page.map = request.POST.get('map')
        page.save()
        return HttpResponseRedirect(reverse('dashboard:contacts'))
