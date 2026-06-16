from blocklog import BlocklogClient, can_manage_members, can_manage_team, is_team_owner


def main() -> None:
    client = BlocklogClient(
        base_url="http://127.0.0.1:8000/api/v1",
    )

    signup = client.auth.signup(
        username="jane",
        email="jane@example.com",
        password="ChangeMe123!",
        workspace_name="Acme Security",
    )

    client.set_access_token(signup.token)

    print("Created team:", signup.team.name)
    print("User owns team:", is_team_owner(signup.team, signup.user.user_id))

    if can_manage_team(signup.team, signup.user.user_id):
        updated = client.teams.update(
            signup.team.id,
            default_sla_minutes=30,
            description="Primary incident response team",
        )
        print("Updated SLA:", updated.default_sla_minutes)

    members = client.teams.members.list(signup.team.id)
    if members and can_manage_members(members[0]):
        print("Owner-level member is present")

    result = client.teams.notify_test(signup.team.id)
    print("Notification result:", result.results)


if __name__ == "__main__":
    main()
