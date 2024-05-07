class DbTaskStatuses:
    wip: str = "WIP"
    init: str = "READY TO START"
    in_progress: str = "IN PROGRESS"
    completed: str = "COMPLETED"
    omitted: str = "OMITTED"
    on_hold: str = "ON HOLD"

    def list_all(self):
        list_all_statuses = [self.wip,
                             self.init,
                             self.in_progress,
                             self.completed,
                             self.omitted,
                             self.on_hold,
                             ]

        return list_all_statuses

class DbVersionStatuses:
    wip: str = "WIP"
    in_progress: str = "IN PROGRESS"
    pending_rev: str = "PENDING-REVIEW"
    tweak: str = "TWEAK"
    ignore: str = "IGNORE"
    rejected: str = "REJECTED"
    approved_internal: str = "INTERNAL APPROVED"
    approved_client: str = "CLIENT APPROVED"
    ready_to_deliver: str = "READY TO DELIVER"
    approved_temp: str = "TEMP APPROVED"
    approved_tech: str = "TECH APPROVED"

    def list_all(self):
        list_all_statuses = [self.wip,
                             self.in_progress,
                             self.pending_rev,
                             self.tweak,
                             self.ignore,
                             self.rejected,
                             self.approved_internal,
                             self.approved_client,
                             self.ready_to_deliver,
                             self.approved_temp,
                             self.approved_tech,
                             ]

        return list_all_statuses


if __name__ == "__main__":
    cc = DbTaskStatuses()
    print (str(cc.list_all()))