from rest_framework import viewsets

from .models import Question, Questionnaire, Theme

from .serializers import QuestionSerializer, QuestionnaireSerializer, ThemeSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.filter(
            theme__questionnaire__control__in=self.request.user.profile.controls.all())
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Instead of rendering a list, we reformat the response data to render
        a dict where the key is the question id.
        """
        response = super(QuestionViewSet, self).list(request, *args, **kwargs)
        dict_data = {}
        for elem in response.data:
            question_id = elem['id']
            dict_data[question_id] = elem
        response.data = dict_data
        return response


class ThemeViewSet(viewsets.ModelViewSet):
    serializer_class = ThemeSerializer

    def get_queryset(self):
        queryset = Theme.objects.filter(
            questionnaire__control__in=self.request.user.profile.controls.all())
        return queryset


class QuestionnaireViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionnaireSerializer

    def get_queryset(self):
        queryset = Questionnaire.objects.filter(
            control__in=self.request.user.profile.controls.all())
        return queryset

    def create(self, request, *args, **kwargs):
        themes_data = request.data.pop('themes')

        response = super(QuestionnaireViewSet, self).create(request, *args, **kwargs)

        saved_themes = self.save_themes_and_questions(themes_data, response.data['id'])

        response.data['themes'] = saved_themes
        return response

    def save_themes_and_questions(self, themes_data, questionnaire_id):
        saved_themes = []
        for theme_data in themes_data:
            questions_data = theme_data.pop('questions')
            saved_theme_json = self.save_theme(theme_data, questionnaire_id)
            saved_questions_json = self.save_questions(questions_data, saved_theme_json['id'])
            saved_theme_json['questions'] = saved_questions_json
            saved_themes.append(saved_theme_json)
        return saved_themes

    def save_theme(self, theme_data, questionnaire_id):
        theme_data['questionnaire'] = questionnaire_id
        return self.save(ThemeSerializer, theme_data)

    def save_questions(self, questions_data, theme_id):
        saved_questions_json = []
        for question_data in questions_data:
            question_data['theme'] = theme_id
            saved_question_json = self.save(QuestionSerializer, question_data)
            saved_questions_json.append(saved_question_json)
        return saved_questions_json

    def save(self, serializer_class, data):
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        saved = serializer.save()
        saved_json = serializer.data
        return saved_json

    def update(self, request, *args, **kwargs):
        response = super(QuestionnaireViewSet, self).update(request, *args, **kwargs)
        return response





