from resources import pretty


def apply_environment(app):
    app.jinja_env.filters['pretty_date'] = pretty.date
