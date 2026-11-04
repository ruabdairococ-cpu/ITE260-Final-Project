import calendar
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

ADMIN_PASSWORD = "admin123"
PERIODS = ["Daily", "Weekly", "Monthly", "Yearly"]

def header(title):
    print("\n" + "=" * 68)
    print(title.center(68))
    print("=" * 68)

def show_menu(title, options):
    header(title)
    for key, label in options:
        print(key + ". " + label)
    print("-" * 68)
    return input("Choose: ").strip()

def print_table(headers, rows, aligns, total=None):
    """Print a boxed table. aligns: 'l' (left) or 'r' (right) for each column.
    The optional total row is always the last row of the table."""
    body = [headers] + rows + ([total] if total else [])
    widths = [max(len(str(row[i])) for row in body) for i in range(len(headers))]
    border = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def fmt(row):
        cells = []
        for i, cell in enumerate(row):
            text = str(cell)
            cells.append(text.rjust(widths[i]) if aligns[i] == "r" else text.ljust(widths[i]))
        return "| " + " | ".join(cells) + " |"

    print(border)
    print(fmt(headers))
    print(border)
    for row in rows:
        print(fmt(row))
    if total:
        print(border)
        print(fmt(total))
    print(border)

def shorten(text, limit=30):
    return text if len(text) <= limit else text[:limit - 3] + "..."

def get_number(message):
    while True:
        value = input(message).strip().replace(",", "")
        if value.isdigit():
            return int(value)
        print("Please enter a whole number.")

