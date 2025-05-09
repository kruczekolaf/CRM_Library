from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template-Filter, um Werte aus einem Dictionary mittels Schlüssel abzurufen
    Verwendung: {{ dict|get_item:key }}
    """
    return dictionary.get(key, 0)