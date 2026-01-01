from origin.ui.asset_stack_manager_ui import asset_stack_manager_ui
from origin.ui.utils.app_run_wrapper import execute_app


def run():
    execute_app(main_widget=asset_stack_manager_ui.AssetStackManagerUI)

if __name__ == "__main__":
    run()