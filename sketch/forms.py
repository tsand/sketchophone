from resources.flask_wtf import Form, TextField, IntegerField, HiddenField, SubmitField
from resources.flask_wtf import Required, AnyOf, NumberRange

class EditGameForm(Form):
    # Error messages
    required = '%s required'

    # Fields
    name = TextField('Name', [Required(message=required % 'Name')])
    rounds = IntegerField('Rounds', [NumberRange(min=3)])
    type = HiddenField('Type', [AnyOf(['public', 'private'])])
    submit = SubmitField('Save Settings')
