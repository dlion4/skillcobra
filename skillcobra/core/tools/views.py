from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from skillcobra.core.views import AuthorizedHomeViewMixin


class ArtificialIntelligenceToolsView(AuthorizedHomeViewMixin):
    template_name = "pages/ai_tools.html"


class PdfReaderView(AuthorizedHomeViewMixin):
    template_name = "pages/pdf_reader.html"


class ChatWithPdfView(AuthorizedHomeViewMixin):
    template_name = "pages/chat_with_pdf.html"


class ChatEmbedPdfView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        return JsonResponse(
            {"message": "You'll ve notified once the embedding is complete"},
            status=200,
        )



