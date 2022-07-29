import pytest
from rest_framework.test import APIClient
from model_bakery import baker


from students.models import Course, Student



@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_one_course(client, course_factory, student_factory):
    #Arrange
    courses = course_factory(_quantity=3)
    #Act
    response = client.get('/api/v1/courses/2/')
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 2


@pytest.mark.django_db
def test_list_course(client, course_factory, student_factory):
    #Arrange
    courses = course_factory(_quantity=3)
    #Act
    response = client.get('/api/v1/courses/')
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_filter_course_id(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=12)
    course_for_test = Course.objects.create(name='course_for_test')
    #Act
    response = client.get(f'/api/v1/courses/?id={course_for_test.id}')
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == course_for_test.id


@pytest.mark.django_db
def test_filter_course_name(client, course_factory):
    #Arrange
    course_to_test = Course.objects.create(name= 'course_to_test')
    courses = course_factory(_quantity=3)
    #Act
    response = client.get('/api/v1/courses/?name=course_to_test')
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == course_to_test.name


@pytest.mark.django_db
def test_create_course(client, course_factory):
    #Arrange
    course_name = {
        'name': 'course13'
    }
    #Act
    response = client.post('/api/v1/courses/', course_name)
    #Assert
    assert response.status_code == 201
    assert Course.objects.get(name='course13').name == course_name['name']


@pytest.mark.django_db
def test_update_course(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=5)
    course_name = {
        'name': 'course13'
    }
    #Act
    response = client.patch('/api/v1/courses/1/', course_name)
    #Assert
    assert response.status_code == 200
    assert Course.objects.get(id=1).name == course_name['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=2)

    #Act
    response = client.delete('/api/v1/courses/1/')
    #Assert
    assert response.status_code == 204
    assert courses[0].id not in list(course.id for course in Course.objects.all())
