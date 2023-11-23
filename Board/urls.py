from django.urls import path

from Board.views import QuestionAPIView,QuestionDetailAPIView,MyQuestionAPIView,AnswerAPIView
from . import views

urlpatterns= [
     path('question/', QuestionAPIView.as_view()),
     path('question/<int:pk>/', QuestionDetailAPIView.as_view()),

     path('mine/', MyQuestionAPIView.as_view()),

     path('answer/<int:pk>/', AnswerAPIView.as_view()),

]