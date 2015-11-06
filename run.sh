mailSend()
{
        mailContent="xxxx Web response time over 5 seconds"
        echo $mailContent
}
timeout()
{
        waitfor=600
        command=$*
        $command &
        commandpid=$!

        ( sleep $waitfor ; kill -9 $commandpid  > /dev/null 2>&1 && mailSend ) &

        watchdog=$!
        sleeppid=$PPID
        wait $commandpid > /dev/null 2>&1

        kill $sleeppid > /dev/null 2>&1
}

#测试的函数

test123()
{
        python waps.py &
        python waps.py &
        python waps.py
}

timeout test123