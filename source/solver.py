import logging

from ortools.sat.python import cp_model

from source.models import Matrix, PiecePart

logger = logging.getLogger(__name__)


def solve_from_matrix(matrix: Matrix, row_inputs: list[int], columns_inputs: list[int]) -> Matrix:
    return solve(
        grid_size=len(matrix),
        top_numbers=columns_inputs,
        side_numbers=row_inputs,
        black_squares=[(w, h) for w in range(len(matrix)) for h in range(len(matrix)) if matrix[h][w] == 1],
    )


def solve(
    grid_size: int, top_numbers: list[int], side_numbers: list[int], black_squares: list[tuple[int, int]]
) -> Matrix:
    model = cp_model.CpModel()

    # The (0, 0) position is at the top-left of the board
    width = grid_size
    height = grid_size

    # # Black squares (w, h)
    # black_squares = [(3, 0), (1, 1), (4, 3), (2, 4)]
    #
    # # Top numbers
    # top_numbers = [2, 5, 3, 5, 3, 6]
    #
    # # Side numbers
    # side_numbers = [5, 4, 2, 3, 4, 6]

    # `ones[w][h]` indicates if the dot number of a one-dot vertical domino is at position (w, h)
    ones = [[model.NewBoolVar(f"ones_{w}_{h}") for h in range(height)] for w in range(width)]

    # `twos[w][h]` indicates if the dot number of a two-dot vertical domino is at position (w, h)
    twos = [[model.NewBoolVar(f"twos_{w}_{h}") for h in range(height)] for w in range(width)]

    # The top numbers must match
    for w in range(width):
        model.Add(
            cp_model.LinearExpr.WeightedSum([ones[w][h] for h in range(height)], [1 for _ in range(height)])
            + cp_model.LinearExpr.WeightedSum([twos[w][h] for h in range(height)], [2 for _ in range(height)])
            == top_numbers[w]
        )

    # The side numbers must match
    for h in range(height):
        model.Add(
            cp_model.LinearExpr.WeightedSum([ones[w][h] for w in range(width)], [1 for _ in range(width)])
            + cp_model.LinearExpr.WeightedSum([twos[w][h] for w in range(width)], [2 for _ in range(width)])
            == side_numbers[h]
        )

    # The dominoes must fit
    for h in range(height):
        for w in range(width):
            # Top-left corner
            if (w, h) == (0, 0):
                if (w, h) in black_squares:
                    model.Add(ones[w][h] + twos[w][h] + twos[w + 1][h] == 0)
                else:
                    model.Add(twos[w][h] == 0)
                    model.Add(ones[w][h] + ones[w][h + 1] <= 1)
                    model.Add(ones[w][h] + twos[w + 1][h] <= 1)
                    model.Add(ones[w][h] + twos[w + 1][h + 1] <= 1)

            # Top-right corner
            elif (w, h) == (width - 1, 0):
                if (w, h) in black_squares:
                    model.Add(ones[w][h] + twos[w][h] == 0)
                else:
                    model.Add(ones[w][h] + ones[w][h + 1] <= 1)
                    model.Add(ones[w][h] + twos[w][h] <= 1)
                    model.Add(ones[w][h] + twos[w][h + 1] <= 1)
                    model.Add(twos[w][h] + twos[w - 1][h] <= 1)
                    model.Add(twos[w][h] + ones[w - 1][h] <= 1)

            # Bottom-left corner
            elif (w, h) == (0, height - 1):
                if (w, h) in black_squares:
                    model.Add(ones[w][h] + ones[w][h - 1] + twos[w][h] + twos[w + 1][h] == 0)
                else:
                    model.Add(ones[w][h] + twos[w][h] == 0)

            # Bottom-right corner
            elif (w, h) == (width - 1, height - 1):
                if (w, h) in black_squares:
                    model.Add(ones[w][h] + ones[w][h - 1] + twos[w][h] == 0)
                else:
                    model.Add(ones[w][h] == 0)
                    model.Add(twos[w][h] + ones[w][h - 1] <= 1)
                    model.Add(twos[w][h] + twos[w - 1][h] <= 1)
                    model.Add(twos[w][h] + ones[w - 1][h - 1] <= 1)

            # Top border
            elif h == 0:
                if (w, h) in black_squares:
                    model.Add(ones[w][h] + twos[w][h] + twos[w + 1][h] == 0)
                else:
                    model.Add(ones[w][h] + twos[w][h] <= 1)
                    model.Add(ones[w][h] + twos[w + 1][h] <= 1)
                    model.Add(twos[w][h] + twos[w + 1][h] <= 1)

            # Left border
            elif w == 0:
                if (w, h) in black_squares:
                    model.Add(ones[w][h] + ones[w][h - 1] + twos[w][h] + twos[w + 1][h] == 0)
                else:
                    model.Add(twos[w][h] == 0)
                    model.Add(ones[w][h] + ones[w][h + 1] <= 1)
                    model.Add(ones[w][h] + ones[w][h - 1] <= 1)
                    model.Add(ones[w][h] + twos[w + 1][h] <= 1)
                    model.Add(ones[w][h] + twos[w + 1][h + 1] <= 1)

            # Right border
            elif w == width - 1:
                if (w, h) in black_squares:
                    model.Add(ones[w][h] + ones[w][h - 1] + twos[w][h] == 0)
                else:
                    model.Add(ones[w][h] + ones[w][h + 1] <= 1)
                    model.Add(ones[w][h] + ones[w][h - 1] <= 1)
                    model.Add(ones[w][h] + twos[w][h] <= 1)
                    model.Add(ones[w][h] + twos[w][h + 1] <= 1)
                    model.Add(twos[w][h] + ones[w - 1][h] <= 1)

            # Bottom border
            elif h == height - 1:
                if (w, h) in black_squares:
                    model.Add(ones[w][h] + ones[w][h - 1] + twos[w][h] + twos[w + 1][h] == 0)
                else:
                    model.Add(ones[w][h] == 0)
                    model.Add(twos[w][h] + twos[w + 1][h] <= 1)
                    model.Add(twos[w][h] + twos[w - 1][h] <= 1)
                    model.Add(twos[w][h] + ones[w][h - 1] <= 1)
                    model.Add(twos[w][h] + ones[w - 1][h - 1] <= 1)

            # Everywhere else
            else:
                if (w, h) in black_squares:
                    model.Add(ones[w][h] + ones[w][h - 1] + twos[w][h] + twos[w + 1][h] == 0)
                else:
                    model.Add(ones[w][h] + ones[w][h - 1] <= 1)
                    model.Add(ones[w][h] + ones[w][h + 1] <= 1)
                    model.Add(ones[w][h] + twos[w][h] <= 1)
                    model.Add(ones[w][h] + twos[w][h + 1] <= 1)
                    model.Add(ones[w][h] + twos[w + 1][h] <= 1)
                    model.Add(ones[w][h] + twos[w + 1][h + 1] <= 1)
                    model.Add(twos[w][h] + twos[w + 1][h] <= 1)
                    model.Add(twos[w][h] + ones[w - 1][h] <= 1)
                    model.Add(twos[w][h] + ones[w][h - 1] <= 1)
                    model.Add(twos[w][h] + ones[w - 1][h - 1] <= 1)

    solver = cp_model.CpSolver()
    solver.Solve(model)

    final_matrix: Matrix = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    # Print the solution
    for h in range(height):
        for w in range(width):
            if solver.Value(ones[w][h]) == 1:
                final_matrix[h][w] = PiecePart.VerticalTop
            elif solver.Value(twos[w][h]) == 1:
                final_matrix[h][w] = PiecePart.HorizontalRight
            elif (w, h) in black_squares:
                pass
            elif w < width - 1 and solver.Value(twos[w + 1][h]) == 1:
                final_matrix[h][w] = PiecePart.HorizontalLeft
            else:
                final_matrix[h][w] = PiecePart.VerticalBottom

    logger.info(final_matrix)
    return final_matrix


# # Black squares (w, h)
# black_squares = [(3, 0), (1, 1), (4, 3), (2, 4)]
#
# # Top numbers
# top_numbers = [2, 5, 3, 5, 3, 6]
#
# # Side numbers
# side_numbers = [5, 4, 2, 3, 4, 6]
# solve(6, top_numbers, side_numbers, black_squares)
