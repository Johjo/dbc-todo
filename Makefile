check: type_check test_check# run all check

type_check: type_check-ty # run all type check

type_check-ty:
	uv run ty check --output-format concise

test_check: # run all test check
	uv run pytest

green: # run green git gamble command
	git-gamble --green -m "green" -- make check

red: # run red git gamble command 
	git-gamble --red -m "red" -- make check
