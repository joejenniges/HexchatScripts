import hexchat
import subprocess
import os.path

__module_name__ = "ChatPipe"
__module_version__ = "1.0"
__module_description__ = "Use /chatpipe <file> to toggle all messages you send being piped through said program before going to your chat"

enabled = False
hooks = list()
filepath = ""

def chatpipe(word, word_eol, userdata):
	global enabled
	enabled = not enabled

	if enabled and len(args) == 1:
		if os.path.isfile(args[0]):
			filepath = args[0]
			print ("ChatPipe is now enabled")
		else:
			print("Invalid file")
			enabled = False
	else:
		print ("ChatPipe is now disabled")
	return hexchat.EAT_HEXCHAT

def send_message(word, word_eol, userdata):
	global enabled

	if not enabled:
		return hexchat.EAT_NONE

	message = word_eol[0]
	channel = hexchat.get_info('channel')

	output = subprocess.Popen("{} \"{}\"".format(filepath, message), stdout=subprocess.PIPE, shell=True).communicate()[0].decode('UTF-8')
	for line in output.split('\n'):
		hexchat.command("say {} {}".format(channel, line))

	return hexchat.EAT_ALL

def on_unload(userdata):
	global hooks
	for hook in hooks:
		if hook is not None:
			hexchat.unhook(hook)
	del hooks[:]
	print("ChatPipe unloaded")

hooks.append(hexchat.hook_command("chatpipe", chatpipe, "Command is /chatpipe <file>"))
hooks.append(hexchat.hook_command("", send_message, priority=hexchat.PRI_HIGHEST))
hexchat.hook_unload(on_unload)
print("ChatPipe loaded")