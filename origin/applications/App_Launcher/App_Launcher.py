from origin.ui.app_launcher import app_launcher_ui
from origin.ui.utils.app_run_wrapper import execute_app


def run():
    execute_app(main_widget=app_launcher_ui.AppLauncherMainUI, widget_size=[350, 850])


if __name__ == "__main__":
    run()

