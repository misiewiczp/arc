



while True:
    for cmd in enumerate(cmds):
        if cmd.is_ready():
	    cmd.run()
    time.sleep(0.1)

