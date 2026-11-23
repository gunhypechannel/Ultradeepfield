set -x
mkdir -p /tmp/shots
adb install -r android/app/build/outputs/apk/debug/app-debug.apk
adb logcat -c
adb shell am start -n com.udf.ultradeepfield/.MainActivity
sleep 2; adb exec-out screencap -p > /tmp/shots/1-splash.png
sleep 40; adb exec-out screencap -p > /tmp/shots/2-loaded.png
adb shell input keyevent KEYCODE_BACK; sleep 3; adb exec-out screencap -p > /tmp/shots/3-after-back.png
adb shell dumpsys activity activities | grep -E "topResumed" > /tmp/shots/after-back.txt
adb logcat -d > /tmp/shots/logcat-online.txt
# offline, with the page already cached (a returning player)
adb shell am force-stop com.udf.ultradeepfield
adb shell cmd connectivity airplane-mode enable; sleep 4
adb logcat -c
adb shell am start -n com.udf.ultradeepfield/.MainActivity; sleep 20
adb exec-out screencap -p > /tmp/shots/4-offline-cached.png
# offline, first launch (nothing cached)
adb shell am force-stop com.udf.ultradeepfield; adb shell pm clear com.udf.ultradeepfield
adb shell am start -n com.udf.ultradeepfield/.MainActivity; sleep 20
adb exec-out screencap -p > /tmp/shots/5-offline-fresh.png
adb shell dumpsys activity activities | grep -E "topResumed" > /tmp/shots/offline-top.txt
adb logcat -d > /tmp/shots/logcat-offline.txt
# back online: tap Retry
adb shell cmd connectivity airplane-mode disable; sleep 8
adb shell uiautomator dump /sdcard/ui.xml >/dev/null 2>&1; adb shell cat /sdcard/ui.xml > /tmp/shots/offline-ui.xml
B=$(grep -o 'text="Retry"[^>]*bounds="\[[0-9]*,[0-9]*\]\[[0-9]*,[0-9]*\]"' /tmp/shots/offline-ui.xml | grep -o '\[[0-9]*,[0-9]*\]\[[0-9]*,[0-9]*\]' | tr -d '[]' | tr ',' ' ')
set -- $B; if [ -n "$1" ]; then adb shell input tap $(( ($1+$3)/2 )) $(( ($2+$4)/2 )); else adb shell input tap 540 1300; fi
sleep 30; adb exec-out screencap -p > /tmp/shots/6-after-retry.png
true
