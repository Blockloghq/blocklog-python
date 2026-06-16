from blocklog.models.teams import Team, TeamMember, TeamRole


def is_team_owner(team: Team, user_id: str) -> bool:
    return team.owner_user_id == user_id


def is_team_admin(member: TeamMember) -> bool:
    return member.role in (TeamRole.OWNER, TeamRole.ADMIN)


def can_manage_team(team: Team, user_id: str) -> bool:
    return is_team_owner(team, user_id)


def can_manage_members(member: TeamMember) -> bool:
    return is_team_admin(member)


def get_primary_team(teams: list[Team]) -> Team | None:
    return teams[0] if teams else None
