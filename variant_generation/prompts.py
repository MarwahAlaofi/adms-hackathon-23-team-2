# Common Fields
CAMPAIGN_MESSAGE = "Craft a detailed persona based on the above description that I can use for a political campaign " \
                   "messaging."
JSON_FIELDS = [
    'name', 'age', 'gender', 'occupation', 'income', 'education', 'location',
    'background', 'values', 'goals', 'pain points'
]

# Personas Dictionary
PERSONAS = {
    'activist_egalitarian': {
        'text': (
            "As an Activist Egalitarian who has a strong social conscience and believes "
            "governments should intervene to make society more equitable. Strong believers "
            "in the redistribution of wealth and public investment, they are socially progressive, "
            "support climate action and want to protect Australian manufacturing. "
            "This group is quite evenly split between city and regional, and across age groups. "
            "Generally speaking, the less you earn the more likely you are to be an Egal. "
            "Victorians are twice as likely to be an Active Egal as a Queenslander. "
            "Nearly 21 per cent of women are Egals, but only 15.5 per cent of men. "
            "Most likely to get on with: Progressive Cosmopolitans, particularly around social issues. "
            "Least likely to get on with: Anti-Establishment Firebrands are not your friends."
        ),
        'campaign_message': CAMPAIGN_MESSAGE,
        'json_fields': JSON_FIELDS
    },
    'prudent_traditionalist': {
        'text': (
            "Prudent Traditionalists share a lot of values with conservatives from days gone by. "
            "They believe the world is changing too quickly and would like a return to traditional "
            "social values, but aren't likely to fire up about the issues of the day. Unimpressed "
            "by luxury and not career-oriented, they are savers rather than spenders, reflecting their "
            "cautious approach to life more generally. They believe government should intervene to make "
            "people's lives safer and want offshore processing of asylum seekers to continue. "
            "The biggest tribe by some margin, Trads are spread pretty evenly across the states, "
            "but Victorians are least likely to be one. Someone living outside a capital city is "
            "almost 50 per cent more likely to be a Trad. National voters are overwhelmingly Trads. "
            "Greens voters are least likely to be Trads. But Trads also are more likely than average "
            "to vote for minor parties. Nearly 50 per cent of the population aged over 65 are Trads."
        ),
        'campaign_message': CAMPAIGN_MESSAGE,
        'json_fields': JSON_FIELDS
    }
}
