from odoo import models, fields

class OnboardingConfirmation(models.TransientModel):
    _name = 'onboarding.confirmation'
    _description = 'Wizard to Confirm Student Onboarding'

    confirmation_date = fields.Date(string="Confirmation Date", required=True)
    teacher_id = fields.Many2one('teacher.details', string="Referenced by", required=True)
    student_ids = fields.Many2many('student.details', string="Students to Onboard", required=True)
    course_ids = fields.Many2many('course.details', string="Courses", required=True)

    def action_confirm(self):
        self.ensure_one()
        for student in self.student_ids:
            student.write({
                'confirm_date': self.confirmation_date,
                'professor_associate': self.teacher_id.id,
                'subject_of_student': [(6, 0, self.course_ids.ids)],
            })
        return {'type': 'ir.actions.act_window_close'}