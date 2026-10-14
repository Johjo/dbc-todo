check: check-type check-lint check-test # run all check

check-type: check-type-ty check-type-mypy # run all type check

check-type-ty:
	uv run ty check --output-format concise

check-type-mypy:
	uv run mypy .

check-lint:
	uv run ruff check .


check-test: # run all test check
	uv run pytest -v

green: # run green git gamble command
	git-gamble --green -m "$(or $(MESSAGE),green)" -- make check

red: # run red git gamble command
	git-gamble --red -m "$(or $(MESSAGE),red)" -- make check

coverage:
	uv run pytest --cov --cov-branch --cov-report=term-missing:skip-covered