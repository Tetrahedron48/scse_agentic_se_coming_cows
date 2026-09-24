import pytest

from navigation_logic import navigate


@pytest.mark.parametrize(
    ("front_blocked", "left_blocked", "right_blocked", "goal_direction", "expected"),
    [
        # Goal is FORWARD and safe
        (False, False, False, "FORWARD", "FORWARD"),
        (False, True, True, "FORWARD", "FORWARD"),

        # Goal is FORWARD but blocked; fall back in order: FRONT -> LEFT -> RIGHT
        (True, False, False, "FORWARD", "LEFT"),
        (True, True, False, "FORWARD", "RIGHT"),
        (True, False, True, "FORWARD", "LEFT"),
        (True, True, True, "FORWARD", "STOP"),

        # Goal is LEFT and safe
        (False, False, False, "LEFT", "LEFT"),
        (True, False, True, "LEFT", "LEFT"),

        # Goal is LEFT but blocked; fall back in order: FORWARD -> LEFT -> RIGHT
        (False, True, False, "LEFT", "FORWARD"),
        (True, True, False, "LEFT", "RIGHT"),
        (False, True, True, "LEFT", "FORWARD"),
        (True, True, True, "LEFT", "STOP"),

        # Goal is RIGHT and safe
        (False, False, False, "RIGHT", "RIGHT"),
        (True, True, False, "RIGHT", "RIGHT"),

        # Goal is RIGHT but blocked; fall back in order: FORWARD -> LEFT -> RIGHT
        (False, False, True, "RIGHT", "FORWARD"),
        (True, False, True, "RIGHT", "LEFT"),
        (False, True, True, "RIGHT", "FORWARD"),
        (True, True, True, "RIGHT", "STOP"),
    ],
)
def test_navigate_decisions(
    front_blocked: bool,
    left_blocked: bool,
    right_blocked: bool,
    goal_direction: str,
    expected: str,
) -> None:
    assert navigate(front_blocked, left_blocked, right_blocked, goal_direction) == expected


def test_goal_direction_priority_is_deterministic() -> None:
    # If the goal direction is safe, it must be chosen before considering fallbacks.
    assert navigate(True, False, False, "FORWARD") == "LEFT"
    assert navigate(True, True, False, "LEFT") == "RIGHT"
    assert navigate(True, True, False, "RIGHT") == "RIGHT"
    assert navigate(False, True, True, "RIGHT") == "FORWARD"
