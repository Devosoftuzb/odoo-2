from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

from datetime import datetime, date


class Group(models.Model):
    _name = 'eduhub.group'
    _description = 'Description'
    _inherit = 'mail.thread'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    course_id = fields.Many2one('eduhub.course', string='Group`s Course')
    students_ids = fields.Many2many('res.partner')

    start_time = fields.Char(string='Group Start Time', help='format - H:M', inverse='_check_start_time')
    end_time = fields.Char(string='Group End Time', help='format - H:M', inverse='_check_end_time')
    start_time_datetime = fields.Datetime(compute='_compute_start_time', store=True)
    end_time_datetime = fields.Datetime(compute='_compute_end_time', store=True)

    days = fields.Many2many('eduhub.week.day', string='Week Days')
    status = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')])
    students_count = fields.Integer(string='Students Count', compute='_compute_students_count')

    @api.depends('start_time')
    def _compute_start_time(self):
        for record in self:
            if record.start_time:
                try:
                    today = date.today()  # Use today's date as the date part
                    start_time = datetime.strptime(record.start_time, "%H:%M").time()
                    record.start_time_datetime = datetime.combine(today, start_time)
                except ValueError:
                    record.start_time_datetime = False
            else:
                record.start_time_datetime = False

    @api.depends('end_time')
    def _compute_start_time(self):
        for record in self:
            if record.end_time:
                try:
                    today = date.today()  # Use today's date as the date part
                    start_time = datetime.strptime(record.end_time, "%H:%M").time()
                    record.end_time_datetime = datetime.combine(today, start_time)
                except ValueError:
                    record.end_time_datetime = False
            else:
                record.end_time_datetime = False

    @api.depends('students_count')
    def _compute_students_count(self):
        for rec in self:
            if rec.students_ids:
                rec.students_count = len(rec.students_ids)
            else:
                rec.students_count = 0

    @api.onchange('students_ids')
    def _check_student_id(self):
        if not self.course_id and self.students_ids:
            return {
                'warning': {
                    'title': _('Missing Course'),
                    'message': _('First add a course.'),
                }
            }

        invalid_students = []
        for student_id in self.students_ids:
            if int(str(student_id.id).split('_')[1]) not in self.course_id.students_ids.ids:
                invalid_students.append(str(student_id.name))

        if invalid_students:
            return {
                'warning': {
                    'title': _('Invalid Students'),
                    'message': _('You can only add students available in the course: %s' % ', '.join(invalid_students)),
                }
            }

    def _check_start_time(self):
        for rec in self:
            if rec.start_time:
                self._is_valid_time(rec.start_time)

            if rec.start_time and rec.end_time:
                rec._check_time_range()

    def _check_end_time(self):
        for rec in self:
            if rec.end_time:
                self._is_valid_time(rec.end_time)

            if rec.start_time and rec.end_time:
                rec._check_time_range()

    def _check_time_range(self):
        for record in self:
            try:
                start = datetime.strptime(record.start_time, '%H:%M')
                end = datetime.strptime(record.end_time, '%H:%M')
                if start > end:
                    raise ValidationError(_('The start time cannot be after the end time.'))
            except (ValueError, TypeError):
                raise ValidationError(_('Invalid time format. Please enter the time in HH:MM format.'))

    def _is_valid_time(self, time_str):
        try:
            datetime.strptime(time_str, '%H:%M')
        except (ValueError, TypeError):
            raise ValidationError(_('Enter a valid time format (HH:MM).'))

    def action_active(self):
        self.status = 'active'

    def action_inactive(self):
        self.status = 'inactive'


class WeekDay(models.Model):
    _name = 'eduhub.week.day'
    _description = 'Week Days'

    name = fields.Char(string='Day', required=True)
