import hexchat

__module_name__ = "Send Multiple Channels"
__module_version__ = "1.0"
__module_description__ = "Use /msgchannels <[server:]channel1,channel2,etc> <msg> to send a message to all channels in the comma separated channel list."

hooks = list()

def msgchannels(word, word_eol, userdata):
    channels = word[1]
    channels = channels.split(",")

    for channel in channels:
        parts = channel.split(":")
        if len(parts) == 2:
            ctx = hexchat.find_context(server=parts[0], channel=parts[1])
            ctx.command("msg {} {}".format(parts[1], word_eol[2]))
        else:
            hexchat.command("msg {} {}".format(channel, word_eol[2]))

    return hexchat.EAT_ALL

def on_unload(userdata):
    global hooks
    for hook in hooks:
        if hook is not None:
            hexchat.unhook(hook)
    del hooks[:]
    print("Send Multiple Channels unloaded")

hooks.append(hexchat.hook_command("msgchannels", msgchannels, "Command is /msgchannels <[server:]channel_list> <msg>. Example: /msgchannels freenode:#python,Rizon#news Hello World!"))
hexchat.hook_unload(on_unload)
print("Send Multiple Channels v{} loaded".format(__module_version__))