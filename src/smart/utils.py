from pathlib import Path
from typing import Optional
from typing import Union

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from profile.models import Profile
from profile.models import TemporaryProfile
from smart.models import Match

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


def get_active_profiles() -> set:
    profiles = Profile.objects.all()
    active_profiles = set()

    for profile in profiles:
        if not profile.provide_help or not profile.needed_help:
            continue
        active_profiles.add(profile)
        profile.active = True
        profile.save()

    return active_profiles


def create_matches(
    provider: Union[Profile, set], needer: Union[Profile, set], reason: str
):
    matches = Match.objects.filter(provider=provider, needer=needer)
    match = matches.first()
    if not matches:
        Match(provider=provider, needer=needer, reason=reason).save()
    elif match.reason != reason:
        match.reason += " | " + reason
        match.save()


def filter_useless_words(*args) -> tuple:
    result = ()
    with open(DIR_WORDS / "useless_words.txt", "r", encoding="utf-8") as file:
        useless_words = {line.strip() for line in file}

    for help_strings in args:
        help_strings = help_strings.split(" | ")
        new_string = ()

        for help_string in help_strings:
            words_list = help_string.split(" ")
            useful_words = " ".join(
                [word for word in words_list if word not in useless_words]
            )
            new_string += (useful_words,)

        new_help_string = " | ".join(new_string)
        result += (new_help_string,)

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
    editor_profile_help_strings(
        user_profile
    )  # update profiles( removing useless words )

    create_temporary_profiles(active_profiles)

    # get user help strings in list
    need_self_list = user_profile.needed_help.split(" | ")
    provide_self_list = user_profile.provide_help.split(" | ")

    providers = set()  # get providers set and create Matches ( user = needer )
    for needed_help in need_self_list:
        prds = TemporaryProfile.objects.filter(provide_help=needed_help)
        for temp_profile in prds:
            providers.add(temp_profile.profile)
            create_matches(
                provider=temp_profile.profile.user,
                needer=user_profile.user,
                reason=needed_help,
            )

    needers = set()  # get needers set and create Matches ( user = provider )
    for provide_help in provide_self_list:
        nds = TemporaryProfile.objects.filter(needed_help=provide_help)
        for temp_profile in nds:
            needers.add(temp_profile.profile)
            create_matches(
                provider=user_profile.user,
                needer=temp_profile.profile.user,
                reason=provide_help,
            )

    TemporaryProfile.objects.all().delete()

    for profile in needers:  # create contacts
        if profile not in providers:
            continue
        user_profile.contacts.add(profile)
        k += 1

    return k


def create_temporary_profiles(profiles) -> None:
    for profile in profiles:

        need_help_list = profile.needed_help.split(" | ")
        provide_help_list = profile.provide_help.split(" | ")

        for need_self_help in need_help_list:
            for provide_self_help in provide_help_list:
                TemporaryProfile(
                    profile=profile,
                    needed_help=need_self_help,
                    provide_help=provide_self_help,
                ).save()
                break
