from django.views.generic import DetailView, TemplateView

from .models import OS, Release


class DownloadBase(object):
    """ Include latest releases in all views """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'latest_python2': Release.objects.python2().latest(),
            'latest_python3': Release.objects.python3().latest(),
        })
        return context


class DownloadHome(DownloadBase, TemplateView):
    template_name = 'downloads/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'releases': Release.objects.downloads(),
        })

        return context


class DownloadOSList(DownloadBase, DetailView):
    template_name = 'downloads/os_list.html'
    context_object_name = 'os'

    def get_object(self):
        return OS.objects.get(slug=self.kwargs['os_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'releases': Release.objects.filter(files__os__slug=self.object.slug).select_related()
        })
        return context


class DownloadReleaseDetail(DownloadBase, DetailView):
    template_name = 'downloads/release_detail.html'
    model = Release
    context_object_name = 'release'

    def get_object(self):
        return self.get_queryset().select_related().get(slug=self.kwargs['release_slug'])
