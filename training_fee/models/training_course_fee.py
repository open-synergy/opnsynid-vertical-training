# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class TrainingCourseFee(models.Model):
    _name = "training.course_fee"
    _description = "Training Course Fee"

    course_id = fields.Many2one(
        string="Course",
        comodel_name="training.course",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        required=True,
    )
    product_id = fields.Many2one(
        string="Fee Component",
        comodel_name="product.product",
        required=True,
        ondelete="restrict",
    )
    quantity = fields.Float(
        string="Quantity",
        required=True,
        default=1.0,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        required=True,
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_course_fee_2_tax",
        column1="tax_fee_id",
        column2="tax_id",
        domain=[
            ("type_tax_use", "=", "sale"),
        ]
    )

    @api.multi
    def onchange_product_id(self, product_id):
        value = {
            "tax_ids": False,
            "uom_id": False,
        }
        domain = {}
        if product_id:
            product = self.env["product.product"].browse([product_id])[0]
            categ_id = product.uom_id.category_id.id
            domain.update({
                "uom_id": [
                    ("category_id", "=", categ_id)
                ]
            })
            value["tax_ids"] = [(6, 0, product.taxes_id.ids)]
            value["uom_id"] = product.uom_id.id
        return {"value": value, "domain": domain}
