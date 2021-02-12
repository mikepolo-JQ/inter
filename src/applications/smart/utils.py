from pathlib import Path

from django.db.models import QuerySet

from applications.profile.models import Profile
from applications.smart.models import Match

DIR_SMART = Path(__file__).resolve().parent

DIR_SMART_STATIC = DIR_SMART / "static/smart"

DIR_WORDS = DIR_SMART_STATIC


def update_matches(profiles: QuerySet) -> int:
    before_count = Match.objects.all().count()

    for profile in profiles:
        profile.provide_help, profile.needed_help = filter_useless_words(
            profile.provide_help, profile.needed_help
        )
        profile.save()

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
        match = Match(
            provider_id=provider.id, needer_id=needer.id, reason=provider.provide_help
        )
        match.save()


with open(DIR_WORDS / "useless_words.txt", "r", encoding="utf-8") as file:
    useless_words = {line.strip() for line in file}


def filter_useless_words(*args) -> tuple:
    resp = ()
    for help_string in args:
        words_list = help_string.split(" ")
        words = " ".join([words for words in words_list if words not in useless_words])
        resp += (words,)
    return resp


def create_contacts() -> int:

    matches = Match.objects.all()
    k = 0
    #
    for i in range(len(matches) - 1):
        for j in range(i + 1, len(matches)):
            if not matches[i].match_with(matches[j]):
                continue

            profile = Profile.objects.get(id=matches[i].provider.pk)
            contact = Profile.objects.get(id=matches[j].provider.pk)
            if contact in profile.get_contact_list:
                continue

            profile.contacts.add(contact)
            k += 1

    return k
