import re

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


def fix_links_in_html(html_content):
    """
    Process HTML content to ensure all links have target="_blank" and rel="noopener noreferrer"
    to prevent window.opener security vulnerabilities.
    Returns the fixed HTML as a string.
    """
    if not html_content:
        return html_content
    
    if HAS_BS4:
        # Use BeautifulSoup for proper HTML parsing
        soup = BeautifulSoup(str(html_content), "html.parser")
        
        for link in soup.find_all("a", href=True):
            # Normalize target attribute - ensure it's "_blank" (fix cases like "blank")
            target = link.get("target", "").strip()
            if target and target.lower() != "_blank":
                # If target exists but is not "_blank", replace it
                link["target"] = "_blank"
            elif not target:
                # Add target="_blank" if not present
                link["target"] = "_blank"
            
            # Ensure rel="noopener noreferrer" is present
            rel_attrs = link.get("rel", [])
            if not isinstance(rel_attrs, list):
                rel_attrs = [rel_attrs] if rel_attrs else []
            
            # Convert to list of strings if needed
            rel_attrs = [str(r) for r in rel_attrs]
            
            if "noopener" not in rel_attrs:
                rel_attrs.append("noopener")
            if "noreferrer" not in rel_attrs:
                rel_attrs.append("noreferrer")
            
            link["rel"] = rel_attrs
        
        return str(soup)
    else:
        # Fallback to regex-based approach (less robust but doesn't require bs4)
        html = str(html_content)
        
        # Pattern to match <a> tags with various attribute orders
        def process_link(match):
            tag_content = match.group(0)
            
            # Check if target="_blank" exists
            if 'target="_blank"' not in tag_content and "target='_blank'" not in tag_content:
                # Add target="_blank" before the closing >
                tag_content = tag_content.rstrip(">") + ' target="_blank">'
            
            # Check if rel="noopener noreferrer" exists
            if 'rel="noopener noreferrer"' not in tag_content and "rel='noopener noreferrer'" not in tag_content:
                # Check if there's already a rel attribute
                if 'rel="' in tag_content or "rel='" in tag_content:
                    # Add to existing rel attribute (simplified - assumes it's at the end)
                    if 'rel="' in tag_content:
                        tag_content = tag_content.replace('rel="', 'rel="noopener noreferrer ')
                    elif "rel='" in tag_content:
                        tag_content = tag_content.replace("rel='", "rel='noopener noreferrer ")
                else:
                    # Add new rel attribute before the closing >
                    tag_content = tag_content.rstrip(">") + ' rel="noopener noreferrer">'
            
            return tag_content
        
        # Match <a> tags with href attribute
        pattern = r'<a\s+[^>]*href\s*=\s*["\'][^"\']*["\'][^>]*>'
        html = re.sub(pattern, process_link, html, flags=re.IGNORECASE)
        
        return html


