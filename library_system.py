import json
import os
from datetime import datetime

# Global state
loans = {}
FINE_PER_DAY = 2

def add_book_loan(student_id, book_id, dates=[]):
    if not student_id:
        return
    dates.append(str(datetime.now()))
    loans[student_id] = loans.get(student_id, []) + [book_id]
    print("%s borrowed %s (loan dates on record: %d)" % (student_id, book_id, len(dates)))

def return_book(student_id, book_id):
    try:
        loans[student_id].remove(book_id)
        if len(loans[student_id]) == 0:
            del loans[student_id]
    except (KeyError, ValueError):
        return

def calculate_fine(days_overdue):
    return days_overdue * FINE_PER_DAY

def renewBook(student_id, book_id, extra_days):
    """Renew an existing book loan."""
    if book_id not in loans.get(student_id, []):
        return
    print(f"Renewed {book_id} for {student_id} by {extra_days} days")


def load_records(file="loans.json"):
    f = open(file, "r")
    global loans
    loans = json.loads(f.read())
    f.close()

def save_records(file="loans.json"):
    f = open(file, "w")
    f.write(json.dumps(loans))
    f.close()
def fine_from_rule(rule, days):
    """Safely calculate a fine from a basic arithmetic expression."""
    import ast
    import operator

    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.Name) and node.id == "days":
            return days
        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            return operations[type(node.op)](
                evaluate(node.left), evaluate(node.right)
            )
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -evaluate(node.operand)
        raise ValueError("Unsupported fine calculation rule")

    return evaluate(ast.parse(rule, mode="eval").body)


def print_report():
    print("Loan Report")
    for s in loans:
        print(s, "->", loans[s])

def main():
    add_book_loan("S101", "B-ALGO")
    add_book_loan("S102", "B-NETW")
    add_book_loan("", "B-DBMS")
    add_book_loan("S103", 4521)  # book id should be a string
    return_book("S999", "B-NONE")
    renewBook("S101", "B-ALGO", 21)
    print("Fine for 5 days:", calculate_fine(5))
    print("Fine for -3 days:", calculate_fine(-3))
    print("Fine via rule:", fine_from_rule("days * 2 + 10", 4))
    days = input("Days overdue for S102 (press Enter for 0): ") or "0"
    print("S102 owes:", calculate_fine(int(days)))
    save_records()
    load_records()
    print_report()

main()
