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
        # python ping_jenkins.py
        python waps.py &
        cp1=$!
        sleep 9
        python waps.py &
        cp2=$!
        sleep 9
        python waps.py &
        cp3=$!
        sleep 9
        python waps.py &
        cp4=$!
        sleep 9
        python waps.py &
        cp5=$!
        sleep 9
        python waps.py &
        cp6=$!
        sleep 8848
        kill -9 $cp1
        kill -9 $cp2
        kill -9 $cp3
        kill -9 $cp4
        kill -9 $cp5
        kill -9 $cp6
}

test123
