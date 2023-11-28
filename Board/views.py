from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http import Http404

from Board.serializers import BoardSerializer
from Board.models import BoardModel
from operator import attrgetter

from Accounts.utils import login_check

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions

class AnswerAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 4-4 답변 등록 API
    def put(self,request,pk):
        try:
            #관리자인지 확인
            if request.user.is_staff:
                b = BoardModel.objects.get(pk=pk)

                serializer = BoardSerializer(b, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "답변을 등록할 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except BoardModel.DoesNotExist:
            return Response({"message": "존재하지 않는 게시물입니다."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"message": "answer를 올바르게 전달하세요."}, status=status.HTTP_400_BAD_REQUEST)

class MyQuestionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    #4-7 내 게시물 조회 API
    def get(self, request):
        try:
            b = BoardModel.objects.filter(user_id = request.user.id)
            sorted(b, key= attrgetter('updated_at'), reverse=True)

            if len(b) == 0:
                raise ValidationError

            serializer = BoardSerializer(b, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({"message": "내 게시물이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

class QuestionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    # 4-2 질문 글 리스트 조회 API(업데이트 최신순)
    def get(self, request):
        try:
            b = BoardModel.objects.all().order_by('-updated_at')

            if len(b) == 0:
                raise ValidationError

            serializer = BoardSerializer(b, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({"message": "게시물이 없습니다."}, status=status.HTTP_404_NOT_FOUND)


    # 4-1 질문 글 등록 API
    def post(self, request):
        try:
            data = request.data.copy()

            if 'title' not in data:
                data['title'] = request.user.nickname + "의 글"

            get_object_or_404(BoardModel, user_id= request.user.id, title= data['title'],
                              field= data['field'])

            return Response({"message":"완전히 중복된 글입니다. 다른 글을 작성하세요"}, status= status.HTTP_400_BAD_REQUEST)
        except Http404:
            data['user_id'] = request.user.id
            serializer = BoardSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({"message": "내용을 올바르게 전달하세요."}, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 4-3 해당 pk와 동일한 id를 가진 글 정보 조회 API
    def get(self, request, pk):
        try:
            b = BoardModel.objects.get(pk= pk)
            b.hit_count += 1
            b.save()

            serializer = BoardSerializer(b)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BoardModel.DoesNotExist:
            return Response({"message": "게시물이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    #4-5 질문 글 수정 API(title, field) -> 질문자만 수정 가능
    def put(self, request, pk):
        try:
            # pk와 id가 동일한 객체를 가져옴
            board_obj = BoardModel.objects.get(pk=pk)

            if board_obj.answer is not None:
                return Response({"message": "이미 답변이 달린 글은 수정할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

            #중복처리 진행
            data = request.data.copy()

            if 'title' not in request.data:
                data['title'] = board_obj.title
            elif data['title'] == "":
                data['title'] = request.user.nickname + "의 글"

            if 'field' not in data:
                data['field'] = board_obj.field


            if BoardModel.objects.exclude(pk=pk).filter(user_id = request.user.id,title=data['title'],
                                                            field=data['field']).exists():
                return Response({"message": "수정하려는 글이 완전히 중복된 글입니다."}, status=status.HTTP_400_BAD_REQUEST)

            board_user = board_obj.user_id
            board_id = board_user.id

            if board_id == request.user.id:
                serializer = BoardSerializer(board_obj, data=data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "글을 수정할 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except BoardModel.DoesNotExist:
            return Response({"message": "해당 글 정보가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"message": "입력값을 올바르게 전달하세요."}, status=status.HTTP_400_BAD_REQUEST)

    #4-6 질문 글 삭제 API
    def delete(self, request, pk):
        try:
            board_obj = BoardModel.objects.get(pk=pk)

            board_user = board_obj.user_id
            board_id = board_user.id

            if request.user.id == board_id or request.user.is_staff == 1:
                # 삭제 진행
                board_obj.delete()
                return Response({"message": "삭제 성공"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "글을 삭제할 권한이 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except BoardModel.DoesNotExist:
            return Response({"message": "삭제할 글을 찾지 못했습니다."}, status=status.HTTP_404_NOT_FOUND)
