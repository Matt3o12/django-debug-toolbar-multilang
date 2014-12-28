# Django-debug-toolbar-multilang #
[![Build Status](https://travis-ci.org/Matt3o12/django-debug-toolbar-multilang.svg?branch=master)](https://travis-ci.org/Matt3o12/django-debug-toolbar-multilang)
[![Coverage Status](https://img.shields.io/coveralls/Matt3o12/django-debug-toolbar-multilang.svg)](https://coveralls.io/r/Matt3o12/django-debug-toolbar-multilang?branch=master)


Django-debug-toolbar-multilang aims to help you internationalize and localized Django apps. It adds a "Language" panel to the toolbar and shows you the current language as well as all available languages. It also lets you quickly change the language to the selected one.

# Screenshots #
![panel preview1](http://media.matt3o12.de/djdt-multilang/v1.0/panel-max.png)


## Install ##

The recommended way to install djdt-multilang is by using pip:

    pip install django-debug-toolbar-multilang


If you'd like to test an upcoming release, use instead:

    pip install -e git+https://github.com/Matt3o12/django-debug-toolbar-multilang#egg=django-debug-toolbar-multilang
    
Next, you will need to add djdt-multilang to add `debug_toolbar_multilang.panels.multilang.MultiLangPanel` to `DEBUG_TOOLBAR_PANELS` and `debug_toolbar_multilang` to `INSTALLED_APPS`:

    DEBUG_TOOLBAR_PANELS = [
        ...
        'debug_toolbar_multilang.panels.multilang.MultiLangPanel',
    ]
    
    INSTALLED_APPS = [
        ...
        'debug_toolbar_multilang'
    ]
    
If you haven't already set, `DEBUG_TOOLBAR_PANELS` make sure not to forget [the defaults](http://django-debug-toolbar.readthedocs.org/en/latest/configuration.html#debug-toolbar-panels):

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar_multilang.panels.multilang.MultiLangPanel',
    ]
    
You will also need to enable the [Locale middleware](https://docs.djangoproject.com/en/dev/ref/middleware/#module-django.middleware.locale).

