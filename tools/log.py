import sys

class Log():

    nb_tab = 0
    muted = False

    @staticmethod
    def output(text):
        if not Log.muted:
            print(Log.nb_tab * "\t" + text)

    @staticmethod
    def input(text):
        return input(Log.nb_tab * "\t" + text)

    @staticmethod
    def nl(n = 1):
        if not Log.muted:
            sys.stdout.write("\n" * n)

    @staticmethod
    def tab(n = 1):
        Log.nb_tab += n

    @staticmethod
    def untab(n = 1):
        if n > Log.nb_tab:
            Log.nb_tab = 0
        else:
            Log.nb_tab -= n

    @staticmethod
    def mute():
        Log.muted = True

    @staticmethod
    def unmute():
        Log.muted = False
