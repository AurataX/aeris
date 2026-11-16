from statistics import correlation


def pearson(pairs: list[tuple[float | None, float | None]]):
    """Pearson r over rows where both values exist. None when there is too little data to say."""
    clean = [(x, y) for x, y in pairs if x is not None and y is not None]
    if len(clean) < 10 or len({x for x, _ in clean}) < 2 or len({y for _, y in clean}) < 2:
        return None
    return round(correlation([x for x, _ in clean], [y for _, y in clean]), 3)
