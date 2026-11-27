from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class TeacherRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not hasattr(request.user, "teacher_profile"):
            return redirect("education:edit_teacher_profile")

        return super().dispatch(request, *args, **kwargs)


class StudentRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not hasattr(request.user, "student_profile"):
            return redirect("education:edit_student_profile")

        return super().dispatch(request, *args, **kwargs)


# The end.
