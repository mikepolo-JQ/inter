from pathlib import Path

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from applications.profile.models import Profile
from applications.smart.models import Match

DIR_SMART = Path(__file__).resolve().parent

DIR_SMART_STATIC = DIR_SMART / "static/smart"

DIR_WORDS = DIR_SMART_STATIC

User = get_user_model()


def update_matches() -> int:
    before_count = Match.objects.all().count()

    profiles = get_active_profiles()

    for profile in profiles:
        editor_profile_help_strings(profile)

    for profile in profiles:
        needers = Profile.objects.filter(needed_help=profile.provide_help)
        if needers:
            create_matches(profile, needers)

    return Match.objects.all().count() - before_count


def editor_profile_help_strings(profile: Profile) -> None:
    profile.provide_help, profile.needed_help = filter_useless_words(
        profile.provide_help, profile.needed_help
    )
    profile.save()


def get_active_profiles() -> list:
    profiles = Profile.objects.all()
    active_profiles = []

    for profile in profiles:
        if not profile.provide_help or not profile.needed_help:
            continue
        active_profiles.append(profile)
        profile.active = True
        profile.save()

    return active_profiles


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


def filter_useless_words(*args) -> tuple:
    result = ()
    with open(DIR_WORDS / "useless_words.txt", "r", encoding="utf-8") as file:
        useless_words = {line.strip() for line in file}

    for help_string in args:
        words_list = help_string.split(" ")
        useful_words = " ".join(
            [word for word in words_list if word not in useless_words]
        )
        result += (useful_words,)
    return result


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


def search_contacts_for(user_profile: Profile) -> int:
    k = 0
    active_profiles = get_active_profiles()
    if user_profile not in active_profiles:
        raise ValueError(
            "Your profile isn't active. Please fill help lines on your profile page."
        )
    editor_profile_help_strings(user_profile)

    needers = Profile.objects.filter(active=True, needed_help=user_profile.provide_help)
    providers = Profile.objects.filter(
        active=True, provide_help=user_profile.needed_help
    )

    for profile in needers:
        if profile not in providers:
            continue
        user_profile.contacts.add(profile)

        create_match_simple(
            provider=profile.user, needer=user_profile.user, reason=profile.provide_help
        )

        create_match_simple(
            provider=user_profile.user,
            needer=profile.user,
            reason=user_profile.provide_help,
        )

        k += 1

    return k


def create_match_simple(provider: User, needer: User, reason: str) -> None:
    match = Match(provider=provider, needer=needer, reason=reason)
    match.save()
