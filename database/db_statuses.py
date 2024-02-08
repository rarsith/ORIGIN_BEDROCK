class DbStatuses:
    wip: str = "WIP"
    init: str = "INIT"
    in_progress: str = "IN PROGRESS"
    pending_rev: str = "PENDING-REVIEW"
    tweak: str = "TWEAK"
    approved_internal: str = "APPROVED_INT"
    approved_client: str = "APPROVED_CLIENT"
    approved_temp: str = "APPROVED_TEMP"
    approved_tech: str = "APPROVED_TECH"

    def list_all(self):
        list_all_statuses = [self.wip,
                             self.init,
                             self.in_progress,
                             self.pending_rev,
                             self.tweak,
                             self.approved_internal,
                             self.approved_client,
                             self.approved_temp,
                             self.approved_tech]
        return list_all_statuses

class DbPubSlotsMethods:
    SLOTS_METHODS = {'m1': 'sf_csh',
                     'm2': 'mf_csh',
                     'm3': 'sf_geo',
                     'm4': 'geo_bake',
                     'm5': 'geo_sim',
                     'm6': 'scn_exp',
                     'm7': 'img_exp',
                     'm8': 'anm_crv',
                     'm9': 'scatter',
                     'm10': 'p_exp',
                     'm11': 'assign_exp',
                     'm12': 'cfg_scn_exp',
                     'm13': 'cfg_exp'}

if __name__ == "__main__":
    cc = DbStatuses()
    print (str(cc.list_all()))