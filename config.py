from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile.dgroups import simple_key_binder
from libqtile import layout, bar, widget


groups = [
    Group("Browser", matches=[Match(wm_class=["Google-chrome-stable", "Firefox"], role=["Browser"])]),
    Group("IDE"),
    Group("Misc"),
    Group("Media", matches=[Match(wm_class=["Steam"])]),
    Group("Workspace"),
]

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
    Key([mod], "space", lazy.spawn("dmenu_run -fn 'Terminus:size=14' -nb '#000000' -nf '#fefefe'")),
]

dgroups_key_binder = simple_key_binder(mod)

layouts = [
    layout.Floating(),
    layout.Tile(ratio=0.35, borderwidth=1),
    layout.Max(),
    #layout.Stack(num_stacks=2),
    #layout.TreeTab(sections=['Work', 'Messaging', 'Docs', 'Util', 'Other']),
    # a layout for pidgin
    # layout.Slice('right', 256, name='pidgin', role='buddy_list',
    #     fallback=layout.Stack(stacks=2, border_width=1)),
]

widget_defaults = dict(
    font='Arial',
    fontsize=16,
    padding=3,
)

def separated_bar(separator, widgets, *args, **kwargs):
    '''returns bar.Bar object
       :separator - tuple, (sep_class, sep_defaults)
       :widgets - list of widgets
       :*args and **kwargs for bar instantiation
    '''
    separated = []

    for widget in widgets:
        separated.extend([widget, separator[0](**separator[1])])

    return bar.Bar(separated, *args, **kwargs)


bottom_bar = separated_bar(
    (widget.TextBox, dict(text=" ")),
    [
        widget.CPUGraph(),
        widget.HDDBusyGraph(),
        widget.MemoryGraph(),
        widget.NetGraph(),
        widget.SwapGraph(),
        widget.Notify(),
        widget.BatteryIcon(),
        widget.KeyboardLayout(configured_keyboards=["us", "ru"]),
        widget.ThermalSensor(),
        widget.CurrentLayout(),
        widget.WindowName(),
        widget.Backlight(backlight_name="intel_backlight"),
    ],
    30,
    background=["#222222", "#000000"],
)

top_bar = separated_bar(
    (widget.TextBox, dict(text=" ")),
    [
        widget.GroupBox(),
        widget.Prompt(),
        widget.TaskList(),
        widget.TextBox("DO COOL CONFIG", name="default"),
        widget.Systray(),
        widget.Volume(),
        widget.Battery(),
        widget.Clock(format='%H:%M'),
    ],
    30,
    background=["#000000", "#222222"],
)

screens = [
    Screen(
        top=top_bar,
        bottom=bottom_bar,
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
wmname = "LG3D"#"qtile"
