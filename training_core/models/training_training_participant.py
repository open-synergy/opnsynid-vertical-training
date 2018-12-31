# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class TrainingTrainingParticipant(models.Model):
    _name = "training.training_participant"
    _inherit = ["mail.thread", "base.sequence_document",
                "base.workflow_policy_object"]
    _description = "Training Participant"

    @api.model
    def _default_date_register(self):
        return fields.Datetime.now()

    @api.model
    def _default_user_id(self):
        return self.env.user.id

    @api.multi
    @api.depends(
        "training_id",
    )
    def _compute_policy(self):
        _super = super(TrainingTrainingParticipant, self)
        _super._compute_policy()

    name = fields.Char(
        string="# Training Participant",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    participant_id = fields.Many2one(
        string="Participant",
        comodel_name="training.participant",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    training_id = fields.Many2one(
        string="Training",
        comodel_name="training.training",
        required=True,
        ondelete="cascade",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_register = fields.Datetime(
        string="Date Register",
        required=True,
        copy=False,
        default=lambda self: self._default_date_register(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        required=True,
        default=lambda self: self._default_user_id(),
        ondelete="cascade",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("approve", "Approved"),
            ("pass", "Passed"),
            ("fail", "Failed"),
            ("cancel", "Cancelled"),
        ],
        required=True,
        default="draft",
        copy=False,
    )
    cancel_reason_id = fields.Many2one(
        string="Cancel Reason",
        comodel_name="training.participant_cancel_reason",
        copy=False,
    )
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    approve_ok = fields.Boolean(
        string="Can Approve",
        compute="_compute_policy",
    )
    pass_ok = fields.Boolean(
        string="Can Mark as Pass",
        compute="_compute_policy",
    )
    fail_ok = fields.Boolean(
        string="Can Mark as Fail",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )
    # Log Fields
    confirmed_date = fields.Datetime(
        string="Confirmation Date",
        readonly=True,
        copy=False,
    )
    confirmed_user_id = fields.Many2one(
        string="Confirmation By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    approved_date = fields.Datetime(
        string="Approved Date",
        readonly=True,
        copy=False,
    )
    approved_user_id = fields.Many2one(
        string="Approved By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    passed_date = fields.Datetime(
        string="Marked as Pass Date",
        readonly=True,
        copy=False,
    )
    passed_user_id = fields.Many2one(
        string="Marked as Pass By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    failed_date = fields.Datetime(
        string="Marked as Fail Date",
        readonly=True,
        copy=False,
    )
    failed_user_id = fields.Many2one(
        string="Marked as Fail By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancelled_date = fields.Datetime(
        string="Cancellation Date",
        readonly=True,
        copy=False,
    )
    cancelled_user_id = fields.Many2one(
        string="Cancellation By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record["id"], record.participant_id.name))
        return result

    @api.multi
    def button_confirm(self):
        for participant in self:
            participant.write(participant._prepare_confirm_data())

    @api.multi
    def button_approve(self):
        for participant in self:
            participant.write(participant._prepare_approve_data())

    @api.multi
    def button_pass(self):
        for participant in self:
            participant.write(participant._prepare_pass_data())

    @api.multi
    def button_fail(self):
        for participant in self:
            participant.write(participant._prepare_fail_data())

    @api.multi
    def button_cancel(self, cancel_reason_id=False):
        for participant in self:
            participant.write(
                participant._prepare_cancel_data(cancel_reason_id))

    @api.multi
    def button_reset(self):
        for participant in self:
            participant.write(participant._prepare_reset_data())

    @api.model
    def _prepare_confirm_data(self):
        result = {
            "state": "confirm",
            "confirmed_date": fields.Datetime.now(),
            "confirmed_user_id": self.env.user.id,
        }
        return result

    @api.model
    def _prepare_approve_data(self):
        result = {
            "state": "approve",
            "approved_date": fields.Datetime.now(),
            "approved_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_pass_data(self):
        self.ensure_one()
        result = {
            "state": "pass",
            "passed_date": fields.Datetime.now(),
            "passed_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_fail_data(self):
        self.ensure_one()
        result = {
            "state": "fail",
            "failed_date": fields.Datetime.now(),
            "failed_user_id": self.env.user.id,
        }
        return result

    @api.multi
    def _prepare_cancel_data(self, cancel_reason_id=False):
        self.ensure_one()
        result = {
            "state": "cancel",
            "cancelled_date": fields.Datetime.now(),
            "cancelled_user_id": self.env.user.id,
            "cancel_reason_id": cancel_reason_id,
        }
        return result

    @api.multi
    def _prepare_reset_data(self):
        self.ensure_one()
        result = {
            "state": "draft",
            "confirmed_date": False,
            "confirmed_user_id": False,
            "approved_date": False,
            "approved_user_id": False,
            "passed_date": False,
            "passed_user_id": False,
            "failed_date": False,
            "failed_user_id": False,
            "cancelled_date": False,
            "cancelled_user_id": False,
            "cancel_reason_id": False,
        }
        return result

    @api.model
    def create(self, values):
        _super = super(TrainingTrainingParticipant, self)
        result = _super.create(values)
        result.write({
            "name": result._create_sequence(),
        })
        return result
