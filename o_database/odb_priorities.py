from dataclasses import dataclass


@dataclass
class DbPriorities:
    low: str = "LOW"
    normal: str = "NORMAL"
    medium: str = "MEDIUM"
    high: str = "HIGH"
    critical: str = "CRITICAL"

    def list_all(self):
        return list(self.__dict__.values())


if __name__ == "__main__":
    cc = DbPriorities()
    print (str(cc.list_all()))