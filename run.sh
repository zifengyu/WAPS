mailSend()
{
        mailContent="xxxx Web response time over 5 seconds"
        echo $mailContent
}
timeout()
{
        waitfor=3600000
        command=$*
        $command &
        commandpid=$!

        ( sleep $waitfor ; kill -9 $commandpid  > /dev/null 2>&1 && mailSend ) &

        watchdog=$!
        sleeppid=$PPID
        wait $commandpid > /dev/null 2>&1

        kill $sleeppid > /dev/null 2>&1
}

test123()
{
        python ping_jenkins.py
        python waps.py &
        sleep 9
        python waps.py &
        sleep 9
        python waps.py &
        sleep 9
        python waps.py &
        sleep 9
        python waps.py &
        sleep 4000
}

timeout test123