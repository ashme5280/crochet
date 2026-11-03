def generate_sphere_pattern(initial_stitches: int, max_stitches: int) -> list:
    """
    Generates row-by-row crochet instructions for a sphere.

    Args:
        initial_stitches (int): Starting stitch count (e.g., 6 for a standard magic ring).
        max_stitches (int): The widest circumference stitch count (e.g., 24 or 30).
    """
    instructions = []
    current_round = 1
    current_stitches = initial_stitches

    # 1. Foundation Round
    instructions.append(f"Rnd {current_round}: Start {initial_stitches} sc in a Magic Ring. ({current_stitches} sts)")

    # 2. Increase Phase: Incrementally increase until reaching max_stitches
    # Each standard increase round adds 'initial_stitches' per round (e.g., +6 per round)
    increment = initial_stitches
    step_count = 1

    while current_stitches < max_stitches:
        current_round += 1
        current_stitches += increment

        # Calculate the math formula for the increase pattern
        # e.g., reaching 18 from 12 means [sc in next 1 st, inc] x 6
        sc_count = step_count
        instructions.append(f"Rnd {current_round}: [sc in next {sc_count} st(s), inc] x {increment}. ({current_stitches} sts)")
        step_count += 1

    # 3. Even Phase (Cylindrical belly of the sphere)
    # A symmetric sphere usually has a few even rounds equal to the number of increase rounds
    even_rounds = step_count - 1
    for _ in range(even_rounds):
        current_round += 1
        instructions.append(f"Rnd {current_round}: sc in each st around. ({current_stitches} sts)")

    # 4. Decrease Phase: Mirror the increase phase down to the initial stitch count
    step_count -= 1
    while current_stitches > initial_stitches:
        sc_count = step_count
        current_round += 1
        current_stitches -= increment

        instructions.append(f"Rnd {current_round}: [sc in next {sc_count} st(s), dec] x {increment}. ({current_stitches} sts)")
        step_count -= 1

    return instructions


# --- Example Test Run ---
if __name__ == "__main__":
    print("Generating Sphere Pattern (Start: 6 sts, Max: 24 sts):")
    pattern = generate_sphere_pattern(initial_stitches=6, max_stitches=24)
    for step in pattern:
        print(step)
