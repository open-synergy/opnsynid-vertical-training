# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class TrainingParticipantFee(models.Model):
    _name = "training.participant_fee"
    _description = "Training Participant Fee"

    @api.multi
    @api.depends(
        "price_unit",
        "quantity",
        "uom_id",
        "product_id",
        "tax_ids",
    )
    def _compute_subtotal(self):
        for fee in self:
            subtotal = 0.0
            price = fee.price_unit
            taxes = fee.tax_ids
            tax_compute = taxes.compute_all(
                price,
                fee.quantity,
                product=fee.product_id
            )
            subtotal = tax_compute["total_included"]
            subtotal_wo_tax = tax_compute["total"]
            tax = tax_compute["total_included"] - subtotal_wo_tax
            fee.price_subtotal = subtotal
            fee.tax = tax
            fee.price_subtotal_wo_tax = subtotal_wo_tax

    @api.multi
    @api.depends(
        "invoice_line_id",
    )
    def _compute_invoice(self):
        for fee in self:
            if fee.invoice_line_id:
                result = True
            else:
                result = False
            fee.invoiced = result

    participant_id = fields.Many2one(
        string="Course Participant",
        comodel_name="training.training_participant",
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
    price_unit = fields.Float(
        string="Price Unit",
        required=True,
        digits=dp.get_precision("Account"),
    )
    quantity = fields.Float(
        string="Quantity",
        required=True,
        digits=dp.get_precision("Product Unit of Measure"),
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
        relation="rel_participant_fee_2_tax",
        column1="tax_fee_id",
        column2="tax_id",
    )
    tax = fields.Float(
        string="Tax",
        compute="_compute_subtotal",
        digits=dp.get_precision("Account"),
        store=True,
    )
    price_subtotal = fields.Float(
        string="Price Subtotal",
        compute="_compute_subtotal",
        digits=dp.get_precision("Account"),
        store=True,
    )
    price_subtotal_wo_tax = fields.Float(
        string="Price Subtotal",
        compute="_compute_subtotal",
        digits=dp.get_precision("Account"),
        store=True,
    )
    invoice_line_id = fields.Many2one(
        string="Invoice Line",
        comodel_name="account.invoice.line",
        ondelete="restrict",
    )
    invoiced = fields.Boolean(
        string="Invoiced",
        compute="_compute_invoice",
        store=True,
    )

    @api.multi
    def action_delete_invoice(self):
        self.ensure_one()
        inv = self.invoice_line_id.invoice_id
        obj_fee = self.env["training.participant_fee"]
        criteria = [
            ("invoice_line_id.invoice_id.id", "=", inv.id),
        ]
        obj_fee.search(criteria).write({"invoice_line_id": False})
        inv.unlink()
        # return {"type": "ir.actions.act_window.none"}
