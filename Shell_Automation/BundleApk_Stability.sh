#!/system/bin/sh

function check_upgrade_env()
{
if [ "$upgrade_env" != "DEBUG" ]
then
  echo ${curTime} "系统升级环境不是DEBUG" >> ${usb_log_path}
  setprop persist.xgimi.upgrade.env DEBUG
  echo ${curTime} "设置系统升级环境为DEBUG并重启" >> ${usb_log_path}
  sleep 3
  input keyevent KPPOWER
  sleep 3
  input keyevent 22
  sleep 3
  input keyevent 23
else
  echo ${curTime} "系统升级环境已经是DEBUG" >> ${usb_log_path}
fi
}

#触发下载并等待开机下载完成
function wait_app_download()
{
  am startservice -a com.xgimi.INUI_APP_UPGRADE --ei flag 1 
  sleep 60 
  curTime=$(date "+%F%H%M%S")
  appupdate_flag=`getprop persist.xgimi.appupdate.flag`
  while [ "$appupdate_flag" != "1" ]
  do
  appupdate_flag=`getprop persist.xgimi.appupdate.flag`
  sleep 30
  done
}

#设备重启动作
function deivce_reboot_action()
{
  input keyevent 3
  sleep 5
  input keyevent KPPOWER
  sleep 3
  input keyevent 22
  sleep 3
  input keyevent 23
}

function check_inui_version()
{
    inui_version=`getprop persist.xgimi.inui.version`
    curTime=$(date "+%F%H%M%S")
if [ "$inui_verison" != "1.3.1.1u" ]
then
  echo ${curTime} "bundle apk upgrde failed" >> ${usb_log_path}
  echo ${curTime} "excute upgarade fail revcovery" >> ${usb_log_path}
  am broadcast -a com.xgimi.intent.action.FACTORY_RESET -f 0x01000000
elif [ "$inui_version" == "1.3.1.1u" ]
then
  echo "bundle apk upgrde success" >> ${usb_log_path}
  echo "excute upgarade succss revcovery" >> ${usb_log_path}
  am broadcast -a com.xgimi.intent.action.FACTORY_RESET -f 0x01000000
fi
}

#检测开机是否完成
key=`getprop sys.boot_completed`
echo "检查开机是否完成..." >> ${usb_log_path}
while [ "$key" != "1" ]
do
key=`getprop sys.boot_completed`
echo "开机检测完成，睡眠30秒..." >> ${usb_log_path}
sleep 30
done

usb_log_path=/mnt/usb/A8FE-96C5/log.txt
echo "日志记录路径 $usb_log_path"
upgrade_env=`getprop persist.xgimi.upgrade.env`
curTime=$(date "+%F%H%M%S")
check_upgrade_env

#分情况执行不同命令
appupdate_flag=`getprop persist.xgimi.appupdate.flag`
inui_version=`getprop persist.xgimi.inui.version`
case "$appupdate_flag" in
  "0") check_inui_version;;
  "1") deivce_reboot_action;;
  *) wait_app_download
deivce_reboot_action
;;
esac


