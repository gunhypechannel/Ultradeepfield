set -x
mkdir -p /tmp/shots
adb install -r android/app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n com.udf.ultradeepfield/.MainActivity
sleep 2; adb exec-out screencap -p > /tmp/shots/1-splash.png
sleep 40; adb exec-out screencap -p > /tmp/shots/2-loaded.png
sleep 30; adb exec-out screencap -p > /tmp/shots/3-later.png
adb logcat -d | grep -iE "chromium|udf|AndroidRuntime|FATAL" | tail -150 > /tmp/shots/logcat.txt
adb shell input keyevent KEYCODE_BACK; sleep 3; adb exec-out screencap -p > /tmp/shots/4-after-back.png
adb shell dumpsys activity activities | grep -E "mResumedActivity|topResumed" > /tmp/shots/after-back.txt
adb shell am force-stop com.udf.ultradeepfield
adb shell pm clear com.udf.ultradeepfield
adb shell svc wifi disable; adb shell svc data disable; sleep 3
adb shell am start -n com.udf.ultradeepfield/.MainActivity; sleep 12
adb exec-out screencap -p > /tmp/shots/5-offline.png
adb shell svc wifi enable; adb shell svc data enable; sleep 8
adb shell input tap 540 1400; sleep 1
adb shell uiautomator dump /sdcard/ui.xml >/dev/null 2>&1; adb shell cat /sdcard/ui.xml > /tmp/shots/offline-ui.xml
true
