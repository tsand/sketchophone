from sketch import views as sketch_views

def apply_urls(app):
    app.add_url_rule('/sketch/', view_func=sketch_views.SketchView.as_view('sketch'))
    app.add_url_rule('/sketch/create/', view_func=sketch_views.CreationWizard.as_view('wizard'))
    
