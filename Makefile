test:
	pytest tests --cov=functions \
		--cov-report=term-missing \
		-m "not slow"
	@printf "\e[32;1mtest ok\e[m\n"

test-lf:
	pytest --lf tests -vv --maxfail 1
	@printf "\e[32;1mtest-lf ok\e[m\n"

fmt:
	black maidnomadweb tests
	isort maidnomadweb tests
	@printf "\e[32;1mfmt ok\e[m\n"

lint:
	black --check maidnomadweb tests
	isort --check-only maidnomadweb tests
	flake8 maidnomadweb tests
	mypy maidnomadweb tests
	@printf "\e[32;1mlint ok\e[m\n"

pip_dev:
	pip install -r requirements_dev.txt -c requirements.lock

pip_prod:
	pip install -r requirements.txt -c requirements.lock

runserver:
	python maidnomadweb/manage.py runserver

