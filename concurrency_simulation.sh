#!/usr/bin/env bash

print_help() {
	cat <<EOF
Usage: $(basename "$0") -t <integer> -- [options...]

Options:
  -t <integer>    Specify number of concurrent calls to databse CLI (required)
  --              Separator before database CLI options
  --versbose      Don't suppress output from database CLI
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
verbose=0

while [[ $# -gt 0 ]]; do
	case $1 in
	--help)
		print_help
		;;
	--verbose)
		verbose=1
		shift
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

for i in $(seq 1 "${t_value}"); do
	(
		echo "[${BASHPID}] Starting concurrent call ${i}"

		if [[ ${verbose} -eq 1 ]]; then
			python -m sjsu_cmpe180b_f25.main "${rest_args[@]}"
			exit_status=$?
		else
			python -m sjsu_cmpe180b_f25.main "${rest_args[@]}" >/dev/null 2>&1
			exit_status=$?
		fi

		echo "[${BASHPID}] Completed concurrent call ${i} with exit status ${exit_status}"
		if [[ ${exit_status} -eq 0 ]]; then
			echo -e "[${BASHPID}][\e[32mSUCCEEDED\e[0m]"
		else
			echo -e "[${BASHPID}][\e[31mFAILED\e[0m]"
		fi
	) &
done

wait
echo "All concurrent calls completed."
