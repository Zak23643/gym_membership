# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta


class MemberMembership(models.Model):
    """
    Model to manage the membership of a specific gym member.
    This links a member (res.partner) to a membership plan.
    """
    _name = 'gym.member.membership'
    _description = 'Gym Member Membership'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # For chatter and activity scheduling
    _order = "start_date desc"

    name = fields.Char(
        string='Membership ID',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    member_id = fields.Many2one(
        'res.partner',
        string='Member',
        required=True,
        domain=[('customer_rank', '>', 0)],  # Show only customers
        help="The person who is a member of the gym."
    )
    plan_id = fields.Many2one(
        'gym.membership.plan',
        string='Membership Plan',
        required=True,
        help="The membership plan subscribed by the member."
    )
    start_date = fields.Date(
        string='Start Date',
        required=True,
        default=fields.Date.context_today,
        help="The date when the membership becomes active."
    )
    end_date = fields.Date(
        string='End Date',
        compute='_compute_end_date',
        store=True,
        readonly=True,
        help="The date when the membership expires."
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to assign a sequence-based name."""
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('gym.member.membership') or _('New')
        return super().create(vals_list)

    @api.depends('start_date', 'plan_id.duration_value', 'plan_id.duration_unit')
    def _compute_end_date(self):
        """Calculate the end date based on the start date and plan duration."""
        for rec in self:
            if rec.start_date and rec.plan_id:
                duration_value = rec.plan_id.duration_value
                duration_unit = rec.plan_id.duration_unit

                # Using relativedelta for accurate date calculations
                delta_args = {duration_unit: duration_value}
                rec.end_date = rec.start_date + relativedelta(**delta_args)
            else:
                rec.end_date = False

    def action_activate(self):
        """Set the membership state to 'Active'."""
        self.write({'state': 'active'})

    def action_cancel(self):
        """Set the membership state to 'Cancelled'."""
        self.write({'state': 'cancelled'})

    def _check_expired_memberships(self):
        """
        Scheduled action method to automatically set memberships to 'Expired'.
        This is meant to be called by a cron job.
        """
        today = date.today()
        expired_memberships = self.search([
            ('state', '=', 'active'),
            ('end_date', '<', today)
        ])
        expired_memberships.write({'state': 'expired'})
