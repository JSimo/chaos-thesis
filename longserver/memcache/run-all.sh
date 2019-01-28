#/usr/bin/env bash
echo "setup"
_short_date_time="$(date +%Y_%m_%d__%H_%M_%S)"
_output_dir="results/$_short_date_time"
mkdir -p "$_output_dir"
_xmem_file="$_output_dir/xmem.log"
_javam_file="$_output_dir/javam.log"
_spym_file="$_output_dir/spym.log"

touch "$_xmem_file" "$_javam_file" "$_spym_file"

# do stuff
echo "Starting benchmarks"

function runBenchmark() {
    echo "$1 | $2"
    _jar="$1"
    _output_file="$2"
    java -jar "$_jar" > "$_output_file"
}

runBenchmark xmemcac/xmemcached.jar "$_xmem_file"
runBenchmark spymemc/spymemcached.jar "$_spym_file"
runBenchmark javamem/javamemcached.jar "$_javam_file"


