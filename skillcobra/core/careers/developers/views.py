from skillcobra.core.views import AuthorizedHomeViewMixin


class DeveloperRecruitmentView(AuthorizedHomeViewMixin):
    template_name = "pages/careers/developer_recruitment.html"
