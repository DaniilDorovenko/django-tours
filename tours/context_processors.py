from data import departures, title, subtitle, description


def get_similar_content(request):

    similar_content = {
        'departures': departures,
        'title': title,
        'subtitle': subtitle,
        'description': description,
    }

    return similar_content
