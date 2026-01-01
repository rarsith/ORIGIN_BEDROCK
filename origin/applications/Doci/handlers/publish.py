class ExportCharacter:
    def run(self, task, event):
        print(
            f"Exporting {task['name']} from {event['scene']}"
        )
        # subprocess -> mayapy here

HANDLERS = {
    "export_character": ExportCharacter()
}

def get_handler(task_type):
    return HANDLERS[task_type]