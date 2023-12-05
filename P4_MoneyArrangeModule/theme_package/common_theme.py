""" 主题颜色配置文件，包含以下可选配置：
    1、default_theme: 默认配置
    2、dark_theme: 暗色主题
"""


class CommonTheme:

    default_theme = {
        'main_top': {
            'bgcolor': '#333',
            'fontcolor': '#000',
            'checkbox_color': '#fff',
        },
        'main_body': {
            'bgcolor': '#eee',
            'fontcolor': '#000',
            'item_box': {
                'bgcolor': '#fff',
                'fontcolor': '#000',
            },
        },
        'main_btn': {
            'bgcolor': '#3276B1',
            'border': '0px',
        },
        'layer': {
            'bgcolor': '#fff',
            'border_bottom_color': '#F0F0F0',
            'title_color': '#333',
        },
        'main_right': {
            'bgcolor': '#aaa',
            'fontcolor': '#000',
            'category_section_bgcolor': '#B0C4DE',
            'category_section_bordercolor': '#E9ECEF',
        },
        'mindmap': {
            'line_color': '#555',
        },
        'table': {
            'header_bgcolor': '#FAFAFA',
            'page_div_bgcolor': '',
            'bgcolor': '#fff',
            'fontcolor': '#666'
        },
        'blockquote': {
            'bgcolor': '#fff',
            'fontcolor': '#000'
        },
        'calendar': {
            'layer': {
                'header_bgcolor': '#4387C2',
                'body_bgcolor': '#eee'
            },
            'now_day_bgcolor': 'rgba(255, 220, 40, 0.15)',
            'list_grid': {
                'header_bgcolor': '#3276B1',
                'hover_bgcolor': '#5B88AE'
            }
        },
    }

    dark_theme = {
        'main_top': {
            'bgcolor': '#3C3F41',
            'fontcolor': '#eff',
            'checkbox_color': '#2B2B2B',
        },
        'main_body': {
            'bgcolor': '#2B2B2B',
            'fontcolor': '#cdd',
            'item_box': {
                'bgcolor': '#3D3E40',
                'fontcolor': '#bbb',
            }
        },
        'main_btn': {
            'bgcolor': '#3276B1',
            'border': '0px',
        },
        'layer': {
            'bgcolor': '#2B2B2B',
            'border_bottom_color': '#2B2B2B',
            'title_color': '#eff'
        },
        'main_right': {
            'bgcolor': '#3C3F41',
            'fontcolor': '#eff',
            'category_section_bgcolor': '#3C3F41',
            'category_section_bordercolor': '#E9ECEF',
        },
        'mindmap': {
            'line_color': '#888',
        },
        'table': {
            'header_bgcolor': '#3D3E40',
            'page_div_bgcolor': '#3D3E40',
            'bgcolor': '#2B2B2B',
            'fontcolor': '#cdd'
        },
        'blockquote': {
            'bgcolor': '#1C1B22',
            'fontcolor': '#cdd'
        },
        'calendar': {
            'layer': {
                'header_bgcolor': '#3C3F41',
                'body_bgcolor': '#2B2B2B'
            },
            'now_day_bgcolor': 'rgba(32, 78, 138, 0.25)',
            'list_grid': {
                'header_bgcolor': '#181A1F',
                'hover_bgcolor': '#3C3F41',
            }
        },
    }
