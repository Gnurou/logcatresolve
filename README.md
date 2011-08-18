Android native stack trace resolver script
==========================================

This simple script acts as a filter to `adb logcat` and resolves addresses and
libraries in native stack traces by their corresponding symbol and originating
source file line. Simply put, it turns this:

    I/DEBUG   (   80):          #00  pc 00011070  /system/lib/libc.so
    ...
    I/DEBUG   (   80):          #12  pc 0001cdc6  /system/lib/libsurfaceflinger.so

into this:

    I/DEBUG   (   80):          #00  pthread_mutex_lock  bionic/libc/bionic/pthread.c:1022
    ...
    I/DEBUG   (   80):          #12  android::LayerBase::drawWithOpenGL(android::Region const&, android::Texture const&) const  frameworks/base/services/surfaceflinger/LayerBase.cpp:486

Usage
-----
Simply pipe the output of `adb logcat` into this script:

    $ adb logcat |logcatresolve.py

This script requires a couple of environment variables to be declared. They
are usually set by the Android configuration macros, e.g. `lunch` or
`choosecombo`, so if you set them according to the build you are using you
should be able to use it directly. The configuration must also be built.

How it works
------------
It simply calls `addr2line` on the right library file in your build directory
to lookup the symbol corresponding to the stack trace addresses and replaces
them with the output.

Contact
-------
Official repository for this script:
https://github.com/Gnurou/logcatresolve

Author:
Alexandre Courbot <acourbot@nvidia.com>
