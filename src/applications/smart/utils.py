from django.db.models import QuerySet

from applications.profile.models import Profile
from applications.smart.models import Contact
from applications.smart.models import Match


def update_matches(profiles: QuerySet) -> int:
    before_count = Match.objects.all().count()

    for profile in profiles:
        profile.provide_help, profile.needed_help = filter_useless_words(profile.provide_help, profile.needed_help)

    for profile in profiles:
        needers = Profile.objects.filter(needed_help=profile.provide_help)
        if needers:
            create_matches(profile, needers)

    return Match.objects.all().count() - before_count


def create_matches(provider: Profile, needers: QuerySet):
    for needer in needers:
        if Match.objects.filter(
                provider_id=provider.id, needer_id=needer.id, reason=provider.provide_help
        ):
            continue
        match = Match(provider_id=provider.id, needer_id=needer.id, reason=provider.provide_help)
        match.save()


def filter_useless_words(*args) -> tuple:
    with open(
        "src/applications/smart/static/smart/useless_words.txt", "r", encoding="utf-8"
    ) as file:
        useless_words = {line.strip() for line in file}

    resp = ()
    for help_string in args:
        words_list = help_string.split(" ")
        words = " ".join([words for words in words_list if words not in useless_words])
        resp += (words,)
    return resp


def create_contacts() -> int:
    matches = Match.objects.all()
    k = 0
    for i in range(len(matches) - 1):
        for j in range(i + 1, len(matches)):
            if not matches[i] == matches[j] or Contact.objects.filter(
                first_match=matches[i], second_match=matches[j]
            ):
                continue
            contact = Contact(first_match=matches[i], second_match=matches[j])
            contact.save()
            k += 1
    return k
