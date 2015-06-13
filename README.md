# cloudwatchplugin #
A plugin that connects to Amazon's CloudWatch for [Slack's Real-time bot for Python](https://github.com/slackhq/python-rtmbot) (rtmbot)

## Usage ##
Copy or symlink the [cloudwatch folder](cloudwatch) to the plugins folder of *rtmbot*. You will need to clone the *rtmbot* repo to be able to use this plugin.

This plugin relies on [boto](http://boto.readthedocs.org/en/latest/) to connect to Amazon. You'll need to set it up with your amazon AWS credentials, and there's a how-to on how to do that in boto's documentation.

You can ask the bot running this plugin about the current state of all configured alarms, and the bot will check the state of all alarms and send a message in Slack if an alarm is something other than OK.

### Commands ###
Currently the plugin supports one command: `get alarms` which will list all configured alarms and their current state. Here's an example with a bot named nejlika and five alarms set up on CloudWatch:

>me [9:53 PM] 
>@nejlika: get alarms

>nejlika BOT [9:53 PM] 
>DBService-dbserver-MySQLStatus: *OK*
>server-CPU_Utilization-Critical: *OK*
>server-StatusCheck-Failure: *OK*
>other_server-CPU_Utilization: *OK*
>other_server-CPU_Utilization-Critical: *OK*

### Configuration ###
Configuration is possible through *rtmbot's* configuration file `rtmbot.conf`. There's currently three things that's configurable in this plugin:

* `testing_channel`: A channel where the plugin can be more verbose without bothering normal users.
* `alarm_channel`: The channel where the plugin should send a message whenever it discoveres a triggered alarm
* `alarm_check_interval`: The time, in seconds, between alarm state checks

Here's an example configuration, without the rest of the settings from rtmbot.conf: `cloudwatch: {bots_channel: D12345678, alarm_channel: D12345678, alarm_check_interval: 60}`