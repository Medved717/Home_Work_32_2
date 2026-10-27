from rest_framework.pagination import PageNumberPagination

class CoursePaginations(PageNumberPagination):
    page_size = 10
    max_page_size = 20
    page_size_query_param = 'course_page_size'

class LessonPaginations(PageNumberPagination):
    page_size = 20
    max_page_size = 30
    page_size_query_param = 'lesson_page_size'