EXIT_STATUS=0

echo "Running clippy..."
# Switch the clippy errors to warnings due to PYO3 bugs.
# cargo clippy --manifest-path ../mmr3/Cargo.toml -- -D warnings|| EXIT_STATUS=$?
cargo clippy --manifest-path ../mmr3/Cargo.toml || EXIT_STATUS=$?
echo "\n"

echo "Running flake8..."
flake8 ../tests|| EXIT_STATUS=$?
flake8 ../mmr3/python|| EXIT_STATUS=$?
echo "\n"

echo "Running mypy..."
mypy ../tests|| EXIT_STATUS=$?
mypy ../mmr3/python|| EXIT_STATUS=$?
echo "\n"

echo "Exit status code $EXIT_STATUS!" 
exit $EXIT_STATUS
