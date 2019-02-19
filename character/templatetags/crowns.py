from django import template

register = template.Library()

def crowns(pennies):
    #12 pence to the crown. Output as Crowns and Pence, actually only work with pence because fuck base 12.
    crowns = pennies // 12
    pence = pennies % 12
    return "{0}/{1}".format(crowns, pence)

register.filter('crowns', crowns)
