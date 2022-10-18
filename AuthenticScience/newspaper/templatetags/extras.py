from django import template

register = template.Library()

#this filter gets the value of a key in a dictionary
@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    if key:
        return dict_data.get(key)
    
# this filter formats a datetime variable, given the formatting string
@register.filter('formatdatetime')
def formatdatetime(article, format_string):
    return article.published_date.strftime(format_string)
