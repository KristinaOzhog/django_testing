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
    courses = course_factory(_quantity=1)
    #Act
    response = client.get(f'/api/v1/courses/{courses[0].id}/')
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == courses[0].id


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
    #Act
    response = client.get(f'/api/v1/courses/?id={courses[9].id}')
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses[9].id


@pytest.mark.django_db
def test_filter_course_name(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=7)
    #Act
    response = client.get(f'/api/v1/courses/?name={courses[5].name}')
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[5].name


@pytest.mark.django_db
def test_create_course(client, course_factory):
    #Arrange
    course_name = {
        'name': 'course13'
    }
    count_courses = Course.objects.count()
    #Act
    response = client.post('/api/v1/courses/', course_name)
    #Assert
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == course_name['name']
    assert Course.objects.count() == count_courses + 1


@pytest.mark.django_db
def test_update_course(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=5)
    course_name = {
        'name': 'course13'
    }
    count_courses = Course.objects.count()
    #Act
    response = client.patch(f'/api/v1/courses/3/', course_name)
    #Assert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course_name['name']
    assert Course.objects.count() == count_courses


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=2)
    #Act
    response = client.delete('/api/v1/courses/1/')
    #Assert
    assert response.status_code == 204
    assert courses[0].id not in list(course.id for course in Course.objects.all())
