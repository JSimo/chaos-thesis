#/usr/bin/env bash
_MINMIN=""
_MIN=""
_PREFIX="\U0001F525"

while getopts ":mn" opt; do
  case $opt in
     n)
      _MINMIN="TRUE"
      ;;
     m)
      _MIN="TRUE"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

function cprint() {
    printf "$_PREFIX $1\n\r"
}

# ------ Cleanup -------
# Cleanup any old instances of memcached.
function startMemcache() {
    cprint "Removing old memcaches instances."
    docker container rm --force $(docker container ls --filter name=memcache -q)

    # Create memcache containers and run tests
    cprint "Deploying two instances of memcache"
    docker run -p 11211:11211 -d --name memcached1 memcached:1.5.5
    docker run -p 11212:11211 -d --name memcached2 memcached:1.5.5
}

_short_date_time="$(date +%Y_%m_%d__%H_%M_%S)"
_output_dir="results/$_short_date_time"
mkdir -p "$_output_dir"
_xmem_file="$_output_dir/xmem.log"
_javam_file="$_output_dir/javam.log"
_spym_file="$_output_dir/spym.log"

touch "$_xmem_file" "$_javam_file" "$_spym_file"

# do stuff
cprint "Starting benchmarks"

function progressbar() {
    bar="##################################################"
    barlength=${#bar}
    n=$(($1*barlength/100))
    printf "\r$_PREFIX [%-${barlength}s (%d%%)] " "${bar:0:n}" "$1"
}

function runBenchmark() {
    cprint "java -jar $1 > $2"
    #cprint ""
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
       progressbar "$_progress"
       ps -p $_pid > /dev/null || break #exit loop if process is done.
       sleep 0.2
    done
    wait $_pid &> /dev/null # wait for benchmark process to finish.
    progressbar 100 #finished, so for prettyness set progress bar to 100
    trap - 9 #reset trap handler
    printf "\n\r"
}

# jar, output, number of lines in output max.
if [[ "$_MINMIN" == "TRUE" ]]; then
    # same a min but with less rounds per type so lesser accuracy.
    runBenchmark xmemcac/xmemcached-minmin.jar "$_xmem_file" 18
    runBenchmark spymemc/spymemcached-minmin.jar "$_spym_file" 18
    runBenchmark javamem/javamemcached-minmin.jar "$_javam_file" 18
elif  [[ "$_MIN" == "TRUE" ]]; then
    runBenchmark xmemcac/xmemcached-min.jar "$_xmem_file" 18
    runBenchmark spymemc/spymemcached-min.jar "$_spym_file" 18
    runBenchmark javamem/javamemcached-min.jar "$_javam_file" 18
else
    #run full tests (takes a *long* time)
    runBenchmark xmemcac/xmemcached.jar "$_xmem_file" 25
    runBenchmark spymemc/spymemcached.jar "$_spym_file" 25
    runBenchmark javamem/javamemcached.jar "$_javam_file" 20
fi

cprint "Finished benchmarking"
