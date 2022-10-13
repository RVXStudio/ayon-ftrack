from pydantic import Field, validator

from openpype.settings import BaseSettingsModel, ensure_unique_names

ROLES_TITLE = "Roles for action"


class DictWithStrList(BaseSettingsModel):
    """Common model for Dictionary like object with list of strings as value.

    This model requires 'ensure_unique_names' validation.
    """

    _layout = "expanded"
    name: str
    value: list[str] = Field(default_factory=list)


class ApplicationLaunchStatuses(BaseSettingsModel):
    enabled: bool = True
    ignored_statuses: list[str] = Field(
        title="Do not change status if current status is",
    )
    status_change: list[DictWithStrList] = Field(
        title="Change task's status to <b>left side</b> if current task status is in list on <b>right side</b>.",
        default_factory=DictWithStrList,
    )

    @validator("status_change")
    def ensure_unique_names(cls, value):
        """Ensure name fields within the lists have unique names."""

        ensure_unique_names(value)
        return value


class FtrackDesktopAppHandlers(BaseSettingsModel):
    """Settings for event handlers running in ftrack service."""

    application_launch_statuses: ApplicationLaunchStatuses = Field(
        title="Application - Status change on launch",
        default_factory=ApplicationLaunchStatuses,
    )