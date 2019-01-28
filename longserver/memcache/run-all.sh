#/usr/bin/env bash
# ------ Cleanup -------
# Cleanup any old instances of memcached.
function startMemcache() {
    echo "Removing old memcaches instances."
    docker container rm --force $(docker container ls --filter name=memcache -q)

    # Create memcache containers and run tests
    echo "Deploying two instances of memcache"
    docker run -p 11211:11211 -d --name memcached1 memcached:1.5.5
    docker run -p 11212:11211 -d --name memcached2 memcached:1.5.5
}

echo "Setup"
_short_date_time="$(date +%Y_%m_%d__%H_%M_%S)"
_output_dir="results/$_short_date_time"
mkdir -p "$_output_dir"
_xmem_file="$_output_dir/xmem.log"
_javam_file="$_output_dir/javam.log"
_spym_file="$_output_dir/spym.log"

touch "$_xmem_file" "$_javam_file" "$_spym_file"

# do stuff
echo "Starting benchmarks"

function progressbar() {
    bar="##################################################"
    barlength=${#bar}
    n=$(($1*barlength/100))
    printf "\r[%-${barlength}s (%d%%)] " "${bar:0:n}" "$1"
}


function runBenchmark() {
    echo "Running benchmark jar $1 outputting to $2"
    echo ""
    _jar="$1"
    _output_file="$2"
    DONE_NR_OF_LINES="$3"
    startMemcache &> /dev/null # start/restart the memcacheinstances
    sleep 30s # wait for memcache to start

    # start the benchmark jar in the background
    java -jar "$_jar" &> "$_output_file" &
    _pid=$!
    trap 'kill -9 $_pid' EXIT
    _lines=0
    while [  $_lines -lt $DONE_NR_OF_LINES ]; do
        _lines=`cat $_output_file | grep "threads" | wc -l`
        _progress=$(($_lines * 100 / $DONE_NR_OF_LINES))
       #echo "progress $_progress lines $_lines done $DONE_NR_OF_LINES"
       progressbar "$_progress"
       sleep 1
    done
    wait $_pid # wait for benchmark process to finish.
}

# jar, output, number of lines in output max.
runBenchmark xmemcac/xmemcached.jar "$_xmem_file" 25
runBenchmark spymemc/spymemcached.jar "$_spym_file" 25
runBenchmark javamem/javamemcached.jar "$_javam_file" 20



