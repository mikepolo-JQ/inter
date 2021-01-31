from applications.smart.models import Contact
from applications.smart.models import Match
from project.settings import DIR_PROJECT


def key_sort(arg):
    return arg[0]


def searcher_matches(providers: list, needers: list) -> list:
    needers.sort(key=key_sort)
    save_needers = needers.copy()
    matches = []

    start = 0
    stop = len(needers) - 1

    for reason, pr_user in providers:

        while start <= stop:
            mid = (start + stop) // 2

            if reason == needers[mid][0]:
                match = (pr_user, needers[mid][1], reason)
                matches.append(match)
                needers.pop(mid)

                start = 0
                stop = len(needers) - 1
            elif reason < needers[mid][0]:
                stop = mid - 1
            else:
                start = mid + 1

        needers = save_needers.copy()
        start = 0
        stop = len(needers) - 1
    return matches


def start_filter(reason: list) -> list:
    with open(
        "src/applications/smart/static/smart/useless_words.txt", "r", encoding="utf-8"
    ) as file:
        useless_words = {line.strip() for line in file}

    for i in range(len(reason)):
        r = set(reason[i][0].split(" "))
        if useless_words.isdisjoint(r):
            continue
        r = r - useless_words

        reason[i][0] = " ".join(r)
    return reason


def create_contacts() -> int:
    matches = Match.objects.all()
    k = 0
    for i in range(len(matches) - 1):
        for j in range(i + 1, len(matches)):
            if matches[i] == matches[j]:
                if Contact.objects.filter(
                    first_match=matches[i], second_match=matches[j]
                ):
                    continue
                contact = Contact(first_match=matches[i], second_match=matches[j])
                contact.save()
                k += 1
    return k