def get_amount(message):
    """Accepts whole numbers or decimals (e.g. 25, 25.5, 25.75). Returns a Decimal
    rounded to 2 decimal places. 0 is allowed here; callers reject it if needed."""
    while True:
        value = input(message).strip().replace(",", "").replace("₱", "")
        try:
            amount = Decimal(value)
        except InvalidOperation:
            print("Please enter a valid amount (e.g. 50 or 50.75).")
            continue
        if not amount.is_finite() or amount < 0:
            print("Please enter a valid amount (e.g. 50 or 50.75).")
            continue
        return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def ask_again(message):
    while True:
        answer = input(message + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")

def peso(amount):
    sign = "-" if amount < 0 else ""
    return sign + "₱" + f"{abs(amount):,.2f}"

def budget_status(has_budget, balance):
    if not has_budget:
        return "NO BUDGET"
    if balance < 0:
        return "OVER BUDGET"
    if balance == 0:
        return "LIMIT REACHED"
    return "WITHIN BUDGET"

def show_date(day):
    return day.strftime("%m/%d/%Y")

def dates_label(items):
    days = sorted({item[2] for item in items})
    if not days:
        return "No expenses"
    if len(days) == 1:
        return show_date(days[0])
    return show_date(days[0]) + " - " + show_date(days[-1])

def get_date(prompt="Date (MM/DD/YYYY): "):
    while True:
        value = input(prompt)
        try:
            month, day, year = value.split("/")
            return date(int(year), int(month), int(day))
        except ValueError:
            print("Invalid date. Use MM/DD/YYYY.")

def get_student_name():
    while True:
        name = input("Enter your student name (Surname): ")
        if name != "" and name.replace(" ", "").isalpha():
            return name
        print("Use letters and spaces only, with no numbers or symbols.")

def period_dates(period, today=None):
    if today is None:
        today = date.today()
    if period == "Daily":
        return today, today
    if period == "Weekly":
        start = today - timedelta(days=today.weekday())
        return start, start + timedelta(days=6)
    if period == "Monthly":
        start = date(today.year, today.month, 1)
        if today.month == 12:
            end = date(today.year, 12, 31)
        else:
            end = date(today.year, today.month + 1, 1) - timedelta(days=1)
        return start, end
    return date(today.year, 1, 1), date(today.year, 12, 31)

def print_range(period, start, end, note=""):
    print("\n" + period.upper() + " RANGE: " + range_text(start, end) + note)

def choose_period():
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")
    print("4. Yearly")
    choice = input("Choose period: ")
    if choice == "1":
        return "Daily"
    if choice == "2":
        return "Weekly"
    if choice == "3":
        return "Monthly"
    if choice == "4":
        return "Yearly"
    print("Invalid choice.")
    return ""

def choose_category(categories, allow_new=True):
    while True:
        print("\nCategories:")
        for i in range(len(categories)):
            print(str(i + 1) + ". " + categories[i])
        if allow_new:
            print(str(len(categories) + 1) + ". Add Custom Category")
        choice = get_number("Choose category: ")
        if 1 <= choice <= len(categories):
            return categories[choice - 1]
        if allow_new and choice == len(categories) + 1:
            new_category = input("Enter category name: ")
            if new_category == "":
                print("Category cannot be blank.")
            elif new_category in categories:
                print("Category already exists.")
                return new_category
            else:
                categories.append(new_category)
                print("Category added.")
                return new_category
        print("Invalid choice.")

def student_expenses(expenses, name):
    result = []
    for item in expenses:
        if item[1] == name:
            result.append(item)
    return result

def range_text(start, end):
    return show_date(start) + " to " + show_date(end)

def add_months(day, months):
    index = day.month - 1 + months
    year = day.year + index // 12
    month = index % 12 + 1
    return date(year, month, min(day.day, calendar.monthrange(year, month)[1]))

def budget_end(period, start):
    # The student picks when a budget starts; the system decides when it ends.
    if period == "Daily":
        return start
    if period == "Weekly":
        return start + timedelta(days=6)
    if period == "Monthly":
        return add_months(start, 1) - timedelta(days=1)
    return add_months(start, 12) - timedelta(days=1)

def next_period_start(period, today):
    if period == "Weekly":
        return today + timedelta(days=7 - today.weekday())
    if period == "Monthly":
        return add_months(date(today.year, today.month, 1), 1)
    return date(today.year + 1, 1, 1)

def choose_start_date(period):
    today = date.today()
    options = [("Start today", today), ("Start tomorrow", today + timedelta(days=1))]
    if period == "Weekly":
        options.append(("Start next week (Monday)", next_period_start(period, today)))
    elif period == "Monthly":
        options.append(("Start next month (1st)", next_period_start(period, today)))
    elif period == "Yearly":
        options.append(("Start next year (Jan 1)", next_period_start(period, today)))
    print("\nWhen should this " + period.lower() + " budget start?")
    for i, (label, day) in enumerate(options, 1):
        print(str(i) + ". " + label + " - " + show_date(day))
    print(str(len(options) + 1) + ". Pick a different start date")
    choice = get_number("Choose: ")
    if 1 <= choice <= len(options):
        start = options[choice - 1][1]
    elif choice == len(options) + 1:
        start = get_date("Start date (MM/DD/YYYY): ")
        while start < today:
            print("Start date cannot be in the past.")
            start = get_date("Start date (MM/DD/YYYY): ")
    else:
        print("Invalid choice.")
        return None
    end = budget_end(period, start)
    print(period + " budget runs from " + range_text(start, end))
    return start, end

def budget_state(budget):
    today = date.today()
    if budget[4] > today:
        return "Upcoming"
    if budget[5] < today:
        return "Ended"
    return "Active"

def find_budget(budgets, name, period, category, start, end):
    for budget in budgets:
        if (budget[0] == name and budget[1] == period and budget[2] == category
                and budget[4] == start and budget[5] == end):
            return budget
    return []

def overlapping_budgets(budgets, name, period, category, start, end):
    result = []
    for budget in budgets:
        if (budget[0] == name and budget[1] == period and budget[2] == category
                and budget[4] <= end and start <= budget[5]):
            result.append(budget)
    return result

def spending_for(expenses, name, category, start, end):
    total = 0
    for item in expenses:
        if item[1] == name and item[4] == category:
            if start <= item[2] <= end:
                total += item[3]
    return total

def set_one_budget(budgets, categories, name):
    period = choose_period()
    if not period:
        return
    dates = choose_start_date(period)
    if not dates:
        return
    start, end = dates
    category = choose_category(categories)
    amount = get_amount("Budget amount for " + category + ": ")
    while amount <= 0:
        print("Budget must be greater than 0.")
        amount = get_amount("Budget amount for " + category + ": ")

    overlaps = overlapping_budgets(budgets, name, period, category, start, end)
    if overlaps:
        print("\nYou already have a " + period.lower() + " budget for " + category + ":")
        for old in overlaps:
            print("  " + range_text(old[4], old[5]) + " - " + peso(old[3]))
        if input("Replace it with this new budget? (y/n): ").strip().lower() != "y":
            print("Budget not changed.")
            return
        for old in overlaps:
            budgets.remove(old)
    budgets.append([name, period, category, amount, start, end])
    print("Budget set for " + category + ": " + peso(amount))

    print("\nBUDGET TABLE - " + period.upper())
    print("DATE RANGE: " + range_text(start, end))
    rows = []
    running_total = 0
    for item in budgets:
        if (item[0] == name and item[1] == period
                and item[4] == start and item[5] == end):
            rows.append([item[2], peso(item[3])])
            running_total += item[3]
    print_table(["CATEGORY", "BUDGETED AMOUNT"], rows, ["l", "r"],
                ["RUNNING TOTAL", peso(running_total)])

def set_my_budget(expenses, budgets, categories, name):
    header("SET BUDGET BY CATEGORY")
    while True:
        set_one_budget(budgets, categories, name)
        if not ask_again("\nSet another budget?"):
            return

def check_remaining_budget(expenses, budgets, categories, name):
    header("CHECK REMAINING BUDGET")
    period = choose_period()
    if not period:
        return
    today = date.today()
    mine = [b for b in budgets if b[0] == name and b[1] == period and b[5] >= today]
    if not mine:
        print("\nNo active or upcoming " + period.lower() + " budget. Use Set Budget first.")
        return
    for start, end in sorted({(b[4], b[5]) for b in mine}):
        print_range(period, start, end, " (UPCOMING)" if start > today else " (ACTIVE)")
        rows = []
        total_budget = 0
        total_balance = 0
        for category in categories:
            budget = find_budget(budgets, name, period, category, start, end)
            if budget:
                spent = spending_for(expenses, name, category, start, end)
                balance = budget[3] - spent
                percent = balance / budget[3] * 100
                rows.append([category, peso(budget[3]), peso(balance), f"{percent:.1f}%",
                             budget_status(True, balance)])
                total_budget += budget[3]
                total_balance += balance
        if not rows:
            continue
        total_percent = total_balance / total_budget * 100
        print_table(["CATEGORY", "SET BUDGET", "BALANCE", "% REMAINING", "STATUS"], rows,
                    ["l", "r", "r", "r", "l"],
                    ["TOTAL", peso(total_budget), peso(total_balance), f"{total_percent:.1f}%",
                     budget_status(True, total_balance)])

def delete_my_budget(budgets, name):
    header("DELETE BUDGET")
    while True:
        mine = sorted([b for b in budgets if b[0] == name],
                      key=lambda b: (b[4], b[1], b[2]))
        if not mine:
            print("No budgets set.")
            return
        rows = []
        for i, budget in enumerate(mine, 1):
            rows.append([i, budget[2], budget[1], range_text(budget[4], budget[5]),
                         peso(budget[3]), budget_state(budget)])
        print_table(["NO.", "CATEGORY", "PERIOD", "DATE RANGE", "BUDGET", "STATE"], rows,
                    ["r", "l", "l", "l", "r", "l"])
        text = input("Enter budget number to delete (0 to cancel): ").strip()
        if text == "0":
            print("Cancelled.")
            return
        if not text.isdigit() or not (1 <= int(text) <= len(mine)):
            print("Invalid budget number. Please enter one number shown in the table.")
            continue
        chosen = mine[int(text) - 1]
        print("\nBudget selected:")
        rows = [[chosen[2], chosen[1], range_text(chosen[4], chosen[5]),
                 peso(chosen[3]), budget_state(chosen)]]
        print_table(["CATEGORY", "PERIOD", "DATE RANGE", "BUDGET", "STATE"], rows,
                    ["l", "l", "l", "r", "l"])
        if ask_again("Delete this budget?"):
            budgets.remove(chosen)
            print("Budget deleted.")
        else:
            print("Budget not deleted.")
        if not ask_again("\nDelete another budget?"):
            return
        print()
def show_category_budget_status(expenses, budgets, name, category):
    today = date.today()
    rows = []
    for period in PERIODS:
        for budget in budgets:
            if (budget[0] == name and budget[1] == period and budget[2] == category
                    and budget[4] <= today <= budget[5]):
                spent = spending_for(expenses, name, category, budget[4], budget[5])
                balance = budget[3] - spent
                rows.append([period, range_text(budget[4], budget[5]), peso(budget[3]),
                             peso(spent), peso(balance), budget_status(True, balance)])
    if rows:
        print("\nBUDGET CHECK - " + category)
        print_table(["PERIOD", "DATE RANGE", "SET BUDGET", "SPENT", "BALANCE", "STATUS"],
                    rows, ["l", "l", "r", "r", "r", "l"])
    else:
        print("\n" + category + ": " + budget_status(False, 0))

def add_expense(expenses, budgets, categories, name):
    header("ADD EXPENSE")
    while True:
        expense_date = date.today()
        print("Date automatically set to:", show_date(expense_date))
        amount = get_amount("Spend amount: ")

        while amount <= 0:
            print("Amount must be greater than 0.")
            amount = get_amount("Spend amount: ")

        category = choose_category(categories)
        description = input("Description: ")

        new_id = 1
        for item in expenses:
            if item[0] >= new_id:
                new_id = item[0] + 1

        expenses.append([new_id, name, expense_date, amount, category, description])
        print("Expense added.")
        show_category_budget_status(expenses, budgets, name, category)

        if not ask_again("\nAdd another expense?"):
            return
        print()

def print_records(records, show_category_totals=False, numbers=None):
    """numbers: optional list of display IDs (same length as records). By default
    the IDs are 1, 2, 3... so they always stay in order after deleting."""
    if numbers is None:
        numbers = list(range(1, len(records) + 1))
    rows = []
    for number, item in zip(numbers, records):
        rows.append([number, show_date(item[2]), item[4], peso(item[3]), shorten(item[5])])
    grand_total = sum(item[3] for item in records)
    print_table(["ID", "DATE", "CATEGORY", "AMOUNT", "DESCRIPTION"], rows,
                ["r", "l", "l", "r", "l"],
                ["", "", "TOTAL", peso(grand_total), ""])
    print("Records:", len(records))
    if show_category_totals:
        totals = {}
        for item in records:
            totals[item[4]] = totals.get(item[4], 0) + item[3]
        ranked = sorted(totals.items(), key=lambda pair: pair[1], reverse=True)
        print("\nTOTAL PER CATEGORY (highest to lowest)")
        print_table(["CATEGORY", "TOTAL SPENT"],
                    [[category, peso(total)] for category, total in ranked],
                    ["l", "r"], ["TOTAL", peso(grand_total)])

def view_my_expenses(expenses, name):
    header("MY EXPENSES")
    records = student_expenses(expenses, name)
    if not records:
        print("No expenses recorded.")
    else:
        print_records(records, True)

def search_my_expenses(expenses, categories, name):
    header("SEARCH MY EXPENSES")
    while True:
        records = student_expenses(expenses, name)
        position = {item[0]: n for n, item in enumerate(records, 1)}
        print("1. Search by date")
        print("2. Search by category")
        print("3. Search by description")
        choice = input("Choose option: ")
        result = []
        valid = True
        if choice == "1":
            chosen_date = get_date()
            for item in records:
                if item[2] == chosen_date:
                    result.append(item)
        elif choice == "2":
            category = choose_category(categories, False)
            for item in records:
                if item[4] == category:
                    result.append(item)
        elif choice == "3":
            keyword = input("Description keyword: ").lower()
            for item in records:
                if keyword in item[5].lower():
                    result.append(item)
        else:
            print("Invalid choice.")
            valid = False
        if valid:
            if result:
                print_records(result, numbers=[position[item[0]] for item in result])
            else:
                print("No matching expenses.")
        if not ask_again("\nSearch again?"):
            return
        print()

def update_my_expense(expenses, categories, name):
    header("UPDATE MY EXPENSE")
    while True:
        records = student_expenses(expenses, name)
        if not records:
            print("No expenses recorded.")
            return
        print_records(records)
        text = input("Enter expense ID to update (0 to cancel): ").strip()
        if text == "0":
            print("Cancelled.")
            return
        if not text.isdigit() or not (1 <= int(text) <= len(records)):
            print("Expense ID not found.")
            continue
        item = records[int(text) - 1]
        amount = get_amount("New amount (0 to keep): ")
        if amount > 0:
            item[3] = amount
        if input("Change category? (y/n): ").lower() == "y":
            item[4] = choose_category(categories)
        description = input("New description (blank to keep): ")
        if description:
            item[5] = description
        print("Expense updated.")
        if not ask_again("\nUpdate another expense?"):
            return
        print()

def delete_my_expense(expenses, name):
    header("DELETE MY EXPENSE")
    while True:
        records = student_expenses(expenses, name)
        if not records:
            print("No expenses recorded.")
            return
        print_records(records)
        text = input("Enter the ID of the expense to delete (0 to cancel): ").strip()
        if text == "0":
            print("Cancelled.")
            return
        if not text.isdigit() or not (1 <= int(text) <= len(records)):
            print("Invalid ID. Please enter one ID shown in the table.")
            continue
        number = int(text)
        chosen = records[number - 1]
        print("\nExpense selected:")
        print_records([chosen], numbers=[number])
        if ask_again("Delete this expense?"):
            expenses.remove(chosen)
            print("Expense deleted. IDs have been renumbered.")
        else:
            print("Nothing deleted.")
        if not ask_again("Delete another expense?"):
            return
        print()

def print_expense_table(records, budgets, name, period, start, end):
    print_range(period, start, end)

    category_names = []
    for item in records:
        if item[4] not in category_names:
            category_names.append(item[4])
    for budget in budgets:
        if (budget[0] == name and budget[1] == period and budget[4] == start
                and budget[5] == end and budget[2] not in category_names):
            category_names.append(budget[2])

    data = []
    for category in category_names:
        category_records = [item for item in records if item[4] == category]
        spent = sum(item[3] for item in category_records)
        data.append((category, category_records, spent,
                     find_budget(budgets, name, period, category, start, end)))
    data.sort(key=lambda entry: entry[2], reverse=True)

    rows = []
    total_spent = 0
    total_budget = 0
    total_balance = 0
    has_unbudgeted = False
    for category, category_records, spent, budget in data:
        total_spent += spent
        if budget:
            balance = budget[3] - spent
            total_budget += budget[3]
            total_balance += balance
            rows.append([category, dates_label(category_records), peso(spent),
                         peso(budget[3]), peso(balance), budget_status(True, balance)])
        else:
            has_unbudgeted = True
            rows.append([category, dates_label(category_records), peso(spent),
                         "-", "-", budget_status(False, 0)])

    has_budget = total_budget > 0
    total_row = ["TOTAL", "-", peso(total_spent),
                 peso(total_budget) if has_budget else "-",
                 peso(total_balance) if has_budget else "-",
                 budget_status(has_budget, total_balance)]
    print_table(["CATEGORY", "DATE(S)", "SPENT", "SET BUDGET", "BALANCE", "STATUS"],
                rows, ["l", "l", "r", "r", "r", "l"], total_row)
    if has_unbudgeted and has_budget:
        print("Note: total balance only counts categories that have a budget.")
    if data and data[0][2] > 0:
        print("Highest spending category:", data[0][0], "-", peso(data[0][2]))

def view_expense_summary(expenses, budgets, name):
    header("MY EXPENSE SUMMARY")
    period = choose_period()
    if not period:
        return
    today = date.today()
    ranges = sorted({(b[4], b[5]) for b in budgets
                     if b[0] == name and b[1] == period and b[4] <= today <= b[5]})
    if not ranges:
        ranges = [period_dates(period)]
    records = student_expenses(expenses, name)
    for start, end in ranges:
        filtered = [item for item in records if start <= item[2] <= end]
        print_expense_table(filtered, budgets, name, period, start, end)

        total = sum(item[3] for item in filtered)
        rows = [["Total records", len(filtered), "-"],
                ["Total expenses", peso(total), "-"]]
        if filtered:
            highest = max(filtered, key=lambda item: item[3])
            lowest = min(filtered, key=lambda item: item[3])
            average = (total / len(filtered)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            rows.append(["Average expense", peso(average), "-"])
            rows.append(["Highest single expense", peso(highest[3]), highest[4]])
            rows.append(["Lowest single expense", peso(lowest[3]), lowest[4]])
        print("\nADDITIONAL SUMMARY")
        print_table(["ITEM", "AMOUNT", "CATEGORY"], rows, ["l", "r", "l"])

def categorize_my_expenses(expenses, name):
    header("EXPENSES BY CATEGORY")
    records = student_expenses(expenses, name)
    if not records:
        print("No expenses recorded.")
        return
    totals = {}
    for item in records:
        totals[item[4]] = totals.get(item[4], 0) + item[3]
    sorted_totals = sorted(totals.items(), key=lambda pair: pair[1], reverse=True)
    grand_total = sum(totals.values())
    rows = []
    for rank, (category, spent) in enumerate(sorted_totals, 1):
        share = spent / grand_total * 100
        rows.append([rank, category, peso(spent), f"{share:.1f}%"])
    print_table(["RANK", "CATEGORY", "TOTAL SPENT", "SHARE"], rows,
                ["r", "l", "r", "r"], ["", "TOTAL", peso(grand_total), "100.0%"])
    print("Highest spending category:", sorted_totals[0][0], "-", peso(sorted_totals[0][1]))

def manage_categories(categories, expenses):
    while True:
        header("MANAGE CATEGORIES")
        for i in range(len(categories)):
            print("  " + str(i + 1) + ". " + categories[i])
        print("-" * 68)
        print("  A. Add category")
        print("  E. Edit category")
        print("  D. Delete category")
        print("  0. Back")
        print("-" * 68)
        choice = input("Choose: ").strip().lower()
        if choice == "a":
            name = input("New category: ")
            if name and name not in categories:
                categories.append(name)
                print("Category added.")
            else:
                print("Name is blank or already exists.")
        elif choice in ["e", "d"]:
            number = get_number("Category number: ")
            if number < 1 or number > len(categories):
                print("Invalid category number.")
                continue
            old_name = categories[number - 1]
            if choice == "e":
                new_name = input("New category name: ")
                if not new_name or new_name in categories:
                    print("Name is blank or already exists.")
                else:
                    categories[number - 1] = new_name
                    for item in expenses:
                        if item[4] == old_name:
                            item[4] = new_name
                    print("Category updated in existing expense records.")
            elif input("Delete category but keep old records? (y/n): ").lower() == "y":
                categories.remove(old_name)
                print("Category removed from choices; old records are preserved.")
        elif choice == "0":
            return
        else:
            print("Invalid choice.")

def view_admin_summary(expenses):
    header("OVERALL EXPENSE SUMMARY")
    if not expenses:
        print("No expenses recorded.")
        return
    totals = {}
    for item in expenses:
        totals[item[4]] = totals.get(item[4], 0) + item[3]
    ranked = sorted(totals.items(), key=lambda pair: pair[1], reverse=True)
    grand_total = sum(totals.values())
    rows = []
    for rank, (category, total) in enumerate(ranked, 1):
        rows.append([rank, category, peso(total)])
    print_table(["RANK", "CATEGORY", "TOTAL SPENT"], rows, ["r", "l", "r"],
                ["", "TOTAL EXPENSES", peso(grand_total)])
    print("Total records:", len(expenses))

def submit_feedback(feedback, name):
    header("SUBMIT FEEDBACK")
    while True:
        message = input("Enter feedback: ")
        if message:
            feedback.append([name, message])
            print("Feedback submitted.")
        else:
            print("Feedback cannot be blank.")
        if not ask_again("\nSubmit another feedback?"):
            return

def review_feedback(feedback):
    header("STUDENT FEEDBACK")
    if not feedback:
        print("No feedback submitted.")
    for item in feedback:
        print("STUDENT:", item[0])
        print("FEEDBACK:", item[1])
        print("-" * 40)

def budget_menu(expenses, budgets, categories, name):
    while True:
        choice = show_menu("BUDGET", [
            ("1", "Set Budget by Category"),
            ("2", "Check Remaining Budget"),
            ("3", "Delete Budget"),
            ("0", "Back"),
        ])
        if choice == "1":
            set_my_budget(expenses, budgets, categories, name)
        elif choice == "2":
            check_remaining_budget(expenses, budgets, categories, name)
        elif choice == "3":
            delete_my_budget(budgets, name)
        elif choice == "0":
            return
        else:
            print("Invalid choice.")

def expenses_menu(expenses, budgets, categories, name):
    while True:
        choice = show_menu("EXPENSES", [
            ("1", "Add Expense"),
            ("2", "View My Expenses"),
            ("3", "Search My Expenses"),
            ("4", "Update My Expense"),
            ("5", "Delete My Expense"),
            ("0", "Back"),
        ])
        if choice == "1":
            add_expense(expenses, budgets, categories, name)
        elif choice == "2":
            view_my_expenses(expenses, name)
        elif choice == "3":
            search_my_expenses(expenses, categories, name)
        elif choice == "4":
            update_my_expense(expenses, categories, name)
        elif choice == "5":
            delete_my_expense(expenses, name)
        elif choice == "0":
            return
        else:
            print("Invalid choice.")

def insights_menu(expenses, budgets, name):
    while True:
        choice = show_menu("INSIGHTS", [
            ("1", "View My Expense Summary"),
            ("2", "Expenses by Category"),
            ("3", "Calculate Total Expenses"),
            ("0", "Back"),
        ])
        if choice == "1":
            view_expense_summary(expenses, budgets, name)
        elif choice == "2":
            categorize_my_expenses(expenses, name)
        elif choice == "3":
            total = sum(item[3] for item in student_expenses(expenses, name))
            print("Total of all expenses:", peso(total))
        elif choice == "0":
            return
        else:
            print("Invalid choice.")

def student_menu(expenses, budgets, categories, feedback, saved_name):
    name = saved_name
    if not name:
        header("STUDENT ACCESS")
        name = get_student_name()
    while True:
        choice = show_menu("STUDENT MENU - " + name, [
            ("1", "Budget"),
            ("2", "Expenses"),
            ("3", "Insights"),
            ("4", "Submit Feedback"),
            ("0", "Exit Student Menu"),
        ])
        if choice == "1":
            budget_menu(expenses, budgets, categories, name)
        elif choice == "2":
            expenses_menu(expenses, budgets, categories, name)
        elif choice == "3":
            insights_menu(expenses, budgets, name)
        elif choice == "4":
            submit_feedback(feedback, name)
        elif choice == "0":
            return name
        else:
            print("Invalid choice.")

def admin_menu(expenses, categories, feedback):
    header("ADMIN ACCESS")
    if input("Enter admin password: ") != ADMIN_PASSWORD:
        print("Incorrect password.")
        return
    while True:
        choice = show_menu("ADMIN MENU", [
            ("1", "Manage Categories"),
            ("2", "View Student Expenses"),
            ("3", "Overall Expense Summary"),
            ("4", "Review Feedback"),
            ("0", "Back"),
        ])
        if choice == "1":
            manage_categories(categories, expenses)
        elif choice == "2":
            name = input("Enter student name: ")
            records = student_expenses(expenses, name)
            if records:
                print_records(records)
            else:
                print("No expenses found for that student.")
        elif choice == "3":
            view_admin_summary(expenses)
        elif choice == "4":
            review_feedback(feedback)
        elif choice == "0":
            return
        else:
            print("Invalid choice.")

def main():
    expenses = []
    budgets = []
    categories = ["Food", "Transportation", "School Supplies", "Mobile/Data"]
    feedback = []
    saved_name = ""
    while True:
        choice = show_menu("EXPENSEASE", [
            ("1", "Student"),
            ("2", "Admin"),
            ("0", "Exit"),
        ])
        if choice == "1":
            saved_name = student_menu(expenses, budgets, categories, feedback, saved_name)
        elif choice == "2":
            admin_menu(expenses, categories, feedback)
        elif choice == "0":
            print("Thank you for using ExpensEase.")
            break
        else:
            print("Invalid choice.")

main()
