import pexpect

child = pexpect.spawn('python my_cli.py')

print(child.expect()