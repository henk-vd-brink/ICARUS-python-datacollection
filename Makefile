build_and_run:
	. ./scripts/build_and_run.sh

build_and_push:
	. ./scripts/build_and_push.sh

test_build:
	docker-compose -f docker-compose.ci.build.yaml build

test_unit: test_build
	docker-compose -f docker-compose.test.yaml run --entrypoint=pytest icarus-webserver /home/docker_user/tests/unit

test_integration: test_build
	docker-compose -f docker-compose.test.yaml run --entrypoint=pytest icarus-webserver /home/docker_user/tests/integration

black:
	python3 -m black icarus-webserver

