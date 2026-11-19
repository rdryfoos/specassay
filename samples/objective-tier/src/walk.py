"""The walking side of the invented app: one function, one coverage mark."""


# @covers AC-WALK-01
def speak_turn(metres_ahead: int, turn: str) -> str | None:
    """Speak the next turn once, fifty metres out, and not again."""
    if metres_ahead > 50:
        return None
    return f"In {metres_ahead} metres, {turn}."
