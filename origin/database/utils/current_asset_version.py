def current_asset_version(self, docs: list[dict]) -> dict | None:
    best = None

    if docs is not None:
        for doc in docs:
            if doc.get("status") not in {"CLIENT APPROVED", "WIP"}:
                continue
            if "date" not in doc or "time" not in doc:
                continue

            if best is None:
                best = doc
                continue

            if best["status"] != "CLIENT APPROVED" and doc["status"] == "CLIENT APPROVED":
                best = doc
                continue

            if doc["status"] == best["status"]:
                if (doc["date"], doc["time"]) > (best["date"], best["time"]):
                    best = doc

        return best
    else:
        return None