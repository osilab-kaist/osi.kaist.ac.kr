from django import template
from django.utils.safestring import mark_safe
from core.clean_html import clean_news_post_html

register = template.Library()


@register.filter
def clean_news_post(value):
    """
    Comprehensive cleaning function for news post HTML content.
    Removes inline styles and ensures all links have target="_blank" and rel="noopener noreferrer".
    
    Note: This filter is mainly for backwards compatibility. The Post model now
    automatically cleans HTML on save, so this filter is typically not needed.
    """
    if not value:
        return value
    
    cleaned_html = clean_news_post_html(value)
    return mark_safe(cleaned_html)
