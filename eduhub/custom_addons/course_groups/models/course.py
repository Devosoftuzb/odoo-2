from odoo import fields, models, api


class Course(models.Model):
    _name = 'eduhub.course'
    _description = 'Description'
    _inherit = 'mail.thread'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    duration = fields.Float(string='Duration', help='Enter in month')
    instructors_ids = fields.Many2many('hr.employee', string='Instructors')
    students_ids = fields.Many2many('res.partner', string='Students')
    price = fields.Float(string='Price', required=True)
    image = fields.Binary(attachment=True)
    tags_ids = fields.Many2many('eduhub.course.tag')
    groups_ids = fields.One2many('eduhub.group', 'course_id', string='Groups')
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], default='inactive')
    students_count = fields.Integer(string='Students Count', compute='_compute_students_count')

    @api.depends('students_count')
    def _compute_students_count(self):
        for rec in self:
            if rec.students_ids:
                rec.students_count = len(rec.students_ids)
            else:
                rec.students_count = 0



class Tag(models.Model):
    _name = 'eduhub.course.tag'
    _description = 'EduHUB Courses` Tags'

    name = fields.Char()
    color = fields.Integer(string='Color')
