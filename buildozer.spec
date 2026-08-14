[app]

# (str) Title of your application
title = Portfolio App

# (str) Package name
package.name = portfolio

# (str) Package domain (needed for android/ios packaging)
package.domain = org.godem

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Application requirements
requirements = python3,kivy==2.2.1,reportlab,pillow,requests

# (str) Application versioning (method 1)
version = 1.4

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

[android]

# (list) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (int) Android API to use
android.api = 31

# (int) Minimum API required
android.minapi = 21

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) python-for-android branch to use, defaults to stable
p4a.branch = stable

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

[iOS]
