# -*- mode: python ; coding: utf-8 -*-
# Swaraj.spec - PyInstaller configuration

import os
import sys

block_cipher = None

a = Analysis(
    ['app/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('assets/branding/*', 'assets/branding'),
        ('config/*', 'config'),
        ('*.py', '.'),
    ],
    hiddenimports=[
        'config.settings',
        'core.logger',
        'core.memory',
        'core.pipeline',
        'core.router',
        'core.sound',
        'core.wake_word_local',
        'core.learning',
        'core.camera',
        'core.semantic_memory',
        'core.email_calendar',
        'core.wake_word_train',
        'commands.app_control',
        'commands.media_control',
        'commands.productivity',
        'commands.system_control',
        'commands.web_search',
        'ui.animations',
        'ui.compact.widget',
        'ui.expanded.window',
        'ui.settings.window',
        'ui.tray.system_tray',
        'services.startup.startup_service',
        'services.windows.power_handler',
        'identity',
        'ai_brain',
        'listener',
        'speaker',
        'wake_word',
        'task_automation',
        'weather',
        'reminders',
        'system_monitor',
        'music_control',
        'pyttsx3',
        'speech_recognition',
        'pyaudio',
        'pystray',
        'PIL',
        'psutil',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Swaraj',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/branding/rajmudra_tray.png',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Swaraj',
)
