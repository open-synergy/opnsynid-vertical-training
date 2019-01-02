# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class TrainingTraining(models.Model):
    _inherit = "training.training"

    default_pricelist_id = fields.Many2one(
        string="Default Pricelist",
        comodel_name="product.pricelist",
        company_dependent=True,
    )
    default_payment_term_id = fields.Many2one(
        string="Default Payment Term",
        comodel_name="account.payment.term",
        company_dependent=True,
    )
    fee_line_ids = fields.One2many(
        string="Fee Lines",
        comodel_name="training.training_fee",
        inverse_name="training_id",
    )

    @api.multi
    def onchange_course_id(self, course_id):
        _super = super(TrainingTraining, self)
        result = _super.onchange_course_id(course_id)
        obj_course = self.env["training.course"]
        result["value"].update({
            "fee_line_ids": [],
            "default_pricelist_id": False,
            "default_payment_term_id": False,
        })
        if course_id:
            course = obj_course.browse([course_id])[0]
            if course.default_pricelist_id:
                result["value"]["default_pricelist_id"] = \
                    course.default_pricelist_id.id

            if course.default_payment_term_id:
                result["value"]["default_payment_term_id"] = \
                    course.default_payment_term_id.id

            if course.fee_line_ids:
                for fee in course.fee_line_ids:
                    result["value"]["fee_line_ids"].append((0, 0, {
                        "product_id": fee.product_id.id,
                        "quantity": fee.quantity,
                        "uom_id": fee.uom_id.id,
                        "tax_ids": [(6, 0, fee.tax_ids.ids)],
                    }))
        return result
