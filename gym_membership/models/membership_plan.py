# -*- coding: utf-8 -*-

from odoo import models, fields


class GymMembershipPlan(models.Model):
    """
    Model to define different types of membership plans available in the gym.
    e.g., Gold Monthly, Silver Annual, etc.
    """
    _name = 'gym.membership.plan'
    _description = 'Gym Membership Plan'
    _order = 'name'

    name = fields.Char(string='Plan Name', required=True, help="Name of the membership plan, e.g., 'Gold Monthly'")

    duration_value = fields.Integer(
        string='Duration',
        default=1,
        help="Numerical value of the plan's duration"
    )
    duration_unit = fields.Selection([
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
        ('years', 'Years'),
    ], string='Duration Unit', default='months', required=True, help="Unit of the plan's duration")

    price = fields.Float(
        string='Price',
        required=True,
        help="The cost of this membership plan"
    )

    description = fields.Text(string='Description', help="Describe the benefits and features of this plan.")

    active = fields.Boolean(default=True, help="If unchecked, it will allow you to hide the plan without removing it.")
