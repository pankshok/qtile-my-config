from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile.dgroups import simple_key_binder
from libqtile import layout, bar, widget

from backlight_control import BacklightControl

groups = [
    Group("Browser", matches=[Match(wm_class=["Google-chrome-stable", "Firefox"], role=["Browser"])]),
    Group("IDE"),
    Group("Misc"),
    Group("Media"),
    Group("Workspace"),
]

backlight = BacklightControl()

################################################################################
# Key bindings
################################################################################

mod = "mod4"

keys = [
    # Movements
    Key([mod], "Left", lazy.screen.prevgroup(skip_managed=True)),
    Key([mod], "Right", lazy.screen.nextgroup(skip_managed=True)),

    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()), #NO SUCH COMMAND
    Key([mod], "j", lazy.layout.up()),   #NO SUCH COMMAND

    Key([mod], "i", lazy.layout.grow()), #NO SUCH COMMAND
    Key([mod], "m", lazy.layout.shrink()), #NO SUCH COMMAND

    Key([mod], "n", lazy.layout.normalize()), 
    Key([mod], "o", lazy.layout.maximize()),

    Key([mod, "shift"], "space", lazy.layout.flip()),

    Key([mod], "Tab", lazy.layout.previous()),
    Key([mod, "shift"], "Tab", lazy.layout.next()),

    Key([mod], "f", lazy.window.toggle_floating()),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen()),

    Key([mod], "space", lazy.nextlayout()),

    Key([mod, "shift"], "v", lazy.layout.add()),
    Key([mod, "control"], "v", lazy.layout.remove()),

    # size
    Key([mod, "shift"], "Right", lazy.layout.increase_ratio()),
    Key([mod, "shift"], "Left", lazy.layout.decrease_ratio()),

    # move to
    Key([mod], "g", lazy.togroup()),

    Key([mod], "q", lazy.findwindow()),

    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),



    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Alsamixer volume controls
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("amixer sset Master 5%+")),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("amixer sset Master 5%-")),
    Key([], "XF86AudioMute",
        lazy.spawn("amixer sset Master toggle")),


    #Backlight controls
    Key([], "XF86MonBrightnessUp", lazy.function(lambda _: backlight.increase())),
    Key([], "XF86MonBrightnessDown", lazy.function(lambda _: backlight.decrease())),


    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

    Key([mod], "Return", lazy.spawn("uxterm")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.nextlayout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]

dgroups_key_binder = simple_key_binder(mod)

#    # mod1 + shift + letter of group = switch to & move focused window to group
#    keys.append(
#        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
#    )

layouts = [
    layout.Floating(),
    layout.Max(),
    layout.Stack(num_stacks=2)
]

widget_defaults = dict(
    font='Arial',
    fontsize=16,
    padding=3,
)



def separated_bar(widgets, separator, *args, **kwargs):
    '''returns bar.Bar object
       :widgets - list of widgets
       :separator - tuple, (sep_class, sep_defaults)
       :*args and **kwargs for bar instantiation
    '''
    separated = []

    for widget in widgets:
        separated.extend([widget, separator[0](**separator[1])])
    return bar.Bar(separated, *args, **kwargs)


bot_bar = separated_bar(
    [
       widget.CPUGraph(),
       widget.HDDBusyGraph(),
       widget.MemoryGraph(),
       widget.NetGraph(),
       widget.SwapGraph(),
       widget.Image(filename="~/1.png"),
       widget.Notify(),
       widget.BatteryIcon(),
       widget.KeyboardLayout(configured_keyboards=["us", "ru"]),
       widget.ThermalSensor(),
       widget.CurrentLayout(),
       widget.WindowName(),
       widget.Backlight(backlight_name="intel_backlight"),
    ],
    (widget.TextBox, dict(text=" ")),
    30,
)


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.TaskList(),
                widget.TextBox("DO COOL CONFIG  ", name="default"),
                widget.Systray(),
                widget.Sep(padding=5),
                widget.Volume(),
                widget.Sep(padding=5),
                widget.Battery(),
                widget.Sep(padding=5),
                widget.Clock(format='%I:%M %p'),
            ],
            30,
            background=["#000000", "#222222"],
        ),
        bottom=bot_bar,#bottom_bar,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
wmname = "qtile"
