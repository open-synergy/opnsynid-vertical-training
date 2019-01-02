# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields


class TrainingCreateInvoice(models.TransientModel):
    _name = "training.create_invoice"
    _description = "Create Invoice From Training Participant"

    @api.model
    def _default_training_participant_id(self):
        tp_id = self._context.get("active_id", False)
        return tp_id

    training_participant_id = fields.Many2one(
        string="# Training Participant",
        comodel_name="training.training_participant",
        required=True,
        default=lambda self: self._default_training_participant_id(),
    )
    fee_line_ids = fields.Many2many(
        string="Training Fee",
        comodel_name="training.participant_fee",
        required=True,
        relation="rel_training_create_invoice_2_fee",
        column1="wizard_id",
        column2="fee_id",
    )
    date_invoice = fields.Date(
        string="Invoice Date",
        required=True,
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        domain=[
            ("type", "=", "sale"),
        ],
    )

    @api.multi
    def action_create_invoice(self):
        for wiz in self:
            wiz._create_invoice()

    @api.multi
    def _create_invoice(self):
        self.ensure_one()
        obj_invoice = self.env["account.invoice"]
        obj_line = self.env["account.invoice.line"]
        invoice = obj_invoice.create(self._prepare_invoice_data())
        for fee in self.fee_line_ids:
            line = obj_line.create(self._prepare_invoice_line(fee, invoice.id))
            fee.write({"invoice_line_id": line.id})
        self.training_participant_id.write({"invoice_ids": [(4, invoice.id)]})

    @api.multi
    def _prepare_invoice_data(self):
        self.ensure_one()
        tp = self.training_participant_id
        partner = tp.participant_id.partner_id
        payment_term_id = tp.payment_term_id and \
            tp.payment_term_id.id or \
            False
        return {
            "journal_id": self.journal_id.id,
            "partner_id": tp.invoice_to_id.id,
            "date_invoice": self.date_invoice,
            "origin": self.training_participant_id.name,
            "type": "out_invoice",
            "payment_term_id": payment_term_id,
            "account_id": partner.property_account_receivable.id,
        }

    @api.multi
    def _prepare_invoice_line(self, fee, invoice_id):
        self.ensure_one()
        result = {
            "invoice_id": invoice_id,
            "name": fee.product_id.name,
            "product_id": fee.product_id.id,
            "price_unit": fee.price_unit,
            "account_id": fee.product_id.property_account_income.id,
            "quantity": fee.quantity,
            "invoice_line_tax_id": [(6, 0, fee.tax_ids.ids)]
        }
        return result

    @api.multi
    def onchange_training_participant_id(self, tp_id):
        value = {
            "fee_line_ids": []
        }
        domain = {
            "fee_line_ids": [
                ("id", "=", 0),
            ]
        }
        if tp_id:
            obj_tp = self.env["training.training_participant"]
            tp = obj_tp.browse([tp_id])[0]
            domain["fee_line_ids"] = [
                ("invoice_line_id", "=", False),
                ("participant_id", "=", tp_id),
            ]
            fees = tp.fee_line_ids.filtered(lambda r: not r.invoice_line_id)
            if len(fees) > 0:
                value["fee_line_ids"] = [(6, 0, fees.ids)]
        return {"value": value, "domain": domain}
