class DbPriorities:
    low: str = "LOW"
    medium: str = "MEDIUM"
    high: str = "HIGH"

    def list_all(self):
        list_all_priorities = [self.low,
                               self.medium,
                               self.high,
                               ]

        return list_all_priorities


if __name__ == "__main__":
    cc = DbPriorities()
    print (str(cc.list_all()))