#TODO Wrap all xbacklight arguments
#TODO Combine this control class with widget that will show current backlight value
#TODO Replase subprocess.call with qtile apropriate command
import subprocess

class BacklightControl(object):
    def __init__(self, 
            command_get="xbacklight -set",
            command_set="xbacklight -set {val}",
            default_backlight=60,
            step=10, max=100, min=10, parse_function=lambda s: int(s)):

        self._command_get = command_get
        self._command_set = command_set
        self._currentBacklight = default_backlight
        self._step = step
        self._max  = max
        self._min  = min
        self._parse = parse_function

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
        return self.parse(out)

    def setBacklight(self):
        subprocess.call(self._command_set.format(val=self._currentBacklight), shell=True)

    def increase(self):
        self._currentBacklight += self._step
        self._update()

    def decrease(self):
        self._currentBacklight -= self._step
        self._update()
