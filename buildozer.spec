[app]

title = MedScale-ORL
package.name = medscaleorl
package.domain = com.medscale

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json

version = 1.0.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.permissions = 

android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

android.release_artifact = aab

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_target = 13.0
ios.ios_add_arch = 

p4a.branch = develop
p4a.bootstrap = sdl2

log_level = 2

warn_on_root = 1

presplash.filename = %(source.dir)s/frontend/assets/presplash.png
icon.filename = %(source.dir)s/frontend/assets/icon.png

android.theme_background_color = "#1976D2"
android.statusbar_color = "#1565C0"
android.navbar_color = "#1565C0"
