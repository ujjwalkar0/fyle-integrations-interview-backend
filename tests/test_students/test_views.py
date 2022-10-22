import json

from django.urls import reverse
import pytest

@pytest.mark.django_db()
def test_student_not_exist(api_client, student_not_exist):
    """
        Test for the student, not registered with the database
    """
    response = api_client.get(
        reverse('students-assignments'),
        HTTP_X_Principal=student_not_exist
    )

    assert response.status_code == 403
    student = response.json()
    student["detail"] = "User not found for this principal"

@pytest.mark.django_db()
def test_no_headers(api_client, student_not_exist):
    """
        Test when no headers are provided
    """
    response = api_client.get(
        reverse('students-assignments'),
    )

    assert response.status_code == 403
    student = response.json()
    student["detail"] = "No X-Principal header found"

@pytest.mark.django_db()
def test_homepage(api_client, student_1):
    """
        Check if homepage loaded successfully.
    """
    response = api_client.get(
        "/",
        HTTP_X_Principal=student_1
    )

    assert response.status_code == 200
    student = response.json()
    student["status"] = "ok"

@pytest.mark.django_db()
def test_get_assignments_student_1(api_client, student_1):
    response = api_client.get(
        reverse('students-assignments'),
        HTTP_X_Principal=student_1
    )

    assert response.status_code == 200

    assignments = response.json()
    assert type(assignments) == list

    for assignment in assignments:
        assert assignment['student'] == 1


@pytest.mark.django_db()
def test_get_assignments_student_2(api_client, student_2):
    response = api_client.get(
        reverse('students-assignments'),
        HTTP_X_Principal=student_2
    )

    assert response.status_code == 200

    assignments = response.json()
    assert type(assignments) == list

    for assignment in assignments:
        assert assignment['student'] == 2


@pytest.mark.django_db()
def test_post_assignment_student_1(api_client, student_1):
    content = 'ABCD TESTPOST'

    response = api_client.post(
        reverse('students-assignments'),
        data=json.dumps({
            'content': content
        }),
        HTTP_X_Principal=student_1,
        content_type='application/json'
    )

    assert response.status_code == 201

    assignment = response.json()
    assert assignment['content'] == content
    assert assignment['state'] == 'DRAFT'
    assert assignment['student'] == 1
    assert assignment['teacher'] is None
    assert assignment['grade'] is None
    assert assignment['id'] is not None

@pytest.mark.django_db()
def test_patch_assignment_not_exist_student_1(api_client, student_1):
    """
        Test for a assignment that is not exist.
    """
    response = api_client.patch(
        reverse('students-assignments'),
        data=json.dumps({
            'id': 18
        }),
        HTTP_X_Principal=student_1,
        content_type='application/json'
    )

    error = response.json()

    print(error)

    assert error['error'] == 'Assignment does not exist/permission denied'
    assert response.status_code == 400


@pytest.mark.django_db()
def test_post_assignment_with_state_student_1(api_client, student_1):
    """
        Student try to submit assignment without teacher id.
    """
    content = 'ABCD TESTPOST'

    response = api_client.post(
        reverse('students-assignments'),
        data=json.dumps({
            'content': content,
            'state': 'SUBMITTED'
        }),
        HTTP_X_Principal=student_1,
        content_type='application/json'
    )

    assert response.status_code == 400
    error = response.json()

    assert error['non_field_errors'] == ['Teacher ID has to be sent to set state to SUBMITTED']

@pytest.mark.django_db()
def test_submit_assignment_without_teacher_student_1(api_client, student_1):
    response = api_client.patch(
        reverse('students-assignments'),
        data=json.dumps({
            'id': 2,
            'state': 'SUBMITTED'
        }),
        HTTP_X_Principal=student_1,
        content_type='application/json'
    )

    assert response.status_code == 400
    error = response.json()

    assert error['non_field_errors'] == ['Teacher ID has to be sent to set state to SUBMITTED']


@pytest.mark.django_db()
def test_set_grade_assignment_student_1(api_client, student_1):
    """
        Student try to set grade of assignment.
    """

    response = api_client.patch(
        reverse('students-assignments'),
        data=json.dumps({
            'id': 2,
            'grade': 'A',
            "teacher_id": 1
        }),
        HTTP_X_Principal=student_1,
        content_type='application/json'
    )

    assert response.status_code == 400
    error = response.json()

    assert error['non_field_errors'] == ['Student cannot set grade for assignment']

@pytest.mark.django_db()
def test_set_state_graded_assignment_student_1(api_client, student_1):
    """
        Test student try to set his assignment graded.
    """

    response = api_client.patch(
        reverse('students-assignments'),
        data=json.dumps({
            'id': 2,
            'state': 'GRADED',
        }),
        HTTP_X_Principal=student_1,
        content_type='application/json'
    )

    assert response.status_code == 400
    error = response.json()
    print(error)
    assert error['non_field_errors'] == ['Student cannot set state to GRADED']


@pytest.mark.django_db()
def test_submit_assignment_student_1(api_client, student_1):
    response = api_client.patch(
        reverse('students-assignments'),
        data=json.dumps({
            'id': 2,
            'state': 'SUBMITTED',
            'teacher_id': 1
        }),
        HTTP_X_Principal=student_1,
        content_type='application/json'
    )

    assert response.status_code == 200

    assignment = response.json()

    assert assignment['content'] is not None
    assert assignment['state'] == 'SUBMITTED'
    assert assignment['student'] == 1
    assert assignment['teacher'] == 1
    assert assignment['grade'] is None
    assert assignment['id'] is not None