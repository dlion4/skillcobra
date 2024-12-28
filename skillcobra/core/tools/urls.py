from django.urls import path

from . import views

app_name = "tools"


urlpatterns = [
    path(
        "",
        views.ArtificialIntelligenceToolsView.as_view(),
        name="ai_tools_view",
    ),
    path(
        "chat-with-pdf/",
        views.ChatWithPdfView.as_view(),
        name="chat_with_pdf_view",
    ),
    path(
        "chat-embed-docx-pd/",
        views.ChatEmbedPdfView.as_view(),
        name="embed_pdf_file_view",
    ),
]
