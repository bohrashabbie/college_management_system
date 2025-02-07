from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class StudentDetails(models.Model):
    """This class is used to manage the details of student and professors"""
    _name = "student.details"
    _description = "Student Details"
    _rec_name = 'sname'

    sname  = fields.Char(string="Student Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    student_branch = fields.Selection([('computer science', "CSE"), ('Artificial Intelligence','AI')], string="Student Branch", required=True)
    roll_num = fields.Char(string="Roll Number", required=True, help="Roll number is the unique id of each student")
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string="Gender", required=True
    )
    student_description = fields.Text(string="Description")
    student_image = fields.Image(string="", max_height=0, max_weidth=0)
    student_email = fields.Char(string="Email of the student", required=True)
    phone = fields.Char(string='Phone', required=True)
    total_number = fields.Float(string="Total Number", default=600)
    obtained_number = fields.Float(string="Number Obtained", default=0)
    Percentage = fields.Float(string="Percentage obtained", compute="_compute_percentage")
    user_name = fields.Char(string="User name")
    is_active_student = fields.Boolean(string="Is Student active", default=True)
    exam_type = fields.Selection([('Odd Sem', 'Odd Semester'), ('Even Semester', 'Even Semester')], string="Choose Semester")
    professor_associate = fields.Many2one(comodel_name='teacher.details', string='Teacher Associated')
    birth_date = fields.Date(string="Birth Date")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    subject_of_student = fields.Many2many(comodel_name='course.details',
                                          column1='subject',
                                          relation="subject_of_student",
                                          string="Subject of the Student")
    confirm_date = fields.Date(string="Confirm Date")
    
    # New computed field for onboarding status
    onboarding_status = fields.Selection(
        [('confirmed', 'Confirmed'), ('unconfirmed', 'Unconfirmed')],
        string="Onboarding Status",
        compute="_compute_onboarding_status",
        store=True
    )

    @api.depends('confirm_date')
    def _compute_onboarding_status(self):
        """Compute the onboarding status based on confirm_date.
           If confirm_date is set, the status is 'confirmed'; otherwise, 'unconfirmed'."""
        for record in self:
            record.onboarding_status = 'confirmed' if record.confirm_date else 'unconfirmed'

    @api.constrains('student_email')
    def check_email(self):
        for record in self:
            if record.student_email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.student_email):
                raise ValidationError("Invalid email format")

    @api.constrains('phone')
    def check_phone(self):
        for record in self:
            if record.phone and not re.match(r"(0|91)?[6-9][0-9]{9}", record.phone):
                raise ValidationError("Please enter a valid phone number")

    @api.depends('total_number', 'obtained_number')
    def _compute_percentage(self):
        """Compute percentage based on total_number and obtained_number."""
        for record in self:
            if record.obtained_number > 0 and record.obtained_number <= 600:
                record.Percentage = (record.obtained_number / record.total_number) * 100
            else:
                record.Percentage = 0.0

    @api.onchange('sname', 'last_name')
    def onchange_user_name(self):
        """Create username by concatenating first and last names."""
        if self.sname and self.last_name:
            self.user_name = self.sname + self.last_name
        else:
            self.user_name = ''


    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_true(self):
        """Raise an error if trying to delete active students."""
        if any(record.is_active_student for record in self):
            raise ValidationError("You cannot delete active students.")

    @api.model
    def create(self, vals):
        if "roll_num" in vals:
            existing_roll = self.env['student.details'].search([("roll_num", "=", vals["roll_num"])])
            if existing_roll:
                raise ValidationError("Student with this roll number already exists.")
        return super(StudentDetails, self).create(vals)

    @api.depends('birth_date')
    def _compute_age(self):
        """Calculate age using birth_date and current date with validations."""
        for student in self:
            if student.birth_date:
                today = fields.Date.today()
                birth_date = student.birth_date
                if birth_date > today:
                    raise ValidationError("Birth date cannot be in the future.")
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                if age < 18:
                    raise ValidationError("Age must be 18 years or older.")
                student.age = age
            else:
                student.age = 0


    def action_verify_wizard():
        return {
            'name': 'verify',
            'type': 'ir.actions.act_window',
            'res_model': 'onboarding.confirmation',
            'views': [(False, 'form'), (False, 'list')],
            'target': 'new',
        }
