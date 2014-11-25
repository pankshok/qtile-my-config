#TODO Wrap all xbacklight arguments
#TODO Combine this control class with widget that will show current backlight value
#TODO Replase subprocess.call with qtile apropriate command
import subprocess

class BacklightControl(object):
    def __init__(self):
        self._command_get = "xbacklight -get"
        self._command_set = "xbacklight -set {val}"

        self._currentBacklight = 60
        self._step = 10
        self._max  = 100
        self._min  = 10
        self.setBacklight()

    def _update(self):
        if self._currentBacklight > self._max:
            self._currentBacklight = self._max
        elif self._currentBacklight < self._min:
            self._currentBacklight = self._min
        self.setBacklight()

    def getCurrentBacklight(self):
        p = subprocess.Popen(self._command_get, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, _ = p.communicate()
        return int(out)

    def setBacklight(self):
        subprocess.call(self._command_set.format(val=self._currentBacklight), shell=True)

    def increase(self):
        self._currentBacklight += self._step
        self._update()

    def decrease(self):
        self._currentBacklight -= self._step
        self._update()
