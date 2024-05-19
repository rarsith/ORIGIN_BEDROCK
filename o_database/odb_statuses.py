from dataclasses import dataclass, field


@dataclass
class DbTaskStatuses:
    wip: dict = "WIP"
    init: dict = "READY TO START"
    in_progress: str = "IN PROGRESS"
    completed: str = "COMPLETED"
    omitted: str = "OMITTED"
    on_hold: str = "ON HOLD"
    not_started: str = "NOT STARTED"

    def list_all(self):
        return list(self.__dict__.values())


@dataclass
class DbVersionStatuses:
    wip: str = "WIP"
    in_progress: str = "IN PROGRESS"
    pending_rev: str = "PENDING REVIEW"
    tweak: str = "TWEAK"
    ignore: str = "IGNORE"
    rejected: str = "REJECTED"
    approved_internal: str = "INTERNAL APPROVED"
    approved_client: str = "CLIENT APPROVED"
    ready_to_deliver: str = "READY TO DELIVER"
    approved_temp: str = "TEMP APPROVED"

    def list_all(self):
        return list(self.__dict__.values())



if __name__ == "__main__":
    cc = DbTaskStatuses()
    print (str(cc.list_all()))