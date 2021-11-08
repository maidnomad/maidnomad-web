import pytest


@pytest.fixture(autouse=True)
def set_mediaroot_as_test(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir
