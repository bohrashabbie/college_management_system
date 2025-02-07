from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class CourseDetails(models.Model):
    _name = "course.details"
    _description = "This is the model for the courses student are enrolled in "
    _rec_name = "subject"

    subject = fields.Selection([('oops', 'OOPS'), ('dbms', 'DBMS'), ('os', 'OS'), ('cnn', 'CNN'), ('ai', 'AI'), ('ml', 'ML'), 
                                       ('bda', 'BDA'), ('maths', 'Advances Math')], string="Select the subject")
