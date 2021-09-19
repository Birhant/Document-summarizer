from django.urls import path
from . import views
from . import views_keyword
from . import views_normalize

urlpatterns = [
    path('book_summarizer/upload/', views.upload_single_book, name="UploadSingleBook"),
    path('book_summarizer/upload/read/', views.read_single_book, name="ReadSingleBook"),
    path('book_summarizer/upload/read/extract/<password>/', views.extract_single_book, name="ExtractSingleBook"),
    path('book_summarizer/upload/read/heading_text/', views.headings_single_book, name="HeadingSingleBook"),
    path('book_summarizer/upload/read/extract/heading_text/summarize/', views.summarize_single_book, name="SummarizeSingleBook"),
    path('book_summarizer/upload/read/extract/heading_text/summarize/export/', views.export_single_book, name="ExportSingleBook"),
    path('book_summarizer/remove/', views.remove_single_book, name="RemoveSingleBook"),
    #keyword
    path('keyword_summarizer/upload', views_keyword.upload_multiple_book, name="UploadMultipleBook"),
    path('keyword_summarizer/upload/read/', views_keyword.read_multiple_book, name="ReadMultipleBook"),
    path('keyword_summarizer/remove/', views_keyword.remove_multiple_book, name="RemoveMultipleBook"),
    path('keyword_summarizer/upload/read/summarize/', views_keyword.summarize_multiple_book, name="SummarizeMultipleBook"),
    path('keyword_summarizer/upload/read/summarize/export/', views_keyword.export_multiple_book, name="ExportMultipleBook"),
    #pdf normalizer
    path('toc_generator_summarizer/upload/', views_normalize.upload_broken_book, name="UploadBrokenBook"),
    path('toc_generator_summarizer/remove/', views_normalize.remove_broken_book, name="RemoveBrokenBook"),
    path('toc_generator_summarizer/upload/read/', views_normalize.read_broken_book, name="ReadBrokenBook"),
    path('toc_generator_summarizer/upload/read/toc/', views_normalize.view_toc, name="ViewToCBook"),
    path('toc_generator_summarizer/upload/read/toc/export/', views_normalize.export_broken_book, name="ExportBrokenBook"),
    path('toc_generator_summarizer/upload/read/<password>/', views_normalize.correct_broken_book, name="GenerateToCBook"),

]



