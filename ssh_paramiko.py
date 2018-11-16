import paramiko
import re


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.1.1', username='root', password='')
shell = ssh.invoke_shell()
stdin = shell.makefile('wb')
stdout = shell.makefile('r')
cmd='ps'
stdin.write(cmd + '\n')
finish = 'end of stdOUT buffer. finished with exit status'
echo_cmd = 'echo {} $?'.format(finish)
stdin.write(echo_cmd + '\n')
shin = stdin
stdin.flush()

shout = []
sherr = []
exit_status = 0
for line in stdout:
    if str(line).startswith(cmd) or str(line).startswith(echo_cmd):
        # up for now filled with shell junk from stdin
        shout = []
    elif str(line).startswith(finish):
        # our finish command ends with the exit status
        print line
        exit_status = int(str(line).rsplit('status')[1])
        if exit_status:
            # stderr is combined with stdout.
            # thus, swap sherr with shout in a case of failure.
            sherr = shout
            shout = []
        break
    else:
        # get rid of 'coloring and formatting' special characters
        shout.append(re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]').sub('', line).
                     replace('\b', '').replace('\r', ''))

# first and last lines of shout/sherr contain a prompt
if shout and echo_cmd in shout[-1]:
    shout.pop()
if shout and cmd in shout[0]:
    shout.pop(0)
if sherr and echo_cmd in sherr[-1]:
    sherr.pop()
if sherr and cmd in sherr[0]:
    sherr.pop(0)

print shin 
print ''.join(shout) 
print sherr





cmd='cd /proc; ls'
stdin.write(cmd + '\n')
finish = 'end of stdOUT buffer. finished with exit status'
echo_cmd = 'echo {} $?'.format(finish)
stdin.write(echo_cmd + '\n')
shin = stdin
stdin.flush()

shout = []
sherr = []
exit_status = 0
for line in stdout:
    if str(line).startswith(cmd) or str(line).startswith(echo_cmd):
        # up for now filled with shell junk from stdin
        shout = []
    elif str(line).startswith(finish):
        # our finish command ends with the exit status
        print line
        exit_status = int(str(line).rsplit('status')[1])
        if exit_status:
            # stderr is combined with stdout.
            # thus, swap sherr with shout in a case of failure.
            sherr = shout
            shout = []
        break
    else:
        # get rid of 'coloring and formatting' special characters
        shout.append(re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]').sub('', line).
                     replace('\b', '').replace('\r', ''))

# first and last lines of shout/sherr contain a prompt
if shout and echo_cmd in shout[-1]:
    shout.pop()
if shout and cmd in shout[0]:
    shout.pop(0)
if sherr and echo_cmd in sherr[-1]:
    sherr.pop()
if sherr and cmd in sherr[0]:
    sherr.pop(0)

print shin 
print ''.join(shout) 
print sherr
