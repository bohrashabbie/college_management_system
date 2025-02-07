from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class TeacherDetails(models.Model):
     _name = "teacher.details"
     _description = "Teacher Details"
     _rec_name = "tname"

     tname = fields.Char(string="Professor Name", required=True)
     sub_of_teacher = fields.Selection([('cse','CSE'),('ai', 'AI/DS')], string="Subject of Professor")
     tgender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string="Gender", required=True
     )
     date_of_birth = fields.Date(string="Date of Birth", required=True)
     tage = fields.Integer(string="Teacher age", required=True)
     teacher_description = fields.Text(string="Description")
     t_id = fields.Integer(string = "Professor Id", required=True)
     description = fields.Text(string = "Description") 
     teacher_image = fields.Image(string = "",max_height = 0, max_weidth = 0)
     teacher_email = fields.Char(string = "Email of the Teacher", required=True)
     teacher_phone = fields.Char(string = "Mobile Number", required=True)
     student_associated = fields.One2many(comodel_name='student.details', 
                                          inverse_name="professor_associate")

     @api.constrains('teacher_email')
     def _check_email(self):
        """This function is use to validate the email"""
        for record in self:
            if record.teacher_email and  not re.match(r"[^@]+@[^@]+\.[^@]+", record.teacher_email):
                    raise ValidationError("Invalid email format")

     @api.constrains('teacher_phone')
     def _check_phone(self):
        """This function is used to check the phone number"""
        for record in self:
            if record.teacher_phone and  not re.match(r"(0|91)?[6-9][0-9]{9}", record.teacher_phone):
                    raise ValidationError("Please enter a valid phone number")
    
