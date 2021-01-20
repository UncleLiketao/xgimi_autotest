function screencap()
{
sleep 10
input keyevent 120
curTime=$(date "+%F%H%M%S")
cp /sdcard/syslog/logcat.log /sdcard/Pictures/Log/${curTime}logcat.log
sleep 10
pm clear com.xgimi.home
}

key=`getprop sys.boot_completed`
while [ "$key" != "1" ]
do
key=`getprop sys.boot_completed`
sleep 1
done

sleep 10
screencap
sleep 60
rebootbin