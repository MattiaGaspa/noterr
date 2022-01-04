from time import sleep
import os, _thread, argparse

class Notification:
    def __init__(self, file, title, message):
        self.file = file
        self.title = title
        self.message = message
        self.pipein, self.pipeout = os.pipe()

        _thread.start_new_thread(self.checkFile, ())
        self.waitForLog()

    def waitForLog(self):
        oldcontent = []
        while True:
            os.read(self.pipein, 32)
            with open(self.file, 'r') as f:
                content = f.readlines()
                tmp = content
                content = content[len(oldcontent):]
                oldcontent = tmp
            for _content in content:
                table = list(filter(None, _content.split(" "))) # Remove empty string
                date = " ".join(table[:3])
                time = table[2]
                code = ''
                hostname = table[3]
                prog = table[4].replace(":", "")
                user = table[5][:len(table[5])-1] # delete the last :
                notmsg = " ".join(table[6:]).replace("\n", "")
                t = self.title.replace("$$DATE$$", date).replace("$$TIME$$", time).replace("$$CODE$$", code).replace("$$HOST$$", hostname).replace("$$PROGRAM$$", prog).replace("$$USER$$", user).replace("$$MESSAGE$$", notmsg)
                msg = self.message.replace("$$DATE$$", date).replace("$$TIME$$", time).replace("$$CODE$$", code).replace("$$HOST$$", hostname).replace("$$PROGRAM$$", prog).replace("$$USER$$", user).replace("$$MESSAGE$$", notmsg)
                os.system("notify-send \"" + t + "\" \"" + msg + "\"")

    def checkFile(self):
        oldtime = os.stat(self.file).st_mtime
        while True:
            if oldtime != os.stat(self.file).st_mtime:
                os.write(self.pipeout, b"File changed")
                oldtime = os.stat(self.file).st_mtime
            else:
                sleep(1)

parser = argparse.ArgumentParser(description="Simple notification manager for error")
parser.add_argument("-f", "--file", metavar="FILE", nargs="?", default="/var/log/critical.log", help="Log file (DEFAULT: /var/log/critical.log)")
args = parser.parse_args()

title = "Report [$$TIME$$] $$CODE$$"
message = "<b>$$PROGRAM$$</b>: <i>$$MESSAGE$$</i>"

if __name__ == "__main__":
    Notification(args.file, title, message)