def fix_malformed_attributes(html_content):
    """
    Fix malformed HTML attributes that may have been corrupted.
    For example: target="_blank style=" becomes target="_blank"
    For anchor tags, rebuild them cleanly with only valid attributes.
    Returns the fixed HTML as a string.
    """
    if not html_content:
        return html_content
    
    if HAS_BS4:
        # Use BeautifulSoup for proper HTML parsing
        soup = BeautifulSoup(str(html_content), "html.parser")
        
        # Special handling for anchor tags - rebuild them cleanly
        for link in soup.find_all("a"):
            # Store valid attributes
            href = link.get("href", "")
            target = link.get("target", "")
            rel = link.get("rel", [])
            
            # Clear all attributes
            link.attrs.clear()
            
            # Only restore valid attributes
            if href:
                link["href"] = str(href).strip()
            if target:
                # Normalize target - only keep if it's "_blank"
                target_clean = str(target).strip().lower()
                if target_clean == "_blank":
                    link["target"] = "_blank"
            if rel:
                # Normalize rel - ensure it's a list
                if not isinstance(rel, list):
                    rel = [rel] if rel else []
                rel = [str(r).strip() for r in rel if r]
                if rel:
                    link["rel"] = rel
        
        # Clean up all other elements - remove suspicious attributes
        for element in soup.find_all(True):  # True means all tags
            if element.name == "a":
                continue  # Already handled above
            
            attrs_to_remove = []
            for attr_name, attr_value in list(element.attrs.items()):
                # Remove style attributes (handled separately)
                if attr_name == "style":
                    attrs_to_remove.append(attr_name)
                    continue
                
                # Check for malformed attribute values
                if isinstance(attr_value, str):
                    # Check for attributes that contain style fragments or look malformed
                    if ' style=' in attr_value or 'style="' in attr_value or "style='" in attr_value:
                        attrs_to_remove.append(attr_name)
                    # Check for attributes with suspicious patterns (multiple quotes, HTML entities in wrong places)
                    elif attr_value.count('"') > 2 or attr_value.count("'") > 2:
                        attrs_to_remove.append(attr_name)
                    # Check for attributes that look like they contain CSS or HTML entities incorrectly
                    elif '&quot;' in attr_value or 'rgb(' in attr_value or 'px' in attr_value:
                        attrs_to_remove.append(attr_name)
                # Check for attributes with suspicious names (containing quotes, semicolons, etc.)
                elif '&quot;' in str(attr_name) or ';' in str(attr_name) or '=' in str(attr_name):
                    attrs_to_remove.append(attr_name)
            
            # Remove malformed attributes
            for attr in attrs_to_remove:
                if attr in element.attrs:
                    del element[attr]
        
        return str(soup)
    else:
        # Fallback regex approach - fix common malformed patterns
        html = str(html_content)
        
        # Fix patterns like: target="_blank style=" or target='_blank style='
        html = re.sub(r'target\s*=\s*["\']_blank\s+style\s*=\s*["\']?', 'target="_blank" ', html, flags=re.IGNORECASE)
        html = re.sub(r'target\s*=\s*["\']_blank\s+style\s*=', 'target="_blank" ', html, flags=re.IGNORECASE)
        
        # Remove attributes that look malformed (contain HTML entities, CSS values, etc.)
        html = re.sub(r'\s+[a-zA-Z0-9_-]*&quot;[^>]*?=', ' ', html)
        html = re.sub(r'\s+[a-zA-Z0-9_-]*=\s*["\']?[^"\'>]*rgb\([^>]*?["\']?', ' ', html)
        
        return html


def remove_inline_styles(html_content):
    """
    Remove all inline style attributes from HTML content.
    This helps clean up HTML that comes from rich text editors.
    Returns the cleaned HTML as a string.
    """
    if not html_content:
        return html_content
    
    if HAS_BS4:
        # Use BeautifulSoup for proper HTML parsing
        soup = BeautifulSoup(str(html_content), "html.parser")
        
        # Remove style attribute from all elements
        for element in soup.find_all(True):  # True means all tags
            if element.has_attr("style"):
                del element["style"]
        
        return str(soup)
    else:
        # Fallback to regex-based approach
        html = str(html_content)
        
        # Remove style attributes (handles both single and double quotes)
        # Pattern matches: style="..." or style='...'
        pattern = r'\s*style\s*=\s*["\'][^"\']*["\']'
        html = re.sub(pattern, "", html, flags=re.IGNORECASE)
        
        return html


def clean_news_post_html(html_content):
    """
    Comprehensive cleaning function for news post HTML content.
    Applies malformed attribute fixing, style removal, and link fixing.
    Returns the cleaned HTML as a string.
    """
    if not html_content:
        return html_content
    
    # First fix malformed attributes, then remove inline styles, then fix links
    cleaned = fix_malformed_attributes(html_content)
    cleaned = remove_inline_styles(cleaned)
    cleaned = fix_links_in_html(cleaned)
    
    return cleaned
