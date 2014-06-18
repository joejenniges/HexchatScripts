import hexchat
import subprocess

__module_name__ = "ChatBash"
__module_version__ = "1.0"
__module_description__ = "Use /chatbash to toggle all messages you send being piped to bash"

enabled = False
hooks = list()

def chatbash(word, word_eol, userdata):
	global enabled
	enabled = not enabled
	if enabled:
		print ("ChatBash is now enabled")
	else:
		print ("ChatBash is now disabled")
	return hexchat.EAT_HEXCHAT

def send_message(word, word_eol, userdata):
	global enabled

	if not enabled:
		return hexchat.EAT_NONE

	message = word_eol[0]
	print("> {}".format(message))

	output = subprocess.Popen(message, stdout=subprocess.PIPE, shell=True).communicate()[0].decode('UTF-8')
	for line in output.split('\n'):
		print(line)

	return hexchat.EAT_ALL

def on_unload(userdata):
	global hooks
	for hook in hooks:
		if hook is not None:
			hexchat.unhook(hook)
	del hooks[:]
	print("ChatBash unloaded")

hooks.append(hexchat.hook_command("chatbash", chatbash, "Command is /chatbash"))
hooks.append(hexchat.hook_command("", send_message, priority=hexchat.PRI_HIGHEST))
hexchat.hook_unload(on_unload)
print("ChatBash loaded")