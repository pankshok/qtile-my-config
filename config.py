from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget

from libqtile.dgroups import simple_key_binder


groups = [
    Group("Browser", matches=[Match(wm_class=["Google-chrome-stable", "Firefox"], role=["Browser"])]),
    Group("IDE"),
    Group("Misc"),
    Group("Media"),
    Group("Workspace"),
]

def getIndex(groupName):
    for i in xrange(len(groups)):
        if groups[i].name == groupName:
            return i

def toPreviousGroup(qtile):
    i = getIndex(qtile.currentGroup.name)
    qtile.currentWindow.togroup(groups[(i-1) % len(groups)])

def toNextGroup(qtile):
    i = getIndex(qtile.currentGroup.name)
    qtile.currentWindow.togroup(groups[(i+1) % len(groups)])


mod = "mod4"

keys = [
    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),

    # Move windows up or down in current stack
    Key(
        [mod, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.shuffle_up()
    ),

    # Switch window focus to other pane(s) of stack
    Key(
        [mod], "space",
        lazy.layout.next()
    ),

    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("amixer sset Master 5%+")),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("amixer sset Master 5%-")),
    Key([], "XF86AudioMute",
        lazy.spawn("amixer sset Master toggle")),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key([mod], "Return", lazy.spawn("uxterm")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.nextlayout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]


keys.append(Key([mod], "Left", lazy.group.prevgroup()))
keys.append(Key([mod], "Right", lazy.group.nextgroup()))
keys.append(Key(["mod1", "shift"], "Left", lazy.function(toPreviousGroup)))
keys.append(Key(["mod1", "shift"], "Right", lazy.function(toNextGroup)))

#for i in group:
#    # mod1 + letter of group = switch to group
#    keys.append(
#        Key([mod], i.name, lazy.group[i.name].toscreen())
#    )
#
#    # mod1 + shift + letter of group = switch to & move focused window to group
#    keys.append(
#        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
#    )

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=3)
]

widget_defaults = dict(
    font='Arial',
    fontsize=16,
    padding=3,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.TextBox("dassdsfault config", name="default"),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            30,
            background=["#000000", "#222222"],
        ),
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

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
wmname = "qtile"
