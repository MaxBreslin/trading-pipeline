.PHONY: build install cppinstall test pytest cpptest integration clean clean-logs lint pylint cpplint format pyformat cppformat

RELEASE_TYPE = Release
PY_SRC = src/pysrc
CPP_SRC = src/cppsrc

build: cppinstall
	cd build && cmake .. \
		-DCMAKE_TOOLCHAIN_FILE=$(RELEASE_TYPE)/generators/conan_toolchain.cmake \
		-DCMAKE_BUILD_TYPE=$(RELEASE_TYPE) \
		-DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
		-G Ninja
	cd build && cmake --build .
	@cp -f build/*.so $(PY_SRC)

install:
	poetry install

cppinstall:
	conan install . --build=missing

test: install build
	@poetry run pytest $(PY_SRC)/test/unit
	@cd build && ./intern_tests

pytest: install build
	@poetry run pytest $(PY_SRC)/test/unit

cpptest: build
	@cd build && ./intern_tests

integration: install build
	@poetry run pytest $(PY_SRC)/test/integration

clean:
	@rm -rf build
	@rm -f $(PY_SRC)/*.so

clean-logs:
	@rm -f logs/*

lint: pylint cpplint

pylint:
	poetry run mypy $(PY_SRC)
	poetry run ruff check $(PY_SRC)
	poetry run ruff format --check $(PY_SRC)

cpplint: build
	find src -name '*.cpp' -o -name '*.hpp' | xargs clang-format --style=file --dry-run -Werror
	run-clang-tidy -j $(shell nproc) -p build

format: pyformat cppformat

pyformat:
	poetry run ruff format $(PY_SRC)
	poetry run ruff check --fix $(PY_SRC)

cppformat: build
	find $(CPP_SRC) -name '*.cpp' -o -name '*.hpp' | xargs clang-format --style=file -i
	run-clang-tidy -fix -j $(shell nproc) -p build
