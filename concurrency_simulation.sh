#!/usr/bin/env bash

print_help() {
	cat <<EOF
Usage: $(basename "$0") -t <integer> -- [options...]

Options:
  -t <integer>    Specify number of concurrent calls to databse CLI (required)
  --              Separator before database CLI options
  --help          Show this help message

Example:
  $(basename "$0") -t 6 -- --pay-fine 7

EOF
	exit 0
}

if [[ $# -eq 0 ]]; then
	print_help
fi

t_value=""
rest_args=()

while [[ $# -gt 0 ]]; do
	case $1 in
	--help)
		print_help
		;;
	-t)
		t_value="$2"
		shift 2
		;;
	--)
		shift
		rest_args=("$@")
		break
		;;
	*)
		echo "Error: Unknown option $1"
		echo "Use --help for usage information"
		exit 1
		;;
	esac
done

if [[ -z "${t_value}" ]]; then
	echo "Error: -t <integer> is required"
	echo "Use --help for usage information"
	exit 1
fi

echo "t_value: ${t_value}"
echo "rest_args:" "${rest_args[@]}"
