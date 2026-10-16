"""Library loan management and fine calculation."""

import ast
import json
import operator
from datetime import datetime

loans = {}
FINE_PER_DAY = 2


def add_book_loan(student_id, book_id, dates=None):
    """Record a book borrowed by a student."""
    if not student_id or not isinstance(book_id, str):
        return

    if dates is None:
        dates = []

    dates.append(str(datetime.now()))
    loans.setdefault(student_id, []).append(book_id)

    print(
        f"{student_id} borrowed {book_id} "
        f"(loan dates on record: {len(dates)})"
    )


def return_book(student_id, book_id):
    """Remove a returned book from student records."""
    student_loans = loans.get(student_id, [])

    if book_id not in student_loans:
        return

    student_loans.remove(book_id)

    if not student_loans:
        del loans[student_id]


def calculate_fine(days_overdue):
    """Calculate a non-negative overdue fine."""
    return max(0, days_overdue) * FINE_PER_DAY


def renew_book(student_id, book_id, extra_days):
    """Renew an existing borrowed book."""
    if book_id not in loans.get(student_id, []):
        return

    if extra_days < 0:
        raise ValueError("Renewal days cannot be negative")

    print(
        f"Renewed {book_id} for {student_id} "
        f"by {extra_days} days"
    )


def load_records(file="loans.json"):
    """Read saved loan records from a JSON file."""
    with open(file, "r", encoding="utf-8") as record_file:
        records = json.load(record_file)

    if not isinstance(records, dict):
        raise ValueError("Invalid loan records format")

    loans.clear()
    loans.update(records)


def save_records(file="loans.json"):
    """Save current loan records to a JSON file."""
    with open(file, "w", encoding="utf-8") as record_file:
        json.dump(loans, record_file, indent=4)


def fine_from_rule(rule, days):
    """Evaluate basic arithmetic fine rules safely."""
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def evaluate(node):
        """Evaluate an approved arithmetic expression."""
        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value

        if isinstance(node, ast.Name) and node.id == "days":
            return days

        if isinstance(node, ast.BinOp):
            operation = operations.get(type(node.op))
            if operation is not None:
                return operation(
                    evaluate(node.left),
                    evaluate(node.right),
                )

        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -evaluate(node.operand)

        raise ValueError("Unsupported fine calculation rule")

    return evaluate(ast.parse(rule, mode="eval").body)


def print_report():
    """Display the current student loan records."""
    print("Loan Report")
    for student_id, books in loans.items():
        print(student_id, "->", books)


def main():
    """Demonstrate borrowing, renewal and fine calculations."""
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", 4521)

    return_book("S999", "B-NONE")
    renew_book("S101", "B-ALGO", 21)

    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))

    user_input = input(
        "Days overdue for S102 (press Enter for 0): "
    ) or "0"

    try:
        days = int(user_input)
    except ValueError:
        print("Invalid input. Using zero overdue days.")
        days = 0

    print("S102 owes:", calculate_fine(days))

    save_records()
    load_records()
    print_report()


if __name__ == "__main__":
    main()
