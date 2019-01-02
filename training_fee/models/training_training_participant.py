# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.addons import decimal_precision as dp
from openerp.exceptions import Warning as UserError


class TrainingTrainingParticipant(models.Model):
    _inherit = "training.training_participant"

    @api.multi
    @api.depends(
        "fee_line_ids",
        "fee_line_ids.price_subtotal"
    )
    def _compute_total(self):
        for participant in self:
            untaxed = tax = total = 0.0
            fees = participant.fee_line_ids
            untaxed = sum(
                line.price_subtotal_wo_tax for line in fees)
            tax = sum(
                line.tax for line in fees)
            total = untaxed + tax
            participant.amount_untaxed = untaxed
            participant.amount_tax = tax
            participant.amount_total = total

    @api.multi
    @api.depends(
        "fee_line_ids",
        "fee_line_ids.invoice_line_id",
    )
    def _compute_invoice(self):
        for participant in self:
            result = False
            obj_fee = self.env["training.participant_fee"]
            criteria = [
                ("participant_id", "=", participant.id),
                ("invoice_line_id", "=", False)
            ]
            if obj_fee.search_count(criteria) == 0:
                result = True
            participant.invoiced = result

    @api.multi
    @api.depends(
        "fee_line_ids",
        "fee_line_ids.invoice_line_id",
    )
    def _compute_all_invoice(self):
        for participant in self:
            result = []
            for fee in participant.fee_line_ids:
                if fee.invoice_line_id:
                    result.append(fee.invoice_line_id.invoice_id.id)
            result = list(set(result))
            participant.invoice_ids = [(6, 0, result)]

    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="pricelist_id.currency_id",
        store=True,
        readonly=True,
    )
    payment_term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="account.payment.term",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    fee_line_ids = fields.One2many(
        string="Fee Lines",
        comodel_name="training.participant_fee",
        inverse_name="participant_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount_untaxed = fields.Float(
        string="Amount Untaxed",
        compute="_compute_total",
        digits=dp.get_precision("Account"),
        store=True,
    )
    amount_tax = fields.Float(
        string="Amount Tax",
        compute="_compute_total",
        digits=dp.get_precision("Account"),
        store=True,
    )
    amount_total = fields.Float(
        string="Amount Total",
        compute="_compute_total",
        digits=dp.get_precision("Account"),
        store=True,
    )
    invoiced = fields.Boolean(
        string="Invoiced",
        compute="_compute_invoice",
        store=True,
    )
    invoice_ids = fields.Many2many(
        string="Invoices",
        comodel_name="account.invoice",
        compute="_compute_all_invoice",
        store=False,
    )
    invoice_to = fields.Selection(
        string="Invoice Policy",
        selection=[
            ("self", "Self"),
            ("father", "Father"),
            ("mother", "Mother"),
            ("spouse", "Spouse"),
            ("guardian", "Guardian"),
            ("instituion", "Institution"),
        ],
        default="self",
        required=True,
    )
    invoice_to_id = fields.Many2one(
        string="Invoice To",
        comodel_name="res.partner",
        required=True,
    )

    @api.multi
    def onchange_training_id(self, training_id=False):
        _super = super(TrainingTrainingParticipant, self)
        result = _super.onchange_training_id(training_id)
        obj_training = self.env["training.training"]
        pricelist = False
        result["value"].update({
            "fee_line_ids": [],
            "pricelist_id": False,
            "payment_term_id": False,
        })
        if training_id:
            training = obj_training.browse([training_id])[0]

            if training.default_pricelist_id:
                pricelist = training.default_pricelist_id
                result["value"]["pricelist_id"] = \
                    pricelist.id

            if training.default_payment_term_id:
                result["value"]["payment_term_id"] = \
                    training.default_payment_term_id.id

            if training.fee_line_ids and pricelist:
                for fee in training.fee_line_ids:
                    price = pricelist.price_get(
                        prod_id=fee.product_id.id,
                        qty=fee.quantity)[pricelist.id]
                    result["value"]["fee_line_ids"].append((0, 0, {
                        "product_id": fee.product_id.id,
                        "quantity": fee.quantity,
                        "uom_id": fee.uom_id.id,
                        "price_unit": price,
                        "tax_ids": [(6, 0, fee.tax_ids.ids)],
                    }))
        return result

    @api.multi
    def onchange_pricelist_id(self, training_id, pricelist_id):
        result = {
            "value": {},
            "domain": {},
        }
        obj_training = self.env["training.training"]
        obj_pricelist = self.env["product.pricelist"]
        pricelist = False
        result["value"].update({
            "fee_line_ids": [],
        })
        if training_id and pricelist_id:
            training = obj_training.browse([training_id])[0]

            pricelist = obj_pricelist.browse([pricelist_id])[0]

            if training.fee_line_ids and pricelist:
                for fee in training.fee_line_ids:
                    price = pricelist.price_get(
                        prod_id=fee.product_id.id,
                        qty=fee.quantity)[pricelist.id]
                    result["value"]["fee_line_ids"].append((0, 0, {
                        "product_id": fee.product_id.id,
                        "quantity": fee.quantity,
                        "uom_id": fee.uom_id.id,
                        "price_unit": price,
                        "tax_ids": [(6, 0, fee.tax_ids.ids)],
                    }))
        return result

    @api.constrains(
        "state",
    )
    def _check_invoiced(self):
        for participant in self:
            if participant.state == "pass" and \
                    not participant.invoiced:
                # TODO: Msg
                msg = _("Not fully invoiced")
                raise UserError(msg)

    @api.onchange("invoice_to", "participant_id")
    def onchange_invoice_to(self):
        domain = {
            "invoice_to_id": [
                ("id", "=", 0),
            ]
        }
        if self.invoice_to == "self":
            self.invoice_to_id = \
                self.participant_id.partner_id
        elif self.invoice_to == "father":
            self.invoice_to_id = \
                self.participant_id.partner_id.father_id
        elif self.invoice_to == "mother":
            self.invoice_to_id = \
                self.participant_id.partner_id.mother_id
        elif self.invoice_to == "spouse":
            self.invoice_to_id = \
                self.participant_id.partner_id.spouse_id
        elif self.invoice_to == "guardian":
            self.invoice_to_id = \
                self.participant_id.partner_id.guardian_id
        elif self.invoice_to == "instituion":
            self.invoice_to_id = False
            domain["invoice_to_id"] = [
                ("is_company", "=", True),
                ("parent_id", "=", False)
            ]
        return {"domain": domain}
