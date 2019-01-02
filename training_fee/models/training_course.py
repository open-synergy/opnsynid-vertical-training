# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class TrainingCourse(models.Model):
    _inherit = "training.course"

    default_pricelist_id = fields.Many2one(
        string="Default Pricelist",
        comodel_name="product.pricelist",
        company_dependent=False,
        domain=[
            ("type", "=", "sale"),
        ],
    )
    default_payment_term_id = fields.Many2one(
        string="Default Payment Term",
        comodel_name="account.payment.term",
        company_dependent=False,
    )
    fee_line_ids = fields.One2many(
        string="Fee Lines",
        comodel_name="training.course_fee",
        inverse_name="course_id",
    )
