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
	git-gamble --green -m "green" -- make check

red: # run red git gamble command 
	git-gamble --red -m "red" -- make check
