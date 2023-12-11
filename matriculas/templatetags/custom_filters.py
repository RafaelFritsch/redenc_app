from django import template
from datetime import timedelta, date

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)



def get_month_range(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        # Adiciona um mês
        if current_date.month == 12:
            current_date = date(current_date.year + 1, 1, 1)
        else:
            current_date = date(current_date.year, current_date.month + 1, 1)

def get_month_range(self):
        return get_month_range(self.data_inicial_processo, self.data_final_processo)