"""
Utility functions for Library Manager
"""

SEPARATOR = "x--------------------x--------------------x--------------------x--------------------x--------------------x--------------------x"


def calculate_days(issue_date, return_date):
    """Calculate the number of days between issue and return"""
    delta = str(return_date - issue_date)
    days = int(delta.split()[0])
    return days


def calculate_penalty(issue_date, return_date, issue_days):
    """Calculate penalty based on days kept"""
    days_kept = calculate_days(issue_date, return_date)
    
    if days_kept <= issue_days:
        return None
    else:
        late_days = days_kept - issue_days
        if late_days <= 7:
            return 100
        else:
            return 100 + (late_days - 7) * 20


def print_separator():
    """Print a formatted separator"""
    print(SEPARATOR)
