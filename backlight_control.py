#TODO Combine this control class with widget that will show current backlight value
#TODO Replase subprocess.call with qtile apropriate command
import subprocess

class BacklightControl(object):
    '''Class for controlling backlight with xbacklight(optional) 
    with qtile window manager(optional too)

    1) Create instance
    2) Call increase and decrease functions

    Arguments:
    :command_get - command that executes to get current backlight value
    :command_set - command that executes to set new backlight value
                   MUST have {val}
    :default_backlight - sets on instantiantion
    :step - changes backlight by that value
    :min - minimal value for backlight (%)
    :max - maximal value for backlight (%)
    :parse_function - function for parsing result of command_get execution
                      MUST take string and return integer
    '''

    def __init__(self,
            command_get="xbacklight -get",
            command_set="xbacklight -set {val}",
            default_backlight=60,
            step=10,
            max=100,
            min=10,
            parse_function=lambda s: int(s)):

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
