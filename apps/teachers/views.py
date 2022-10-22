from django.shortcuts import render

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.teachers.serializers import TeacherAssignmentSerializer
from apps.students.models import Assignment

from apps.teachers.models import Teacher


class TeacherAssignmentsView(ListAPIView):
    serializer_class = TeacherAssignmentSerializer

    # List all assignments submitted to this teacher
    def get(self, request, *args, **kwargs):
        assignments = Assignment.objects.filter(teacher__user=request.user)
        
        return Response(
            data=self.serializer_class(assignments, many=True).data,
            status=status.HTTP_200_OK
        )

    # Grade an assignment
    def patch(self, request, *args, **kwargs):
        assignment_id = request.data.get('id')

        if 'student' in request.data: 
            return Response(
                data={"non_field_errors": ["Teacher cannot change the student who submitted the assignment"]},
                status=status.HTTP_400_BAD_REQUEST
            )

        if 'content' in request.data:
            return Response(
                data={"non_field_errors": ["Teacher cannot change the content of the assignment"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            assignment = Assignment.objects.get(teacher__user=request.user, id=assignment_id)

            if assignment.grade != None: 
                return Response(
                    data={"non_field_errors": ["GRADED assignments cannot be graded again"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if assignment.state != "SUBMITTED": 
                return Response(
                    data={"non_field_errors": ["SUBMITTED assignments can only be graded"]},
                    status=status.HTTP_400_BAD_REQUEST
                )


        except Assignment.DoesNotExist:
            return Response(
                data={'non_field_errors': ['Teacher cannot grade for other teacher''s assignment']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.serializer_class(assignment, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )