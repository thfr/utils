# Pacfilediff

`pacfilediff` shows changes to packaged file.

```bash
$ pacfilediff /etc/pulse/daemon.conf
```

produces (in my case)

```diff
--- /tmp/etc/pulse/daemon.conf	2017-09-19 09:42:03.000000000 +0200
+++ /etc/pulse/daemon.conf	2018-03-11 17:34:01.241075880 +0100
@@ -50,7 +50,7 @@
 ; log-time = no
 ; log-backtrace = 0

-; resample-method = speex-float-1
+resample-method = speex-float-3
 ; avoid-resampling = false
 ; enable-remixing = yes
 ; remixing-use-all-sink-channels = yes
@@ -78,6 +78,7 @@

 ; default-sample-format = s16le
 ; default-sample-rate = 44100
+default-sample-rate = 96000
 ; alternate-sample-rate = 48000
 ; default-sample-channels = 2
 ; default-channel-map = front-left,front-right
```
