import pytest


@pytest.mark.django_db
def test_ログインせずにアクセスするとログインページにリダイレクトされること(
    client,
):
    response = client.get("/__django_admin/", follow=True)
    assert response.template_name == ["admin/login.html"]


@pytest.mark.django_db
def test_ログインページに何も入れないでsubmitするとログインできないこと(form_client):
    response = form_client.get_and_submit(
        "/__django_admin/", selector="form#login-form", data={}
    )
    assert response.template_name == ["admin/login.html"]


@pytest.mark.django_db
def test_ログインページにID_PASSを入れてsubmitするとindexページが表示されること(
    form_client, superuser, superuser_password
):
    response = form_client.get_and_submit(
        "/__django_admin/",
        selector="form#login-form",
        data={"username": superuser.username, "password": superuser_password},
    )
    assert response.template_name == "admin/index.html"


@pytest.mark.django_db
def test_ログインして__django_admin_URLに直接アクセスするとindexページが表示されること(client_superuser_loggedin):
    response = client_superuser_loggedin.get("/__django_admin/", follow=True)

    assert response.template_name == "admin/index.html"
